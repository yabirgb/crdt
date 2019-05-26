# CRDT algorithm: Counter

## Setup

With this file you can find a `docker-compose.yml` file containing the
needed configuration to mount a docker container with all the setup ready
to run this project.

The docker project opens a connection on port 8000 so you can go visit
the url [http://localhost:8000](http://localhost:8000). 

In this webpage you can find different things:

- A monitorizing tool where for each server you find the counter of
  views for a certain video that the server has stored (the growing counter)
- A little web form so you can send a certain number of views to a node
- A button to prepare a test where each server recives a random amount of views

The webpage fetches every two seconds information from the server.

## What I have done

### Research

First of all I've researched on the topic of CRDTs. I've found that it
works because what it's really being build is a _lattice structure_.
A lattice is in mathematics a structure where every two elements have
supremum and infimum, both uniques. What we are doing with the counter
is to define the supreme operation as the maximum of two numbers that
verifies the properties of being _idempotent_ and transitive. For this
reason asynctotycally what we are doing is to reach the total number
of views registered individually by each server.

### System design

Each node in the network is represented by an instance of the class
`Server`.  Each server has a unique id, a variable being `True` when
the server is active on the network and a dictionary of the known
state of the network.

The _CRDT-counter_ operations are implemented in this class, those are:

- `incr(video_id)`: Increment the counter for the video in the current node by 1.
- `incr_by(video_id, amount)`: Increment the counter for the video in
  the current node by `amount`.
- `set_to(video_id, amount)`: Set the views counter to a certain amount.
- `total(video_id)`: Total number of views received in the node.
- `count(video_id)`: Total number of views of the video in the network (as known by now by the node).
- `merge(server)`: The operation that using the max function updates
  the state of the local counter.

The class `Cluster` is the one representing the network that all the
servers build. Its task in the program is to build each server,
populate it's list of servers and communicate with the frontend for
tasks like deleting a node or watching a video in a node (the idea is
that this class acts like the load balancer or the router that matches
your location with the right server).

The main script is a [sanic
server](https://github.com/huge-success/sanic). I've choosen sanic
because is a flask like framework that can work asyncronously. I've
created a task with it that every 2 seconds performs the merge
operation for a certain server each time (to test the interface
working only one node communicate with 5 nodes each time). Also sanic
provides the API endpoints for the web interface to operate on the
program.  I've chosen to build a web interface because it emulates
the activity proposed in the exercise while I can easily manage the
state of the system.

### Things that I changed

Firstly I implemented the system for just one video but the
generalization for a bigger number of videos was easy to implement.
For this reason each instance of `Server` doesn't assume that the number of videos
is 1 but to make easy the web interface I just made available one
video.

### About the problem and my implementation

With the code provided I belive to achieve the task proposed:

- Read up on CRDTs and specifically Grow-Only counters
- Write a program that simulates the distributed system of multiple independent nodes
- Simulate the process of a fixed number of page views being sent to an arbitrary node
- Implement a Grow-Only counter that is used to respond to incoming page views
- Build a simple frontend visualization of the page counter

In my implementation the nodes are "interconnected" in the way that
they have direct access to their data so they just "talk" with each
other asking for the info (it simulates a distributed system but is
not a distributed system).

If this is an error on how I understood the problem and alternative
solution will reimplement the system being distributed as:

- Each instance of the class `Server` is a different programm running
  isolated.
- Each server has an API endpoint where I can `POST` a json object
  containing pairs of videos ids and the number of views.
- The merge operation is implemented in that API endpoint but this
  time I use the information provided instead of just going and look
  for it, as I do now.
- Eeach server should now know where to locate each other, let's say
  by knowing their ports and ip's.
- Now the cluster class is not necessary.

### About the questions

**What can happen when the user reloads the website? Can we synchronize the counter
not only across nodes but also across the nodes and the frontend?**

When the user reloads the website the site should show the same or a
greater counter depending on the updated counter. We can introduce the
frontend as one more server and sync the counter with it too. In this
case when the user reloads the website we can expect that the program
destroys the frontend from the list of connected servers loosing its
counter.

**What happens if a node gets removed from the cluster? What happens if more nodes
get added to the cluster?**

If a server gets removed from the cluster we'll loose the counter
information corresponding to this node unless it syncronizes it's
information with at least one node before being destroyed.  If a node
gets added to the cluster it's inmediatly known by the rest of servers
and after a certain period of time it'll retrive the up to date
information.

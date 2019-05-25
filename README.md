# CRDT algorithm: Counter

## Setup

With this file you can find a `docker-compose.yml` file containing the
needed instructions to mount a docker container with all the setup ready
to run this project.

The docker project opens a connection on port 8000 so you can go visit
the url [http://localhost:8000](http://localhost:8000). 

In this webpage you can find different things:

- A monitorizing tool where for each server you find the counter of
  views for a certain video that the server has stored (the growing counter).
- A little web form so you can send a certain number of views to a node
- A button to load a test where each server is loaded with a random amount of views

The webpage fetches every two seconds information from the server.

## What I have done

### Reseach

First of all I've researched on the topic of CRDTs. I've found that it
works because what it's really being build is a _lattice structure_.
A lattice is in mathematics a structure where every two elements have
supremum and infimum, both uniques. What we are doing with the counter
is to define the supreme operation as the maximum of two numbers that
verifies the properties of being _idempotent_ (operation applied to an
object and itself results in the same object) and transitive. For this
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
- `count(video_id)`: Total number of views of the video in the network.
- `merge(server)`: The operation that using the max function updates
  the state of the local counter.

The class `Cluster` is the one representing the network that all the
servers build. Its task in the program is to build each server,
populate it's list of servers and communicate with the frontend for
tasks like deleting a node or watching a video in a node (the idea is
that this class is like the load balancer or the router that matches
your location with the right server).

The main script is a [sanic
server](https://github.com/huge-success/sanic). I've choosen sanic
because is a flask like framework that can work asyncronously. I've
created a task with it that every 5 seconds performs the merge
operation for a certain server each time. Also sanic provides the API
endpoints for the web interface to operate on the program.

### Things that I changed

Firstly I implemented the system for just one video but the
generalization for a bigger number of videos was easy to implement.
For this reason each instance of `Server` doesn't assume that the number of videos
is 1 but to make easy the web interface I just made available one
video.

### About the questions

**What can happen when the user reloads the website? Can we synchronize the counter
not only across nodes but also across the nodes and the frontend?**

We can introduce the frontend as one more server and sync the counter
with it too. When the user reloads the website we can expect that the
program destroys the server from the list of servers.

**What happens if a node gets removed from the cluster? What happens if more nodes
get added to the cluster?**

If a server gets removed from the cluster we'll loose the counter
information corresponding to this node unless it syncronizes it's
information with the rest of nodes before being destroyed.  If a node
gets added to the cluster it's inmediatly known by the rest of servers
and after a certain period of time it'll retrive the up to date
information.

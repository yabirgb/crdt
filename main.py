import sys
import json

from sanic import Sanic
from sanic.response import json, text

from cluster import Cluster

# Initialize a virtual cluster of 10 servers
# containing the same 5 videos
cluster = Cluster(10, 1)

app = Sanic()

@app.route('/')
async def home(request):
    return text("Welcome to our video service!")

@app.route('/servers')
async def servers(request):
    return json(cluster.info())

@app.route('/watch/<server>')
async def watch(request, server):
    cluster.watch(int(server))
    return text(f"Now playing the only video on server #{server}")

if __name__ == '__main__':

    if len(sys.argv) > 1:
        app.run(host='127.0.0.1', port=int(sys.argv[1]), auto_reload=True)
    else:
        print("Not enought arguments")

import sys
import json
import asyncio

from sanic import Sanic
from sanic.response import json, text

from cluster import Cluster


"""
Things related to the cluster
"""

# Initialize a virtual cluster of 10 servers
# containing the same 5 videos
cluster = Cluster(10, 1)

async def sync_action():
    i = 0
    size = len(cluster.info())

    while True:
        await asyncio.sleep(5)
        cluster.sync(i)
        print(f"Synced {i}")
        i += 1
        i = i%size

"""
Things related to the API
"""

app = Sanic()

app.add_task(sync_action())


app.static('/js', './webUI/js')
app.static('/', './webUI/index.html')

@app.route('/servers')
async def servers(request):
    return json(cluster.info())

@app.route('/watch/<server>')
async def watch(request, server):
    cluster.watch(int(server))
    return text(f"Now playing the only video on server #{server}")

@app.route('/watch/<server>/<times>')
async def watch(request, server, times):
    cluster.watch(server, int(times))
    return json(f"Now playing the only video on server #{server}")




if __name__ == '__main__':

    if len(sys.argv) > 1:
        app.run(host='127.0.0.1', port=int(sys.argv[1]), auto_reload=True)
    else:
        print("Not enought arguments")

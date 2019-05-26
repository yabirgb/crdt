import random
from typing import List
from typing import Union
from uuid import uuid4

class Server:

    def __init__(self, videos: List[str]):

        self.id_ = str(uuid4())
        self.universe = {self.id_ : {}}
        self.alive = True

        # Initialize the videos with a default
        # number of views of 0
        for video in videos:
            self.universe[self.id_][video] = 0



    def info(self):
        data = {'videos':{}}
        for video in self.universe[self.id_]:
            data['videos'][video] = self.count(video)
        data['ident'] = self.id_
        data['alive'] = self.alive

        return data


    # Different functions used by the crdt
    
    def incr(self, id_:str) -> Union[bool, int]:
        """
        Increment the views of the video with id id_ by 1
        This is the update function of the crdt counter
        """

        if id_ in self.universe[self.id_].keys():
            self.universe[self.id_][id_] += 1
            return self.universe[self.id_][id_]
        else:
            return False

    def incr_by(self, id_:str, amount: int) -> Union[bool, int]:
        """
        Instead of just increment by one, we increment by 
        a certain amount
        """
        
        if id_ in self.universe[self.id_].keys() and amount > 0:
            self.universe[self.id_][id_] += amount
            return self.universe[self.id_][id_]
        else:
            return False

    def set_to(self, id_:str, amount:int) -> Union[bool, int]:
        """
        Fix the counter to a certain value
        """
        
        if id_ in self.universe[self.id_] and amount > 0:
            self.universe[self.id_][id_] = amount
            return self.universe[self.id_][id_]
        else:
            return False
        
    def total(self, id_:str) -> Union[bool,int]:

        if id_ in self.universe[self.id_].keys():
            return self.universe[self.id_][id_]
        else:
            return False

    def merge(self, server) -> None:

        for ident in server.universe:
            if not ident in self.universe:
                self.universe[ident] = {}
                
            for video in server.universe[ident]:
                if video in self.universe[ident]:
                    own = self.universe[ident][video]
                else:
                    own = 0
                self.universe[ident][video] = max(own, server.universe[ident][video])

    def count(self, video:str) -> int:
        total = 0
        for server in self.universe:
            total += self.universe[server][video]

        return total
                    

class Cluster:

    def __init__(self, amount: int, videos:int = 10):
        """
        amount: The number of replicas of our server
        """

        # A list with all our servers
        self.cluster = list()

        self.videos = list(map(str, [uuid4() for x in range(videos)]))
        
        for i in range(amount):
            self.cluster.append(Server(self.videos))
        

    def info(self):

        data = dict()
        for index, server in enumerate(self.cluster):
            data[f'server_{index}'] = server.info()

        return data

    def sync(self, i):
        if self.cluster[i].alive:
            for pos in random.sample(range(0, len(self.cluster)),5):
                server = self.cluster[pos]
                if server.alive:
                    self.cluster[i].merge(server)
            

    def list_of_videos(self) -> List[str]:
        return self.videos

    def watch(self, server_id: str, times:Union[int, None] = None) -> None:
        """
        server_id is in the range 0 <= server_id < amount
        being it the positional id of the server in the cluster list
        """

        for server in self.cluster:
            if server_id == server.id_:
                if times:
                    server.incr_by(self.videos[0], times)
                else:
                    server.incr(self.videos[0])
                break

    def toggle(self, id_):
        for server in self.cluster:
            if server.id_ == id_:
                server.alive = not server.alive
                break

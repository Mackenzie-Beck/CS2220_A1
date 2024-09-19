class ActorGraph:

    # class representing the graph of actors
    # Stores and maintains a dictionary of actors, these are the nodes of our graph


    def __init__(self):
        # dictionary of actors
        # key: actorID, value: actor object
        self.actors = {}


    # This method adds an actor to the graph
    def add_actor(self, actor):
        self.actors[actor.actorID] = actor
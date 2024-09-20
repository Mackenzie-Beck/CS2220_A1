class Actor:

# class representing each individual actor





    #actorShows s a dictionary of show’s IDs (where the actor participated). Initially – 
    #   empty. It stores TV show data as follows: keys are show’s IDs, values – TV shows 
    #   dates (year of premiere).

    def __init__(self, actorID, actorName, actorBirthday, actorCharacterName, actorShows):
        self.actorID = actorID
        self.actorName = actorName
        self.actorBirthday = actorBirthday
        self.actorCharacterName = actorCharacterName
        self.actorShows = actorShows
        # dictionary of actorID : weight this dicitonary will be the edges of our graph
        self.actor_relations = {} 


# This fills the actors ActorShows dictionary with the relevant show data
    def fill_actor_shows(self, show_data):
        self.actorShows[show_data['id']] = show_data['premiere_year']

#  This method creates the actor relations dictionary
#  By taking self and the actor_graph 
#  weight of relationships between actors is calculated as follwos:
#  If actors are in the same show, weight is 1
#  If actors are in more than one show together, the weight is the number of shows they have together
    def create_actor_relations(self, actor_graph):
        for show in self.actorShows.keys():
            for actor in actor_graph.actors.values():
                for show1 in actor.actorShows.keys():
                    if show1 == show:
                        if actor.actorID not in self.actor_relations:
                            self.actor_relations[actor.actorID] = 1
                        else:
                            self.actor_relations[actor.actorID] += 1


# This method calculates the influence of an actor
# influence is the sum of the weights of all the relationships of an actor
    def calculate_influence(self):
        #total_weight = sum(self.actor_relations.values())
        #self.influence = total_weight / len(self.actor_relations)
        self.influence = sum(self.actor_relations.values())


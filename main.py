import json
import os
import io
from Actor import Actor
from ActorGraph import ActorGraph
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx


def plot_actor_influence(actor_graph):
    # Create a list of tuples containing actor names and their influence
    actor_influence = [(actor.actorName, actor.influence) for actor in actor_graph.actors.values()]
    # Sort the list by influence in descending order and take top 5 actors
    top_5_actors = sorted(actor_influence, key=lambda x: x[1], reverse=True)[:5]

    # Create a DataFrame from top 5 actors
    df = pd.DataFrame(top_5_actors, columns=['Actor', 'Influence'])

    # Create the bar plot
    plt.figure(figsize=(12, 6))  # Adjusted figure size for 5 actors
    sns.barplot(x='Actor', y='Influence', data=df)
    plt.title('Top 5 Actors by Influence')
    plt.xticks(rotation=45, ha='right')  # Adjusted rotation for better readability
    plt.tight_layout()
    plt.show()

file_name = "tvshows.json"



# this will locate akk tge JSIB files inside the main directory and sub directories

json_files = [os.path.join(root,name)
              for root, dirs, files in os.walk(os.getcwd())
              for name in files
              if name.endswith('.json')]

#print("number of json files ready to be processed: ", len(json_files))


def main():
    with open(json_files[0]) as f:
        json_data = json.load(f)

   # print(f"Type of json_data: {type(json_data)}")
   # print(f"Length of json_data: {len(json_data)}")
   # print(f"First item in json_data: {json_data[0] if json_data else 'Empty'}")

    data_shows = []

    for show in json_data[:8]:

        data_show = {}
        data_show['id'] = show['id']
        data_show['name'] = show['name']
        data_show['cast'] = show['cast']
        data_show['genres'] = show['genres']
        data_shows.append(data_show)

    # Create an ActorGraph instance
    actor_graph = ActorGraph()

    # Extract actors from data_shows and create Actor objects
    for show in data_shows:
        show_id = show['id']
        premiere_year = show.get('premiere_year', None)  # Assuming premiere_year is in the show data
        
        for cast_member in show['cast']:
            actor_id = cast_member['person']['id']  # Changed this line
            actor_name = cast_member['person']['name']  # Also change this line
            actor_birthday = cast_member['person'].get('birthday', None)  # And this line
            actor_character_name = cast_member.get('character', None)
            
            # Check if the actor already exists in the graph
            if actor_id not in actor_graph.actors:
                # Create a new Actor object
                new_actor = Actor(actor_id, actor_name, actor_birthday, actor_character_name, {})
                # Add the actor to the graph
                actor_graph.add_actor(new_actor)
                
            # Add the show to the actor's shows
            actor_graph.actors[actor_id].fill_actor_shows({'id': show_id, 'premiere_year': premiere_year})

    # Create relationships between actors
    for actor in actor_graph.actors.values():
        actor.create_actor_relations(actor_graph)

    # Calculate influence for each actor
    for actor in actor_graph.actors.values():
        actor.calculate_influence()

    plot_actor_influence(actor_graph)

    # Print the actors in the graph
    for actor in actor_graph.actors.values():
        print(f"Actor ID: {actor.actorID}, Name: {actor.actorName}, Influence: {actor.influence}")

if __name__ == "__main__":
    main()





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


def visualize_actor_network(actor_graph):
    # Create a graph from the actor relationships
    G = nx.Graph()


    # Rank actors by influence and select top 20
    # can change the number of actors to be displayed
    # by changing the [:20]
    top_actors = sorted(actor_graph.actors.values(), key=lambda x: x.influence, reverse=True)[:77]
    
    # Add nodes for top actors
    for actor in top_actors:
        G.add_node(actor.actorID, name=actor.actorName, influence=actor.influence)
    
    # Add edges between top actors
    for i, actor in enumerate(top_actors):
        for other_actor in top_actors[i+1:]:
            if other_actor.actorID in actor.actor_relations:
                weight = actor.actor_relations[other_actor.actorID]
                G.add_edge(actor.actorID, other_actor.actorID, weight=weight)

    # Calculate node positions
    pos = nx.spring_layout(G, k=0.75, iterations=150)


    # Create figure and axes
    fig, (ax_main, ax_cbar1, ax_cbar2) = plt.subplots(1, 3, figsize=(16, 10), 
                                                      gridspec_kw={'width_ratios': [20, 1, 1]})
    fig.suptitle('Actor Network Visualization', fontsize=16)
    
    # Increase the k parameter to increase distance between nodes
    pos = nx.spring_layout(G, k=0.75, iterations=150)
    
    # Correctly access node attributes
    node_size = [3000 * G.nodes[node]['influence'] for node in G.nodes()]
    node_color = [G.nodes[node]['influence'] for node in G.nodes()]
    
    # Calculate edge widths based on influence
    edge_widths = [0.1 + 0.9 * min(G.nodes[u]['influence'], G.nodes[v]['influence']) / max(node['influence'] for node in G.nodes.values()) for u, v in G.edges()]
    
    # Calculate edge colors based on average influence of connected nodes
    edge_colors = ['#%02x%02x%02x' % (int(255 * (1 - avg)), int(255 * avg), 0) for avg in 
                   [(G.nodes[u]['influence'] + G.nodes[v]['influence']) / (2 * max(node['influence'] for node in G.nodes.values())) for u, v in G.edges()]]
    
    # Draw the network on the main axes
    nx.draw(G, pos, ax=ax_main, with_labels=True, node_size=1000, node_color=node_color, alpha=0.7, 
            edge_color=edge_colors, width=edge_widths, font_size=8, labels={node: G.nodes[node]['name'] for node in G.nodes()})

    # Create a ScalarMappable object for node colors
    # This object maps scalar data to colors
    sm = plt.cm.ScalarMappable(cmap='coolwarm', norm=plt.Normalize(vmin=min(node_color), vmax=max(node_color)))
    
    # Set the array for the ScalarMappable (required for some versions of matplotlib)
    sm.set_array([])
    
    # Create a colorbar for node colors using the ScalarMappable
    # The colorbar is added to the figure using the specified axes (ax_cbar1)
    cbar1 = fig.colorbar(sm, cax=ax_cbar1)
    
    # Set the label for the node color colorbar
    cbar1.set_label('Actor Influence')

    # Add color bar for edge colors
   
    # Create a ScalarMappable object for edge colors
    # Using 'RdYlGn' colormap (Red-Yellow-Green) and normalizing values between 0 and 1
    sm_edges = plt.cm.ScalarMappable(cmap='RdYlGn', norm=plt.Normalize(vmin=0, vmax=1))
    
    # Set the array for the ScalarMappable (required for some versions of matplotlib)
    sm_edges.set_array([])
    
    # Create a colorbar for edge colors using the ScalarMappable
    cbar2 = fig.colorbar(sm_edges, cax=ax_cbar2)
    
    # Set the label for the edge color colorbar
    cbar2.set_label('Average Connected Actor Influence')

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




    # Plot and visualize the actor network
    #plot_actor_influence(actor_graph)
    visualize_actor_network(actor_graph)

    # Print the actors in the graph
    for actor in actor_graph.actors.values():
       print(f"Actor ID: {actor.actorID}, Name: {actor.actorName}, Influence: {actor.influence}")

if __name__ == "__main__":
    main()





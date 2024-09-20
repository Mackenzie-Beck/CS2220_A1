# Actor Network Analysis

This project analyzes and visualizes actor relationships based on their appearances in TV shows.

## Features

- Parses JSON data of TV shows and their casts
- Builds a graph of actor relationships
- Calculates actor influence based on their connections
- Visualizes the actor network using NetworkX and Matplotlib
- Displays top actors by influence using a bar plot

## Files

- `main.py`: Main script to run the analysis and visualization
- `Actor.py`: Defines the Actor class
- `ActorGraph.py`: Defines the ActorGraph class
- `test_Actor.py`: Unit tests for the Actor class

## Dependencies

- json
- os
- io
- seaborn
- pandas
- matplotlib
- networkx

## Usage

1. Ensure all dependencies are installed
2. Place your TV show JSON data file(s) in the project directory or subdirectories
3. Run `main.py`

## Classes

### Actor

Represents an individual actor with properties such as ID, name, birthday, character name, and shows they've appeared in.

### ActorGraph

Represents the entire network of actors, storing Actor objects and their relationships.

## Visualization

The project generates two types of visualizations:

1. A bar plot of the top 5 actors by influence
2. A network graph showing connections between actors, with node size and color representing influence

## Testing

Run `test_Actor.py` to execute unit tests for the Actor class.

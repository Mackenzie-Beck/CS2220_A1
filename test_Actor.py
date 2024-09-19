import unittest
from Actor import Actor

class TestActor(unittest.TestCase):
    def setUp(self):
        self.actor = Actor("123", "John Doe", "1990-01-01", "Character Name", {})

    def test_init(self):
        self.assertEqual(self.actor.actorID, "123")
        self.assertEqual(self.actor.actorName, "John Doe")
        self.assertEqual(self.actor.actorBirthday, "1990-01-01")
        self.assertEqual(self.actor.actorCharacterName, "Character Name")
        self.assertEqual(self.actor.actorShows, {})
        self.assertEqual(self.actor.actor_relations, {})

    def test_fill_actor_shows(self):
        show_data = {"id": "show1", "premiere_year": 2020}
        self.actor.fill_actor_shows(show_data)
        self.assertEqual(self.actor.actorShows, {"show1": 2020})

    def test_create_actor_relations(self):
        # Create a mock ActorGraph
        class MockActorGraph:
            def __init__(self):
                self.actors = {"456": Actor("456", "Jane Doe", "1995-05-05", "Another Character", {"show1": 2020})}

        self.actor.actorShows = {"show1": 2020}
        mock_graph = MockActorGraph()
        self.actor.create_actor_relations(mock_graph)
        self.assertEqual(self.actor.actor_relations, {"456": 1})

    def test_calculate_influence(self):
        self.actor.actor_relations = {"456": 2, "789": 1}
        self.actor.calculate_influence()
        self.assertEqual(self.actor.influence, 1.5)

if __name__ == '__main__':
    unittest.main()

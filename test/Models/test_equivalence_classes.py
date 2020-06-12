import unittest
from src.models.equivalence_classes import EquivalenceClasses
from src.models.node import Node


class TestEquivalenceClasses(unittest.TestCase):
    def setUp(self):
        self.equivalence_classes = EquivalenceClasses()

    def test_cannot_add_duplicate(self):
        self.equivalence_classes.add(1)
        with self.assertRaises(ValueError):
            self.equivalence_classes.add(1)

    def test_can_find_added_identifiers(self):
        self.equivalence_classes.add(1)
        self.equivalence_classes.add(2)
        self.assertEqual(0, self.equivalence_classes.find(1))
        self.assertEqual(1, self.equivalence_classes.find(2))

    def test_union_of_missing_identifier_raises_error(self):
        self.equivalence_classes.add(1)
        with self.assertRaises(ValueError):
            self.equivalence_classes.union(1, 2)

    def test_can_union_two_classes(self):
        self.equivalence_classes.add(1)
        self.equivalence_classes.add(2)
        self.equivalence_classes.union(1, 2)
        self.assertEqual(
            self.equivalence_classes.find(1), self.equivalence_classes.find(2)
        )

    def test_can_track_number_unique_classes(self):
        self.assertEqual(0, self.equivalence_classes.count)
        self.equivalence_classes.add(1)
        self.assertEqual(1, self.equivalence_classes.count)
        self.equivalence_classes.add(2)
        self.assertEqual(2, self.equivalence_classes.count)
        self.equivalence_classes.union(1, 2)
        self.assertEqual(1, self.equivalence_classes.count)

    def test_can_check_if_item_inside(self):
        self.assertFalse(1 in self.equivalence_classes)
        self.equivalence_classes.add(1)
        self.assertTrue(1 in self.equivalence_classes)

    def test_can_retrieve_node_for_identifier(self):
        self.equivalence_classes.add(1)
        node = self.equivalence_classes.get_node(1)
        self.assertIsInstance(node, Node)
        self.assertEqual(1, node.identifier)

    def test_get_node_errors_if_untracked(self):
        with self.assertRaises(ValueError):
            self.equivalence_classes.get_node(1)

    def test_connect_unions_identifiers(self):
        self.equivalence_classes.add(1)
        self.equivalence_classes.add(2)
        self.equivalence_classes.connect(1, 2)
        self.assertEqual(
            self.equivalence_classes.find(1), self.equivalence_classes.find(2)
        )

    def test_connect_errors_with_untracked_identifer(self):
        self.equivalence_classes.add(1)
        with self.assertRaises(ValueError):
            self.equivalence_classes.connect(1, 2)
        with self.assertRaises(ValueError):
            self.equivalence_classes.connect(2, 1)

    def test_connect_adds_destination_to_source_connected_nodes(self):
        self.equivalence_classes.add(1)
        self.equivalence_classes.add(2)
        self.equivalence_classes.connect(1, 2)
        source_node = self.equivalence_classes.get_node(1)
        self.assertIn(Node(2), source_node.connected_nodes)

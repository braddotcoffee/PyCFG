import unittest
from src.models.node import Node


class TestNode(unittest.TestCase):
    def test_node_equivalence(self):
        self.assertEqual(Node(1), Node(1))
        self.assertNotEqual(Node(1), Node(2))
        self.assertNotEqual(2, Node(2))

    def test_node_is_hashable(self):
        test_set = set()
        test_set.add(Node(1))
        self.assertIn(Node(1), test_set)

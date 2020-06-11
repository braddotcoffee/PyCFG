import unittest
from src.models.equivalence_classes import EquivalenceClasses


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

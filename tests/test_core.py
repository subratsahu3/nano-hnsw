import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from nano_hnsw.core import NanoVectorIndex


class TestNanoVectorIndex(unittest.TestCase):
    def setUp(self):
        self.index = NanoVectorIndex(dim=3)

    def test_insert_and_exact_match(self):
        self.index.insert([1.0, 0.0, 0.0])
        self.index.insert([0.0, 1.0, 0.0])
        self.index.insert([0.0, 0.0, 1.0])

        results = self.index.search([1.0, 0.0, 0.0], top_k=1)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0], 0)
        self.assertAlmostEqual(results[0][1], 0.0, places=5)

    def test_nearest_neighbor_ranking(self):
        # Insert target and near target
        self.index.insert([1.0, 0.0, 0.0])
        self.index.insert([0.9, 0.1, 0.0])
        self.index.insert([0.0, 1.0, 0.0])

        results = self.index.search([0.95, 0.05, 0.0], top_k=2)
        top_ids = [r[0] for r in results]
        self.assertIn(0, top_ids)
        self.assertIn(1, top_ids)

    def test_dimension_mismatch_raises(self):
        with self.assertRaises(ValueError):
            self.index.insert([1.0, 0.0])
        with self.assertRaises(ValueError):
            self.index.search([1.0, 0.0, 0.0, 0.0])


if __name__ == "__main__":
    unittest.main()

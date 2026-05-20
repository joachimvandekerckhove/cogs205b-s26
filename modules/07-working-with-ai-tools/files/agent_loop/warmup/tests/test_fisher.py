import unittest
import math
from fisher import fisher_z_transform


class TestFisherZ(unittest.TestCase):
    def test_zero(self):
        self.assertAlmostEqual(fisher_z_transform(0), 0.0, places=10)

    def test_known_value(self):
        self.assertAlmostEqual(fisher_z_transform(0.5), math.atanh(0.5), places=10)

    def test_negative(self):
        self.assertLess(fisher_z_transform(-0.3), 0)

    def test_boundary_raises(self):
        with self.assertRaises(ValueError):
            fisher_z_transform(1.0)

    def test_negative_boundary_raises(self):
        with self.assertRaises(ValueError):
            fisher_z_transform(-1.0)


if __name__ == "__main__":
    unittest.main()

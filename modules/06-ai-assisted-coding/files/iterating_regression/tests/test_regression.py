import unittest
import numpy as np
from regression import fit_regression


class TestFitRegression(unittest.TestCase):
    def setUp(self):
        self.X = np.array([[0], [1], [2], [3]], dtype=float)
        self.y = np.array([1, 3, 5, 7], dtype=float)

    def test_slope(self):
        beta = fit_regression(self.X, self.y)
        np.testing.assert_allclose(beta[1], 2.0, atol=1e-8)

    def test_intercept(self):
        beta = fit_regression(self.X, self.y)
        np.testing.assert_allclose(beta[0], 1.0, atol=1e-8)

    def test_shape(self):
        beta = fit_regression(self.X, self.y)
        self.assertEqual(len(beta), 2)

    def test_add_intercept_false(self):
        X2 = np.hstack([np.ones((4, 1)), self.X])
        beta = fit_regression(X2, self.y, add_intercept=False)
        np.testing.assert_allclose(beta, [1.0, 2.0], atol=1e-8)


if __name__ == "__main__":
    unittest.main()

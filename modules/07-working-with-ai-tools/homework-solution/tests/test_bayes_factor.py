import unittest

from bayes_factor import BayesFactor


class TestBayesFactor(unittest.TestCase):
    def setUp(self):
        self.bf_chance = BayesFactor(2, 1)
        self.bf_success = BayesFactor(2, 2)
        self.bf_fail = BayesFactor(2, 0)
        self.bf_big_n = BayesFactor(1000000, 0)
        self.bf_zeros = BayesFactor(0, 0)

    # Input and state validation
    def test_initialization(self):
        self.assertEqual(self.bf_chance.n, 2)
        self.assertEqual(self.bf_chance.k, 1)

    def test_invalid_n_type(self):
        with self.assertRaises(TypeError) as exception_context:
            BayesFactor(7.2, 1)
        self.assertEqual(
            str(exception_context.exception),
            "n must be an integer",
        )
        with self.assertRaises(TypeError):
            BayesFactor(True, 1)

    def test_invalid_k_type(self):
        with self.assertRaises(TypeError) as exception_context:
            BayesFactor(7, 1.2)
        self.assertEqual(
            str(exception_context.exception),
            "k must be an integer",
        )
        with self.assertRaises(TypeError):
            BayesFactor(1, True)

    def test_invalid_n_range(self):
        with self.assertRaises(ValueError) as exception_context:
            BayesFactor(-1, 7)
        self.assertEqual(
            str(exception_context.exception),
            "n and k cannot be negative",
        )

    def test_invalid_k_range(self):
        with self.assertRaises(ValueError) as exception_context:
            BayesFactor(1, -7)
        self.assertEqual(
            str(exception_context.exception),
            "n and k cannot be negative",
        )

    def test_k_larger_than_n(self):
        with self.assertRaises(ValueError) as exception_context:
            BayesFactor(5, 10)
        self.assertEqual(
            str(exception_context.exception),
            "k cannot be larger than n",
        )

    # API behavior and return contracts
    def test_methods_are_callable(self):
        self.assertTrue(callable(self.bf_chance.likelihood))
        self.assertTrue(callable(self.bf_chance.evidence_slab))
        self.assertTrue(callable(self.bf_chance.evidence_spike))
        self.assertTrue(callable(self.bf_chance.bayes_factor))

    def test_likelihood_output(self):
        self.assertAlmostEqual(self.bf_chance.likelihood(0.5), 0.5)
        self.assertIsInstance(self.bf_chance.likelihood(0.5), float)

    def test_evidence_slab_output(self):
        self.assertAlmostEqual(self.bf_chance.evidence_slab(), 1 / 3)
        self.assertIsInstance(self.bf_chance.evidence_slab(), float)

    def test_evidence_spike_output(self):
        # Etz ROPE U(0.47, 0.53) gives ~0.4994 for n=2, k=1 (not exact 0.5).
        self.assertAlmostEqual(self.bf_chance.evidence_spike(), 1 / 2, places=2)
        self.assertIsInstance(self.bf_chance.evidence_spike(), float)

    def test_bayes_factor_output(self):
        self.assertAlmostEqual(self.bf_chance.bayes_factor(), 3 / 2, places=2)
        self.assertIsInstance(self.bf_chance.bayes_factor(), float)

    # Method validation/edge cases
    def test_likelihood_theta_invalid_type(self):
        with self.assertRaises(TypeError) as exception_context:
            self.bf_chance.likelihood("0.5")
        self.assertEqual(
            str(exception_context.exception),
            "Theta must be an integer or float",
        )
        with self.assertRaises(TypeError):
            self.bf_chance.likelihood(True)

    def test_likelihood_theta_invalid_range(self):
        with self.assertRaises(ValueError) as exception_context:
            self.bf_chance.likelihood(-1)
        self.assertEqual(
            str(exception_context.exception),
            "Theta must be within the range [0, 1]",
        )
        with self.assertRaises(ValueError):
            self.bf_chance.likelihood(1.1)

    def test_likelihood_at_theta_boundaries(self):
        self.assertEqual(self.bf_fail.likelihood(0), 1)
        self.assertEqual(self.bf_success.likelihood(1), 1)

    def test_impossible_likelihood_at_theta_boundaries(self):
        self.assertEqual(self.bf_success.likelihood(0), 0)
        self.assertEqual(self.bf_fail.likelihood(1), 0)

    def test_bayes_factor_zero_division(self):
        with self.assertRaises(ValueError) as exception_context:
            self.bf_big_n.bayes_factor()
        self.assertEqual(
            str(exception_context.exception),
            "Bayes Factor undefined; slab evidence ≈ 0",
        )

    def test_bayes_factor_same_prior(self):
        self.assertAlmostEqual(
            self.bf_zeros.evidence_spike(),
            self.bf_zeros.evidence_slab(),
        )
        self.assertAlmostEqual(self.bf_zeros.bayes_factor(), 1)

    def test_evidence_nonnegative(self):
        self.assertGreaterEqual(self.bf_chance.evidence_slab(), 0)
        self.assertGreaterEqual(self.bf_chance.evidence_spike(), 0)

    def test_spike_dominates_chance_case(self):
        self.assertGreater(
            self.bf_chance.evidence_spike(),
            self.bf_chance.evidence_slab(),
        )


if __name__ == "__main__":
    unittest.main()

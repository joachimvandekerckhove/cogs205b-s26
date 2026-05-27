import tempfile
import unittest
from pathlib import Path

from belief_polarization_abm import BeliefPolarizationABM, run_demo


class TestBeliefPolarizationABM(unittest.TestCase):
    def test_model_runs_and_tracks_bounds(self):
        model = BeliefPolarizationABM(n_agents=40, seed=11)
        history = model.run(n_steps=500, record_every=50)
        self.assertEqual(history.shape[1], 40)
        self.assertTrue((history >= -1.0).all())
        self.assertTrue((history <= 1.0).all())

    def test_demo_creates_figure_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "figures" / "abm"
            run_demo(
                output_dir=output_dir,
                n_agents=40,
                n_steps=1200,
                record_every=50,
                base_seed=13,
            )
            expected = [
                "belief_trajectories.png",
                "final_distribution.png",
                "polarization_over_time.png",
                "tolerance_sweep.png",
            ]
            for name in expected:
                self.assertTrue((output_dir / name).exists(), f"Missing figure: {name}")


if __name__ == "__main__":
    unittest.main()

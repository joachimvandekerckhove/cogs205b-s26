"""Belief polarization ABM with plotting utilities.

Run from command line:
    python belief_polarization_abm.py
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt


@dataclass
class RunSummary:
    final_polarization: float
    final_variance: float
    output_dir: Path


class Agent:
    """One agent with a continuous belief in [-1, 1]."""

    def __init__(self, belief: float) -> None:
        self.belief = float(belief)

    def interact_with(
        self,
        other: Agent,
        *,
        alpha: float,
        beta: float,
        tolerance: float,
    ) -> None:
        """Bounded-confidence update toward or away from a neighbor."""
        difference = other.belief - self.belief
        if abs(difference) < tolerance:
            self.belief += alpha * difference
        else:
            self.belief -= beta * difference
        self.belief = float(np.clip(self.belief, -1.0, 1.0))


class BeliefPolarizationABM:
    def __init__(
        self,
        n_agents: int = 100,
        alpha: float = 0.10,
        beta: float = 0.03,
        tolerance: float = 0.35,
        seed: int | None = None,
    ) -> None:
        self.n_agents = n_agents
        self.alpha = alpha
        self.beta = beta
        self.tolerance = tolerance
        self.rng = np.random.default_rng(seed)
        initial = self.rng.normal(loc=0.0, scale=0.25, size=n_agents)
        self.agents: list[Agent] = [
            Agent(float(np.clip(belief, -1.0, 1.0))) for belief in initial
        ]
        self.history = [self.beliefs_array()]

    def beliefs_array(self) -> np.ndarray:
        return np.array([agent.belief for agent in self.agents], dtype=float)

    def neighbors(self, i: int) -> list[int]:
        left = (i - 1) % self.n_agents
        right = (i + 1) % self.n_agents
        return [left, right]

    def step(self) -> None:
        i = int(self.rng.integers(self.n_agents))
        j = int(self.rng.choice(self.neighbors(i)))
        self.agents[i].interact_with(
            self.agents[j],
            alpha=self.alpha,
            beta=self.beta,
            tolerance=self.tolerance,
        )

    def run(self, n_steps: int = 10_000, record_every: int = 100) -> np.ndarray:
        for step in range(n_steps):
            self.step()
            if step % record_every == 0:
                self.history.append(self.beliefs_array())
        return np.array(self.history)

    def polarization(self) -> float:
        beliefs = self.beliefs_array()
        return float(np.mean(np.abs(beliefs)))

    def variance(self) -> float:
        return float(np.var(self.beliefs_array()))

    def extreme_proportion(self, threshold: float = 0.8) -> float:
        beliefs = self.beliefs_array()
        return float(np.mean(np.abs(beliefs) >= threshold))


def plot_trajectories(history: np.ndarray, output_path: Path, max_agents: int = 35) -> None:
    fig, ax = plt.subplots(figsize=(8, 4.5))
    n_agents = history.shape[1]
    n_plot = min(max_agents, n_agents)
    for idx in range(n_plot):
        ax.plot(history[:, idx], alpha=0.45, linewidth=1.0)
    ax.set_title("Belief trajectories over time")
    ax.set_xlabel("Recorded time index")
    ax.set_ylabel("Belief")
    ax.set_ylim(-1.05, 1.05)
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def plot_final_distribution(final_beliefs: np.ndarray, output_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.hist(final_beliefs, bins=24, range=(-1, 1), color="#3B528B", alpha=0.9)
    ax.set_title("Final belief distribution")
    ax.set_xlabel("Belief")
    ax.set_ylabel("Agent count")
    ax.set_xlim(-1.05, 1.05)
    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def plot_polarization_over_time(history: np.ndarray, output_path: Path) -> None:
    polarization_series = np.mean(np.abs(history), axis=1)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(polarization_series, color="#5EC962", linewidth=2.2)
    ax.set_title("Polarization over time")
    ax.set_xlabel("Recorded time index")
    ax.set_ylabel("Mean |belief|")
    ax.set_ylim(0, 1.0)
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def tolerance_sweep(
    tolerances: Iterable[float],
    seeds: Iterable[int],
    n_agents: int = 100,
    n_steps: int = 10_000,
    record_every: int = 100,
    alpha: float = 0.10,
    beta: float = 0.03,
) -> tuple[np.ndarray, np.ndarray]:
    tolerance_values = np.array(list(tolerances), dtype=float)
    mean_polarization = np.zeros_like(tolerance_values)

    seed_list = list(seeds)
    for idx, tau in enumerate(tolerance_values):
        per_seed = []
        for seed in seed_list:
            model = BeliefPolarizationABM(
                n_agents=n_agents,
                alpha=alpha,
                beta=beta,
                tolerance=float(tau),
                seed=int(seed),
            )
            model.run(n_steps=n_steps, record_every=record_every)
            per_seed.append(model.polarization())
        mean_polarization[idx] = float(np.mean(per_seed))
    return tolerance_values, mean_polarization


def plot_tolerance_sweep(
    tolerances: np.ndarray, mean_polarization: np.ndarray, output_path: Path
) -> None:
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(tolerances, mean_polarization, marker="o", color="#21918C", linewidth=2.0)
    ax.set_title("Final polarization by tolerance")
    ax.set_xlabel("Tolerance (tau)")
    ax.set_ylabel("Mean final polarization")
    ax.set_ylim(0, 1.0)
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def run_demo(
    output_dir: Path,
    n_agents: int = 120,
    n_steps: int = 12_000,
    record_every: int = 100,
    base_seed: int = 2026,
) -> RunSummary:
    output_dir.mkdir(parents=True, exist_ok=True)

    model = BeliefPolarizationABM(
        n_agents=n_agents,
        alpha=0.10,
        beta=0.03,
        tolerance=0.35,
        seed=base_seed,
    )
    history = model.run(n_steps=n_steps, record_every=record_every)

    plot_trajectories(history, output_dir / "belief_trajectories.png")
    plot_final_distribution(history[-1], output_dir / "final_distribution.png")
    plot_polarization_over_time(history, output_dir / "polarization_over_time.png")

    tolerances, means = tolerance_sweep(
        tolerances=np.linspace(0.10, 0.90, 9),
        seeds=range(10),
        n_agents=n_agents,
        n_steps=n_steps,
        record_every=record_every,
    )
    plot_tolerance_sweep(tolerances, means, output_dir / "tolerance_sweep.png")

    return RunSummary(
        final_polarization=model.polarization(),
        final_variance=model.variance(),
        output_dir=output_dir,
    )


def main() -> None:
    script_dir = Path(__file__).resolve().parent
    output_dir = script_dir / "figures" / "abm"
    summary = run_demo(output_dir=output_dir)
    print("Belief polarization ABM complete.")
    print(f"Final polarization: {summary.final_polarization:.4f}")
    print(f"Final variance: {summary.final_variance:.4f}")
    print(f"Figures saved to: {summary.output_dir}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Regenerate pv-p.png (prior on theta) and pv-d.png (predictive on k) for the HW spec."""

from __future__ import annotations

import numpy as np
from scipy.special import betainc, betaln, comb
import matplotlib.pyplot as plt

N = 25
K_OBS = 15
SPIKE_LO, SPIKE_HI = 0.47, 0.53
SPIKE_DENSITY = 1.0 / (SPIKE_HI - SPIKE_LO)


def predictive_slab(k: int) -> float:
    """Uniform(0,1) prior on theta -> P(k|n) = 1/(n+1)."""
    if k < 0 or k > N:
        return 0.0
    return 1.0 / (N + 1)


def predictive_spike(k: int) -> float:
    """Uniform(spike) prior density times Beta-binomial slice integral."""
    if k < 0 or k > N:
        return 0.0
    a, b = k + 1, N - k + 1
    reg = betainc(a, b, SPIKE_HI) - betainc(a, b, SPIKE_LO)
    beta_inc = np.exp(betaln(a, b))
    return SPIKE_DENSITY * comb(N, k, exact=True) * beta_inc * reg


def main() -> None:
    ks = np.arange(0, N + 1)
    p_slab = np.array([predictive_slab(int(k)) for k in ks])
    p_spike = np.array([predictive_spike(int(k)) for k in ks])
    assert np.isclose(p_slab.sum(), 1.0, atol=1e-9)
    assert np.isclose(p_spike.sum(), 1.0, atol=1e-9)

    # --- Prior in theta space (pv-p) ---
    fig, ax = plt.subplots(figsize=(5.5, 3.2), dpi=150)
    theta = np.linspace(0, 1, 500)
    ax.plot(theta, np.ones_like(theta), "k--", lw=1.8, label="slab prior")
    ax.fill_between(
        [SPIKE_LO, SPIKE_HI],
        [0, 0],
        [SPIKE_DENSITY, SPIKE_DENSITY],
        color="0.35",
        edgecolor="k",
        lw=1.2,
        label="spike prior",
    )
    ax.set_xlim(0, 1)
    ymax = max(1.05, SPIKE_DENSITY * 1.05)
    ax.set_ylim(0, ymax)
    ax.set_xlabel(r"value of parameter ($\theta$)")
    ax.set_ylabel("density")
    ax.legend(frameon=False, loc="upper right", fontsize=9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig("pv-p.png", bbox_inches="tight")
    plt.close(fig)

    # --- Predictive over k (pv-d); mark observed k ---
    prop = ks / N
    width = 0.9 / N
    fig, ax = plt.subplots(figsize=(6.0, 3.2), dpi=150)
    ax.bar(
        prop - width / 2,
        p_slab,
        width=width,
        align="edge",
        facecolor="#6baed6",
        edgecolor="0.2",
        linewidth=0.4,
        label=r"$\mathcal{H}_0$ slab predictive",
        alpha=0.75,
    )
    ax.bar(
        prop - width / 2,
        p_spike,
        width=width,
        align="edge",
        facecolor="#fb6a4a",
        edgecolor="0.2",
        linewidth=0.4,
        label=r"$\mathcal{H}_1$ spike predictive",
        alpha=0.55,
    )
    ax.axvline(K_OBS / N, color="0.15", ls="--", lw=1.2, label=rf"data: $k={K_OBS}$, $n={N}$")
    ax.set_xlim(-0.02, 1.02)
    ax.set_xlabel(r"success proportion $k/n$")
    ax.set_ylabel(r"$P(k \mid n=25,\,\mathcal{H}_i)$")
    ax.legend(frameon=False, loc="upper right", fontsize=8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig("pv-d.png", bbox_inches="tight")
    plt.close(fig)

    print("Wrote pv-p.png, pv-d.png")
    print("P(k=15|slab)=", predictive_slab(15), "P(k=15|spike)=", predictive_spike(15))


if __name__ == "__main__":
    main()

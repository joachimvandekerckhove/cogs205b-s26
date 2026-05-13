"""
Minimal signal-detection MCP server: one tool, ``d_prime``.

Computes *d′* (d-prime) from hit and false-alarm **counts** under the standard
equal-variance Gaussian SDT model:

  d′ = Φ⁻¹(H) − Φ⁻¹(F)

with *H* = hits / n_signal and *F* = false_alarms / n_noise (the empirical
rates from your counts—no adjustment), and Φ⁻¹ the standard normal quantile
function (``statistics.NormalDist``). If *H* or *F* is exactly 0 or 1,
*d′* is not finite; the tool raises ``ValueError`` instead of altering rates.

Uses the official Model Context Protocol Python SDK (FastMCP).  Default
transport is **stdio**.

Run (after installing dependencies; see README)::

    python sdt_server.py

Stdio is the MCP control channel; use :mod:`client_demo` or an IDE host to
exercise the server.
"""

from __future__ import annotations

from statistics import NormalDist

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Signal detection demo")


@mcp.tool()
def d_prime(hits: int, false_alarms: int, n_signal: int, n_noise: int) -> float:
    """
    Equal-variance Gaussian SDT sensitivity *d′* from outcome counts.

    Args:
        hits: Correct responses to signal trials (0 ≤ hits ≤ n_signal).
        false_alarms: Incorrect “signal” responses on noise trials (0 ≤ false_alarms ≤ n_noise).
        n_signal: Number of signal trials (must be positive).
        n_noise: Number of noise trials (must be positive).

    Raises:
        ValueError: Invalid counts, or a hit / false-alarm rate of exactly 0 or 1.
    """
    if n_signal <= 0 or n_noise <= 0:
        raise ValueError("n_signal and n_noise must be positive.")
    if hits < 0 or false_alarms < 0:
        raise ValueError("hits and false_alarms must be non-negative.")
    if hits > n_signal:
        raise ValueError("hits cannot exceed n_signal.")
    if false_alarms > n_noise:
        raise ValueError("false_alarms cannot exceed n_noise.")

    if hits in (0, n_signal) or false_alarms in (0, n_noise):
        raise ValueError(
            "Hit rate and false-alarm rate must be strictly between 0 and 1 "
            "(need 0 < hits < n_signal and 0 < false_alarms < n_noise). "
            "Perfect or chance-only performance has no finite d′ under z-transform SDT."
        )

    hit_rate = hits / n_signal
    fa_rate = false_alarms / n_noise

    z = NormalDist()
    return z.inv_cdf(hit_rate) - z.inv_cdf(fa_rate)


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()

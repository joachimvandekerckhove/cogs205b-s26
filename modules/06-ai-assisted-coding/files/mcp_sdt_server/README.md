# Minimal signal-detection MCP server (`d_prime`)

Reference implementation for the **worked MCP example** in [062-ai-coding-landscape.md](../../062-ai-coding-landscape.md): one tool **`d_prime`** that computes sensitivity *d′* from hit and false-alarm counts (equal-variance Gaussian SDT), using the official [Model Context Protocol Python SDK](https://github.com/modelcontextprotocol/python-sdk).

## Layout

| File | Role |
|------|------|
| [`sdt_server.py`](./sdt_server.py) | MCP server (stdio transport) |
| [`client_demo.py`](./client_demo.py) | Local smoke test: list tools, call `d_prime` |
| [`requirements.txt`](./requirements.txt) | Pins the `mcp` dependency |

## Setup

From this directory:

```bash
 python3 -m venv .venv
 source .venv/bin/activate   # Windows: .venv\Scripts\activate
 pip install -r requirements.txt
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv venv
uv pip install -r requirements.txt
```

## Run the server

The server speaks MCP on **stdin/stdout**. A host process connects to it; you do not normally run it alone for human-readable output.

```bash
python sdt_server.py
```

## Smoke test

```bash
python client_demo.py
```

You should see `tools: ['d_prime']` and structured output with *d′* for 7 hits out of 10 signal trials and 2 false alarms out of 10 noise trials.

## Tool contract

- **Name:** `d_prime`
- **Arguments:** `hits`, `false_alarms`, `n_signal`, `n_noise` (non-negative integers; `hits ≤ n_signal`, `false_alarms ≤ n_noise`; `n_signal`, `n_noise` positive). For a **finite** *d′*, also require `0 < hits < n_signal` and `0 < false_alarms < n_noise` (empirical hit and FA rates must not be exactly 0 or 1).
- **Returns:** *d′* = Φ⁻¹(*H*) − Φ⁻¹(*F*) for empirical *H* = hits / n_signal and *F* = false_alarms / n_noise (no continuity correction). If either rate is exactly 0 or 1, the tool raises ``ValueError`` (finite *d′* would require changing or extending the data).

## Cursor / MCP host (optional)

Point your MCP config at this server using your venv’s `python` and [`sdt_server.py`](./sdt_server.py). See [Cursor MCP documentation](https://cursor.com/docs/context/mcp).

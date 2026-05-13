"""
Smoke-test :mod:`sdt_server` over stdio.

Run from this directory with the same environment that has ``mcp`` installed::

    python client_demo.py

Spawns ``sdt_server.py``, lists tools, and calls ``d_prime`` with a small
example (7 hits / 10 signal, 2 false alarms / 10 noise).

**What this script demonstrates (MCP in one file):**

1. The **host** (this program) starts an MCP **server** as a child process.
2. Host and server talk over **stdio**: they encode MCP messages on the
   subprocess's standard input and output (no network port needed for local demos).
3. The host performs a short **handshake** (``initialize``), **discovers** which
   tools exist (``list_tools``), then **invokes** one tool (``call_tool``) and
   reads the **result** (human-readable text plus optional structured data).
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from statistics import NormalDist

from mcp import ClientSession, types
from mcp.client.stdio import StdioServerParameters, stdio_client

_SERVER_DIR = Path(__file__).resolve().parent
_SERVER_SCRIPT = _SERVER_DIR / "sdt_server.py"


async def main() -> None:
    if not _SERVER_SCRIPT.is_file():
        sys.exit(f"Missing server script: {_SERVER_SCRIPT}")

    # Tell the MCP library how to launch the server: same Python, server script,
    # working directory so imports and relative paths behave predictably.
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(_SERVER_SCRIPT)],
        cwd=str(_SERVER_DIR),
    )

    # Toy SDT outcome table: 7 hits in 10 signal trials, 2 false alarms in 10 noise trials.
    hits, false_alarms, n_signal, n_noise = 7, 2, 10, 10

    # Same formula as the server: empirical H, F only (no nudging of rates).
    # Degenerate 0 / 1 rates are rejected by the tool with ValueError.
    h = hits / n_signal
    f = false_alarms / n_noise
    expected = NormalDist().inv_cdf(h) - NormalDist().inv_cdf(f)

    # stdio_client starts the subprocess and yields async read/write streams.
    # ClientSession wraps those streams in the MCP request/response API.
    # asyncio: the official MCP client exposes concurrency-friendly async methods.
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Protocol step: negotiate capabilities and protocol version with the server.
            await session.initialize()

            # Discovery: ask which tools exist (names, descriptions, JSON Schemas for args).
            tools = await session.list_tools()
            names = [t.name for t in tools.tools]
            print("tools:", names)
            assert "d_prime" in names, f"expected tool 'd_prime', got {names!r}"

            # Invocation: name must match a listed tool; the dict keys match the tool's parameters.
            result = await session.call_tool(
                "d_prime",
                {
                    "hits": hits,
                    "false_alarms": false_alarms,
                    "n_signal": n_signal,
                    "n_noise": n_noise,
                },
            )
            # Tool results can include several "content blocks"; here we only show the first.
            block = result.content[0]
            if isinstance(block, types.TextContent):
                print("d_prime tool text content:", repr(block.text))
            # FastMCP also returns structured JSON (easy for programs to parse).
            if result.structuredContent is not None:
                got = result.structuredContent["result"]
                print("d_prime structured:", result.structuredContent)
                assert abs(float(got) - expected) < 1e-9, (got, expected)


if __name__ == "__main__":
    asyncio.run(main())

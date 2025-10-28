"""Minimal python-sdk tool wiring for xfoil-mcp."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from xfoil_mcp.tool import build_tool

app = FastMCP("xfoil-mcp", "XFOIL polar analysis")
build_tool(app)


if __name__ == "__main__":
    # Example: echo a simple request into STDIN when running via `uv run mcp dev ...`
    # {
    #   "tool": "xfoil-mcp.polar",
    #   "arguments": {
    #     "airfoil_name": "naca0012",
    #     "airfoil_data": "0.0 0.0\n1.0 0.0\n...",
    #     "alphas": [0.0, 2.0, 4.0],
    #     "reynolds": 1200000,
    #     "mach": 0.0,
    #     "iterations": 200
    #   }
    # }
    app.run()

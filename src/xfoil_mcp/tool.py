"""Helper for wiring XFOIL into python-sdk MCP servers."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from .core import compute_polar
from .models import PolarRequest, PolarResponse


def build_tool(app: FastMCP) -> None:
    """Register XFOIL polar computation tooling on an MCP server."""

    @app.tool(
        name="xfoil.compute_polar",
        description=(
            "Run XFOIL for an airfoil at specified Reynolds angle of attack sweep. "
            "Input airfoil coordinates or NACA code plus sweep parameters. "
            "Returns lift/drag polar tables and solver metadata."
        ),
        meta={"version": "0.1.1", "categories": ["aero", "analysis"]},
    )
    def polar(request: PolarRequest) -> PolarResponse:
        return compute_polar(request)


__all__ = ["build_tool"]

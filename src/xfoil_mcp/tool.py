"""Helper for wiring XFOIL into python-sdk MCP servers."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from .core import compute_polar
from .models import PolarRequest, PolarResponse


def build_tool(app: FastMCP) -> None:
    """Register the polar analysis tool on the provided MCP app."""

    @app.tool()
    def polar(request: PolarRequest) -> PolarResponse:  # type: ignore[valid-type]
        return compute_polar(request)


__all__ = ["build_tool"]

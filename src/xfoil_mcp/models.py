"""Typed request/response models for XFOIL MCP calls."""

from __future__ import annotations

from pydantic import BaseModel, Field


class PolarRequest(BaseModel):
    """Parameters required to run an XFOIL polar sweep."""

    airfoil_name: str = Field(..., description="Identifier used when writing temporary files")
    airfoil_data: str = Field(..., description="Airfoil coordinate data in XFOIL DAT format")
    alphas: list[float] = Field(..., description="Angles of attack to analyse")
    reynolds: float = Field(..., gt=0.0, description="Reynolds number")
    mach: float = Field(0.0, ge=0.0, description="Mach number")
    iterations: int = Field(200, ge=10, le=10000, description="Maximum solver iterations")


class PolarResponse(BaseModel):
    """CSV payload returned by `compute_polar`."""

    csv: str = Field(..., description="CSV text containing XFOIL polar data")

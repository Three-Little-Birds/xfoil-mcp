"""Factory for the XFOIL FastAPI service."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException

from .core import XFOIL_BIN, compute_polar
from .models import PolarRequest, PolarResponse


def create_app() -> FastAPI:
    app = FastAPI(
        title="XFOIL MCP Service",
        version="0.1.0",
        description="Run XFOIL polar analyses and return CSV-formatted results.",
    )

    @app.post("/polar", response_model=PolarResponse)
    def run_polar(request: PolarRequest) -> PolarResponse:
        try:
            return compute_polar(request)
        except RuntimeError as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "binary": XFOIL_BIN, "xfoil_binary": XFOIL_BIN}

    return app


app = create_app()

__all__ = ["create_app", "app"]

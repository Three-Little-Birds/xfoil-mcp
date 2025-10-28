from __future__ import annotations

import subprocess
from http import HTTPStatus
from pathlib import Path
from unittest import mock

from fastapi.testclient import TestClient

from xfoil_mcp.core import compute_polar
from xfoil_mcp.fastapi_app import create_app
from xfoil_mcp.models import PolarRequest


def _fake_run(
    args: list[str],
    *,
    input: bytes,
    cwd: Path,
    check: bool,
    capture_output: bool,
) -> subprocess.CompletedProcess[bytes]:
    polar = cwd / "polar.txt"
    polar.write_text("alpha CL CD CM\n0.0 0.3 0.01 -0.05\n", encoding="utf-8")
    return subprocess.CompletedProcess(args, 0, b"ok", b"")


def test_compute_polar_returns_csv(tmp_path: Path) -> None:
    """Simulate an XFOIL run and ensure the helper emits a CSV string.

    The subprocess call is patched so newcomers can see the minimum request
    payload without needing XFOIL installed locally.
    """
    request = PolarRequest(
        airfoil_name="demo",
        airfoil_data="demo airfoil",
        alphas=[0.0],
        reynolds=1_200_000,
        mach=0.0,
        iterations=200,
    )

    with mock.patch("xfoil_mcp.core.subprocess.run", side_effect=_fake_run):
        response = compute_polar(request)

    assert "alpha" in response.csv
    assert "0.3" in response.csv


def test_fastapi_endpoint(tmp_path: Path) -> None:
    """Exercise the FastAPI surface so developers can copy/paste a request."""
    app = create_app()
    client = TestClient(app)
    payload = {
        "airfoil_name": "demo",
        "airfoil_data": "demo airfoil",
        "alphas": [0.0],
        "reynolds": 1_200_000,
        "mach": 0.0,
        "iterations": 200,
    }

    with mock.patch("xfoil_mcp.core.subprocess.run", side_effect=_fake_run):
        response = client.post("/polar", json=payload)

    assert response.status_code == HTTPStatus.OK
    csv_text = response.json()["csv"]
    assert "alpha" in csv_text
    assert "0.3" in csv_text

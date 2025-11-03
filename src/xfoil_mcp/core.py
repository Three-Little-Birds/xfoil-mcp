"""Core helpers for running XFOIL."""

from __future__ import annotations

import csv
import os
import subprocess
import tempfile
from collections.abc import Iterable
from pathlib import Path

from .models import PolarRequest, PolarResponse

XFOIL_BIN = os.environ.get("XFOIL_BIN", "xfoil")


def compute_polar(request: PolarRequest) -> PolarResponse:
    """Run XFOIL with the provided parameters and return a CSV payload."""

    script, polar_path = _prepare_script(request)
    try:
        result = subprocess.run(
            [XFOIL_BIN],
            input=script.encode("utf-8"),
            cwd=polar_path.parent,
            check=False,
            capture_output=True,
        )
    except FileNotFoundError as exc:  # pragma: no cover
        raise RuntimeError("XFOIL binary not found") from exc

    if not polar_path.exists():
        raise RuntimeError(
            "XFOIL did not create the polar output",
        )

    if result.returncode != 0:
        # XFOIL often exits with code 2 even when the polar file is valid. We keep
        # the output but annotate the CSV with a comment so downstream users are
        # aware of the non-zero status.
        warning_comment = f"# xfoil exit code {result.returncode}"
    else:
        warning_comment = None

    lines = polar_path.read_text(encoding="utf-8").splitlines()
    if warning_comment:
        lines.insert(0, warning_comment)

    rows = list(csv.reader(lines))
    if rows and rows[0] and "alpha" not in rows[0][0].lower():
        rows.insert(0, ["alpha", "CL", "CD", "CM"])

    csv_text = "\n".join(",".join(row) for row in rows)
    return PolarResponse(csv=csv_text)


def _prepare_script(request: PolarRequest) -> tuple[str, Path]:
    tmpdir = Path(tempfile.mkdtemp(prefix="xfoil_mcp_"))
    airfoil_path = tmpdir / f"{request.airfoil_name}.dat"
    polar_path = tmpdir / "polar.txt"
    airfoil_path.write_text(request.airfoil_data, encoding="utf-8")

    airfoil_name = airfoil_path.name
    polar_name = polar_path.name

    commands: Iterable[str] = [
        f"LOAD {airfoil_name}",
        "PANE",
        "OPER",
        f"VISC {request.reynolds}",
        f"MACH {request.mach}",
        f"ITER {request.iterations}",
        "PACC",
        polar_name,
        "",
    ]
    alpha_cmds = [f"ALFA {alpha}" for alpha in request.alphas]
    if not alpha_cmds:
        raise RuntimeError("At least one angle of attack must be supplied")

    footer = ["PACC", "", "QUIT"]
    script = "\n".join([*commands, *alpha_cmds, *footer]) + "\n"
    return script, polar_path


__all__ = ["compute_polar", "XFOIL_BIN"]

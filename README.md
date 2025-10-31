# xfoil-mcp · Aerodynamic polars on-call for your MCP agents

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License: MIT"></a>
  <a href="pyproject.toml"><img src="https://img.shields.io/badge/python-3.10%2B-3776AB.svg" alt="Python 3.10 or newer"></a>
  <a href="https://github.com/Three-Little-Birds/xfoil-mcp/actions/workflows/ci.yml"><img src="https://github.com/Three-Little-Birds/xfoil-mcp/actions/workflows/ci.yml/badge.svg" alt="CI status"></a>
  <img src="https://img.shields.io/badge/status-production%20ready-4caf50.svg" alt="Project status: production ready">
  <img src="https://img.shields.io/badge/MCP-tooling-blueviolet.svg" alt="MCP tooling badge">
</p>

> **TL;DR**: Wrap [XFOIL](https://web.mit.edu/drela/Public/web/xfoil/) in an MCP-native service so agents can request lift/drag/moment polars without touching shell scripts.

## Table of contents

1. [Why agents love it](#why-agents-love-it)
2. [Quickstart](#quickstart)
3. [Run as a service](#run-as-a-service)
4. [Agent playbook](#agent-playbook)
5. [Stretch ideas](#stretch-ideas)
6. [Accessibility & upkeep](#accessibility--upkeep)
7. [Contributing](#contributing)

## Why agents love it

| Persona | What you get immediately | Why it scales |
|---------|-------------------------|---------------|
| **New users** | One `uv pip install` plus a concrete polar example; CSVs land on disk with clear headers. | Typed models and example responses keep the learning curve shallow. |
| **Experienced teams** | Drop-in FastAPI app or STDIO tool compatible with the Model Context Protocol. | Deterministic artefact folders (`response.workdir`) simplify audits and orchestration.

The layout mirrors 2025 README recommendations—purpose up top, actionable steps next, then detail for deeper dives.【turn0search0】

## Quickstart

### 1. Install dependencies

```bash
uv pip install "git+https://github.com/Three-Little-Birds/xfoil-mcp.git"
```

Ensure the XFOIL binary is on your `PATH` (or point to it explicitly):

```bash
export XFOIL_BIN=/path/to/xfoil
```

### 2. Compute your first polar

```python
from pathlib import Path

from xfoil_mcp import PolarRequest, compute_polar

request = PolarRequest(
    airfoil_path=str(Path("naca2412.dat")),
    alpha_start_deg=-2,
    alpha_end_deg=12,
    alpha_step_deg=0.5,
    reynolds=1.2e6,
    mach=0.08,
)
response = compute_polar(request)
print("CSV stored at", response.csv_path)
```

Analyse with `pandas`:

```python
import pandas as pd

df = pd.read_csv(response.csv_path)
print(df.head())
```

## Run as a service

### FastAPI (REST)

```bash
uv run uvicorn xfoil_mcp.fastapi_app:create_app --factory --port 8001
```

Browse `http://127.0.0.1:8001/docs` to test requests and download CSVs.

### python-sdk tool (STDIO / MCP)

```python
from mcp.server.fastmcp import FastMCP
from xfoil_mcp.tool import build_tool

mcp = FastMCP("xfoil-mcp", "XFOIL polar analysis")
build_tool(mcp)

if __name__ == "__main__":
    mcp.run()
```

Launch:

```bash
uv run mcp dev examples/xfoil_tool.py
```

Connect any MCP-compatible agent (Cursor, Claude Desktop, Windsurf, …) and ask for polars on demand.

## Agent playbook

- **Batch sweeps** – iterate through a directory of `.dat` files and persist each polar to object storage.
- **Optimisation loops** – embed the tool inside a genetic algorithm; typed responses keep mutation + evaluation deterministic.
- **Visualisation** – feed `response.csv_path` into Plotly or Matplotlib to plot `Cl` vs. `Cd` without manual parsing.

## Stretch ideas

1. Compare multiple foils by merging CSVs into a parquet dataset for notebook analysis.
2. Pair with `ctrltest-mcp` to explore control implications from polar derivatives.
3. Schedule nightly polars via CI and publish artefacts for downstream agents.

## Accessibility & upkeep

- Badges include descriptive alt text and are limited to five for readability on mobile.【turn0search0】
- Tests mock XFOIL so they run quickly: `uv run pytest`.
- Use `uv run ruff check .` before submitting changes.

## Contributing

1. Fork and `uv pip install --system -e .[dev]`.
2. Run the formatting and test suite.
3. Open a PR with before/after polar snippets so reviewers can verify quickly.

MIT license — see [LICENSE](LICENSE).

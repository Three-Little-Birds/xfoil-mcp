# xfoil-mcp - Aerodynamic polars on-call for your MCP agents

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License: MIT"></a>
  <a href="pyproject.toml"><img src="https://img.shields.io/badge/python-3.10%2B-3776AB.svg" alt="Python 3.10 or newer"></a>
  <a href="https://github.com/Three-Little-Birds/xfoil-mcp/actions/workflows/ci.yml"><img src="https://github.com/Three-Little-Birds/xfoil-mcp/actions/workflows/ci.yml/badge.svg" alt="CI status"></a>
  <img src="https://img.shields.io/badge/MCP-tooling-blueviolet.svg" alt="MCP tooling badge">
</p>

> **TL;DR**: Wrap [XFOIL](https://web.mit.edu/drela/Public/web/xfoil/) in an MCP-native service so agents can request lift/drag/moment polars without touching shell scripts.

## Table of contents

1. [What it provides](#what-it-provides)
2. [Quickstart](#quickstart)
3. [Run as a service](#run-as-a-service)
4. [Agent playbook](#agent-playbook)
5. [Stretch ideas](#stretch-ideas)
6. [Accessibility & upkeep](#accessibility--upkeep)
7. [Contributing](#contributing)

## What it provides

| Scenario | Value |
|----------|-------|
| Quick experiments | Compute lift/drag/moment polars from an airfoil file or NACA code without launching XFOIL manually. |
| MCP integration | STDIO/HTTP transports that follow the Model Context Protocol so ToolHive or other clients can call XFOIL programmatically. |
| Audit trail | Responses include on-disk work directories and metadata so you can trace which inputs produced a given polar. |

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

### CLI (STDIO / Streamable HTTP)

```bash
uvx xfoil-mcp  # runs the MCP over stdio
# or python -m xfoil_mcp
python -m xfoil_mcp --transport streamable-http --host 0.0.0.0 --port 8000 --path /mcp
```

Use `python -m xfoil_mcp --describe` to view metadata and exit.

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

Connect any MCP-compatible agent (Cursor, Claude Desktop, Windsurf, ...) and ask for polars on demand.

### ToolHive smoke test

Requires `XFOIL_BIN` pointing to the XFOIL executable:

```bash
export XFOIL_BIN=/path/to/xfoil
uvx --with 'mcp==1.20.0' python scripts/integration/run_xfoil.py
# ToolHive 2025+ defaults to Streamable HTTP; match that transport when registering
# the workload manually to avoid the legacy SSE proxy failures.
```

## Agent playbook

- **Batch sweeps** - iterate through a directory of `.dat` files and persist each polar to object storage.
- **Optimisation loops** - embed the tool inside a genetic algorithm; typed responses keep mutation + evaluation deterministic.
- **Visualisation** - feed `response.csv_path` into Plotly or Matplotlib to plot `Cl` vs. `Cd` without manual parsing.

## Stretch ideas

1. Compare multiple foils by merging CSVs into a parquet dataset for notebook analysis.
2. Pair with `ctrltest-mcp` to explore control implications from polar derivatives.
3. Schedule nightly polars via CI and publish artefacts for downstream agents.

## Accessibility & upkeep

- Badges include descriptive alt text and are limited to five for readability on mobile.
- Tests mock XFOIL so they run quickly: `uv run pytest`.
- Use `uv run ruff check .` before submitting changes.

## Contributing

1. Fork and `uv pip install --system -e .[dev]`.
2. Run the formatting and test suite.
3. Open a PR with before/after polar snippets so reviewers can verify quickly.

MIT license - see [LICENSE](LICENSE).

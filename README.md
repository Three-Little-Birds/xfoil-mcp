# xfoil-mcp · Teach an Agent to Fly an Airfoil

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-brightgreen.svg)](pyproject.toml)
[![CI](https://github.com/Three-Little-Birds/xfoil-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/Three-Little-Birds/xfoil-mcp/actions/workflows/ci.yml)

This repository turns the classic [XFOIL](https://web.mit.edu/drela/Public/web/xfoil/) polar solver into an approachable learning project for Model Context Protocol (MCP) agents. Instead of wrestling with shell scripts, you can hand an agent a set of coordinates and walk away with a clean CSV table of lift, drag, and moment data.

## What you will build

By the end of this README you will:

1. Install XFOIL and the MCP wrapper on any workstation.
2. Run your first polar sweep from Python, complete with visualisation-ready CSV output.
3. Connect the python-sdk tool to a conversational agent so it can answer “what if” questions about airfoil performance on demand.

## Prerequisites

- XFOIL binaries (macOS/Linux users can grab them from the [official site](https://web.mit.edu/drela/Public/web/xfoil/); Windows users can rely on WSL).
- Python 3.10 or newer with [`uv`](https://github.com/astral-sh/uv) installed.
- Optional but recommended: a plotting library such as `matplotlib` to visualise results.

Set an environment variable if `xfoil` isn’t already on your `PATH`:

```bash
export XFOIL_BIN=/path/to/xfoil
```

## Step 1 – Install the wrapper

```bash
uv pip install "git+https://github.com/Three-Little-Birds/xfoil-mcp.git"
```

This brings in the typed request/response models, FastAPI surface, and python-sdk tool helper. The package has no heavy dependencies; as long as XFOIL itself is reachable the wrapper will do the rest.

## Step 2 – Run your first polar sweep in Python

```python
from pathlib import Path

from xfoil_mcp import PolarRequest, compute_polar

airfoil_path = Path("naca2412.dat")  # any coordinate file works
request = PolarRequest(
    airfoil_path=str(airfoil_path),
    alpha_start_deg=-2.0,
    alpha_end_deg=12.0,
    alpha_step_deg=0.5,
    reynolds=1.2e6,
    mach=0.08,
)

response = compute_polar(request)
print("CSV stored at", response.csv_path)
```

Open the CSV in your favourite tool, or drop it into `pandas`:

```python
import pandas as pd

df = pd.read_csv(response.csv_path)
print(df.head())
```

Behind the scenes the helper wrote the temporary XFOIL command script, streamed it to the CLI, and normalised the output into a clean table. Every artefact is saved in `response.workdir` for later auditing.

## Step 3 – Expose XFOIL through an MCP agent

### Option A: FastAPI microservice

```python
from xfoil_mcp.fastapi_app import create_app

app = create_app()
```

Run it locally:

```bash
uv run uvicorn xfoil_mcp.fastapi_app:create_app --factory --port 8001
```

Visit `http://127.0.0.1:8001/docs` to try the interactive schema and download results.

### Option B: python-sdk tool (STDIO transport)

```python
from mcp.server.fastmcp import FastMCP
from xfoil_mcp.tool import build_tool

mcp = FastMCP("xfoil-mcp", "XFOIL polar analysis")
build_tool(mcp)

if __name__ == "__main__":
    mcp.run()
```

Launch the tool in development mode:

```bash
uv run mcp dev examples/xfoil_tool.py
```

Open your MCP-compatible agent (Cursor, Claude Desktop, Windsurf, …) and point it at the running tool. Ask it “compute a polar for the S1223 airfoil at 500k Reynolds” and the agent will call into XFOIL using the wrapper above.

## Step 4 – Stretch goals

- Batch multiple airfoils: iterate through a directory of `.dat` files and save a consolidated CSV per design.
- Couple to optimisation: use the MCP tool inside a genetic algorithm to evolve airfoil shapes while logging every script/result pair.
- Visualise directly: load `response.csv_path` into Plotly or Matplotlib to render `Cl` vs. `Cd` traces.

## Developing the package

```bash
uv pip install --system -e .[dev]
uv run ruff check .
uv run pytest
```

The tests double as examples—they mock the XFOIL binary so you can inspect the expected request payloads and CSV structure without running the solver.

## License

MIT — see [LICENSE](LICENSE).

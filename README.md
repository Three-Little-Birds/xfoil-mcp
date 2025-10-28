# xfoil-mcp

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-brightgreen.svg)](pyproject.toml)
[![CI](https://github.com/yevheniikravchuk/xfoil-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/yevheniikravchuk/xfoil-mcp/actions/workflows/ci.yml)

Model Context Protocol (MCP) toolkit for driving [XFOIL](https://web.mit.edu/drela/Public/web/xfoil/) polar analyses from agents or automation scripts. It wraps the CLI workflow—coordinate ingestion, input script generation, result parsing—so tools can request lift/drag data without hand-coding shell glue.

## Why you might want this

- **Automate airfoil studies** – feed raw coordinates and let an agent schedule lift/drag sweeps without opening XFOIL manually.
- **Skip ad-hoc shell scripts** – the package writes the control script, manages the working directory, and normalises the CSV output.
- **Keep pipelines reproducible** – every request captures the script and result text, making it easy to archive or replay analyses.

## Features

- Typed request/response models for polar sweeps.
- Reusable `compute_polar` helper that streams commands to the XFOIL CLI.
- Optional FastAPI app and python-sdk tool shims for quick integration.
- MIT-licensed, fully typed, and covered by unit tests.

## Installation

```bash
pip install "git+https://github.com/yevheniikravchuk/xfoil-mcp.git"
```

> PyPI publication is on the roadmap; until then install directly from the Git repository or vendor the package.

## Quickstart (FastAPI)

```python
from xfoil_mcp.fastapi_app import create_app

app = create_app()
```

Run locally:

```bash
uv run uvicorn xfoil_mcp.fastapi_app:create_app --factory --host 127.0.0.1 --port 8001
```

## Quickstart (python-sdk tool)

```python
from mcp.server.fastmcp import FastMCP
from xfoil_mcp.tool import build_tool

mcp = FastMCP("xfoil-mcp", "XFOIL polar analysis")
build_tool(mcp)

if __name__ == "__main__":
    mcp.run()
```

Launch via STDIO transport:

```bash
uv run mcp dev examples/xfoil_tool.py
```

## Environment

Set `XFOIL_BIN` to the path of your XFOIL executable if it is not already on `PATH`.

## Local development

```bash
uv pip install --system -e .[dev]
uv run ruff check .
uv run pytest
```

The tests double as usage samples: each one mocks XFOIL so newcomers can see the minimum request payload and the shape of the CSV response.

## License

MIT — see [LICENSE](LICENSE).

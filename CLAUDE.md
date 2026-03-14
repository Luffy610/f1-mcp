# F1 Analytics MCP Server

## Project Overview
An MCP (Model Context Protocol) server providing 118+ Formula 1 analytics tools powered by FastF1 and Ergast APIs. Installable via `pip install -e .` with a `f1-mcp` CLI entry point (stdio transport). Also supports SSE transport via `python server.py`.

## Architecture
```
f1_mcp/                    → Python package (pip-installable)
  server.py                → Entry point, registers all tool modules, main() for stdio
  config.py                → FastF1 cache init
  connectors/              → Data sources (FastF1Loader, ErgastClient)
  core/                    → Caching layer (SessionCacheManager, TelemetryCacheManager)
  models/schemas.py        → Pydantic schemas
  services/                → Business logic (14 service classes)
  tools/                   → MCP tool registrations (14 modules, 1:1 with services)
server.py                  → Backwards-compat wrapper (SSE mode)
tests/                     → E2E test suite
plots/                     → Generated visualization PNGs
cache/                     → FastF1 disk cache
```

## Key Patterns
- **Services** contain all logic; **tools** are thin wrappers registering with `@mcp.tool()`
- `session_cache` and `telemetry_cache` are singletons in `core/` — thread-safe with locks
- All DataFrame→JSON conversion must go through `core/serialization.py:sanitize_df()` to avoid Timedelta/NaN/float-int serialization errors
- Tool parameters use: `year: int, grand_prix: str, session: str` (session = "R", "Q", "FP1", etc.)

## Running
```bash
pip install -e .                         # Install in dev mode
f1-mcp                                   # Start MCP server (stdio, for MCP clients)
python server.py                         # Start MCP server (SSE, port 8000)
python -m pytest tests/ -v               # Run E2E tests
python -m pytest tests/ -v -k "test_lap" # Run specific test group
```

## Common Pitfalls
- FastF1 `LapNumber`, `Position`, `Stint` columns are **float64** (not int) — always cast before JSON
- `Timedelta` columns (`LapTime`, `SectorXTime`, `PitInTime`) are not JSON-serializable — convert to string
- Telemetry arrays from different laps have different lengths — always interpolate to common distance before comparing
- `NaN`/`NaT` values must be converted to `None` for JSON
- DataFrames from `get_circuit_info()` marshal data are DataFrames, not dicts — must convert

## Dependencies
fastmcp, fastf1, pandas, numpy, pydantic, matplotlib, scikit-learn

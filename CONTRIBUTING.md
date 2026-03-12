# Contributing to F1 MCP Server

Thanks for your interest in contributing! This guide will help you get started.

## Development Setup

1. **Clone the repo:**
   ```bash
   git clone https://github.com/Luffy610/f1-mcp.git
   cd f1-mcp
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   # or: .venv\Scripts\activate  # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install pytest  # for running tests
   ```

4. **Start the server:**
   ```bash
   python server.py
   ```

## Project Structure

```
server.py          → Entry point, registers all tool modules
config.py          → FastF1 cache configuration
connectors/        → Data sources (FastF1Loader, ErgastClient)
core/              → Caching and serialization
models/            → Pydantic schemas
services/          → Business logic (14 service classes)
tools/             → MCP tool registrations (14 modules)
tests/             → End-to-end test suite
```

## Adding a New Tool

Each tool follows a **service + tool** pattern:

1. **Create or extend a service** in `services/` with the business logic.
2. **Create or extend a tool module** in `tools/` that registers the tool with `@mcp.tool()`.
3. **Add tests** in `tests/` covering the new tool.

### Example

```python
# services/my_service.py
class MyService:
    def my_analysis(self, year, grand_prix, session, driver):
        # Load data via connectors, perform analysis
        return result

# tools/my_tools.py
from services.my_service import MyService

service = MyService()

def register_tools(mcp):
    @mcp.tool()
    def my_analysis(year: int, grand_prix: str, session: str, driver: str) -> dict:
        """One-line description of what the tool does."""
        return service.my_analysis(year, grand_prix, session, driver)
```

### Key conventions

- Tool parameters use: `year: int, grand_prix: str, session: str` (session = "R", "Q", "FP1", etc.)
- All DataFrame-to-JSON conversion must use `core/serialization.py:sanitize_df()` to handle Timedelta/NaN/float-int issues.
- Tools are thin wrappers; keep logic in the service layer.

## Running Tests

```bash
python -m pytest tests/ -v

# Run a specific test group
python -m pytest tests/ -v -k "test_lap"
```

Tests use the 2023 Bahrain GP Race data. FastF1 caches session data on first run, so the initial test run will be slower.

## Code Style

- Follow existing patterns in the codebase.
- Use type hints for function signatures.
- Keep tool docstrings concise — they appear in the MCP tool listing.

## Pull Request Process

1. Fork the repo and create a feature branch.
2. Make your changes following the patterns above.
3. Ensure all tests pass.
4. Submit a PR with a clear description of what you added/changed.

## Common Pitfalls

- FastF1 columns like `LapNumber`, `Position`, `Stint` are **float64**, not int — cast before JSON.
- `Timedelta` columns (`LapTime`, `SectorXTime`) are not JSON-serializable — convert to string.
- `NaN`/`NaT` values must be converted to `None` for JSON output.
- Telemetry arrays from different laps have different lengths — interpolate to a common distance scale before comparing.

# F1 Analytics MCP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://github.com/Luffy610/f1-mcp/actions/workflows/test.yml/badge.svg)](https://github.com/Luffy610/f1-mcp/actions/workflows/test.yml)

An MCP (Model Context Protocol) server providing **118+ Formula 1 analytics tools** powered by [FastF1](https://docs.fastf1.dev/) and the Ergast API. Connect it to Claude Desktop, Claude Code, or any MCP client to analyze races, compare drivers, explore telemetry, and simulate strategies using natural language.

## Features

- **Session & Driver Info** — race results, standings, circuit details, driver metadata
- **Lap & Sector Analysis** — lap times, sector deltas, consistency scores, clean lap filtering
- **Telemetry** — speed/throttle/brake/gear/RPM traces, corner analysis, braking points
- **Strategy Intelligence** — tyre degradation, pit windows, undercut/overcut analysis, strategy simulation
- **Race Position** — overtakes, battles, gap evolution, position changes, lead changes
- **Predictive AI** — race winner prediction, overtake probability, tyre cliff prediction, safety car probability
- **Visualizations** — speed maps, race progression charts, tyre degradation plots, track dominance maps

## Architecture

```
server.py              → Entry point, registers all tool modules
config.py              → FastF1 cache configuration
connectors/            → Data sources (FastF1Loader, ErgastClient)
core/                  → Caching layer + serialization utilities
models/                → Pydantic schemas
services/              → Business logic (14 service classes)
tools/                 → MCP tool registrations (14 modules, 1:1 with services)
tests/                 → End-to-end test suite (118 tests)
```

## Quick Start

### Docker (recommended)

```bash
docker compose up -d
```

The MCP server will be available at `http://localhost:8000/sse`.

### pip

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python server.py
```

### conda

```bash
conda create -n f1-mcp python=3.13
conda activate f1-mcp
pip install -r requirements.txt
python server.py
```

## MCP Client Configuration

### Claude Desktop

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "f1": {
      "url": "http://localhost:8000/sse"
    }
  }
}
```

### Claude Code

Add to your project's `.mcp.json`:

```json
{
  "mcpServers": {
    "f1": {
      "type": "sse",
      "url": "http://localhost:8000/sse"
    }
  }
}
```

## Tool Categories

| Category | Tools | Examples |
|---|---|---|
| Session | 8 | Race info, weather, circuit details, flag events |
| Driver | 8 | Standings, driver info, team lookup, points |
| Lap | 10 | Lap times, distributions, clean laps, deleted laps |
| Sector | 8 | Sector times, deltas, consistency, improvement trends |
| Telemetry | 12 | Speed/brake/throttle/gear traces, corner analysis |
| Strategy | 10 | Tyre strategy, stint lengths, compound usage, degradation |
| Pit Stops | 6 | Pit times, pit lane loss, pit stop summaries |
| Race Position | 8 | Overtakes, battles, gap evolution, lead changes |
| Strategy Intelligence | 10 | Undercut/overcut, optimal pit window, strategy simulation |
| Telemetry Intelligence | 10 | Braking analysis, corner speeds, dirty air, energy deployment |
| Advanced Analytics | 8 | Driver style clustering, aggression/risk indices, consistency |
| Predictive AI | 14 | Race winner, overtake probability, tyre cliff, safety car |
| Visualization | 6 | Speed maps, race progression, tyre degradation plots |

## Example Prompts

```
Analyze why Verstappen won the 2023 Bahrain GP. Break down his tyre strategy,
pit stops, race pace trend, and any overtakes he made.
```

```
Compare Verstappen and Leclerc through Turn 10 at the 2023 Bahrain GP.
Who brakes later, carries more apex speed, and gets on the throttle earlier?
```

```
Simulate how the 2023 Bahrain GP would have played out if Verstappen used
a two-stop strategy instead of his actual strategy.
```

See [example.md](example.md) for more detailed example prompts with the specific tools they trigger.

## Development

```bash
# Install dev dependencies
pip install -r requirements.txt
pip install pytest

# Run all tests
python -m pytest tests/ -v

# Run specific test group
python -m pytest tests/ -v -k "test_lap"
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on adding new tools.

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `F1_CACHE_DIR` | `./cache` | Directory for FastF1 data cache |

## License

[MIT](LICENSE)

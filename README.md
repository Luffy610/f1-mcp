# F1 Analytics MCP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://github.com/Luffy610/f1-mcp/actions/workflows/test.yml/badge.svg)](https://github.com/Luffy610/f1-mcp/actions/workflows/test.yml)
[![PyPI version](https://img.shields.io/pypi/v/f1-mcp.svg)](https://pypi.org/project/f1-mcp/)
[![GitHub stars](https://img.shields.io/github/stars/Luffy610/f1-mcp)](https://github.com/Luffy610/f1-mcp/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/Luffy610/f1-mcp)](https://github.com/Luffy610/f1-mcp/issues)
[![GitHub Discussions](https://img.shields.io/github/discussions/Luffy610/f1-mcp)](https://github.com/Luffy610/f1-mcp/discussions)

An MCP (Model Context Protocol) server providing **118+ Formula 1 analytics tools** powered by [FastF1](https://docs.fastf1.dev/) and the Ergast API. Connect it to Claude Desktop, Claude Code, or any MCP client to analyze races, compare drivers, explore telemetry, and simulate strategies using natural language.

## Features

- **Session & Driver Info** — race results, standings, circuit details, driver metadata
- **Lap & Sector Analysis** — lap times, sector deltas, consistency scores, clean lap filtering
- **Telemetry** — speed/throttle/brake/gear/RPM traces, corner analysis, braking points
- **Strategy Intelligence** — tyre degradation, pit windows, undercut/overcut analysis, strategy simulation
- **Race Position** — overtakes, battles, gap evolution, position changes, lead changes
- **Predictive AI** — race winner prediction, overtake probability, tyre cliff prediction, safety car probability
- **Visualizations** — speed maps, race progression charts, tyre degradation plots, track dominance maps

## Quick Start

### pip install (recommended)

```bash
pip install f1-mcp
```

Install from source:

```bash
pip install git+https://github.com/Luffy610/f1-mcp.git
```

### Docker

```bash
docker compose up -d
```

The MCP server will be available at `http://localhost:8000/sse`.

## MCP Client Configuration

### Claude Desktop / Claude Code (stdio — recommended)

```json
{
  "mcpServers": {
    "f1": {
      "command": "f1-mcp"
    }
  }
}
```

### SSE mode (remote / Docker)

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

To start the SSE server manually: `python server.py`

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

## Contributing

We welcome contributions! The `master` branch is protected — please **fork the repo**, create a feature branch, and submit a pull request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/my-new-tool`)
3. Make your changes and ensure tests pass (`python -m pytest tests/ -v`)
4. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines on project structure, adding tools, and code style.

## Reporting Issues & Requesting Features

- **Bug reports** — [Open an issue](https://github.com/Luffy610/f1-mcp/issues/new?template=bug_report.md) with steps to reproduce
- **Feature requests** — [Open an issue](https://github.com/Luffy610/f1-mcp/issues/new?template=feature_request.md) describing your use case
- **Questions & ideas** — Start a thread in [GitHub Discussions](https://github.com/Luffy610/f1-mcp/discussions)

## Development

```bash
# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Run all tests
python -m pytest tests/ -v

# Run specific test group
python -m pytest tests/ -v -k "test_lap"

# Start SSE server for development
python server.py
```

## Architecture

```
f1_mcp/                → Python package
  server.py            → Entry point, registers all tool modules
  config.py            → FastF1 cache configuration
  connectors/          → Data sources (FastF1Loader, ErgastClient)
  core/                → Caching layer + serialization utilities
  models/              → Pydantic schemas
  services/            → Business logic (14 service classes)
  tools/               → MCP tool registrations (14 modules, 1:1 with services)
tests/                 → End-to-end test suite (118 tests)
```

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `F1_CACHE_DIR` | `./cache` | Directory for FastF1 data cache |

## License

[MIT](LICENSE)

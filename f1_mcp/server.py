"""F1 Analytics MCP Server entry point. Registers all tool modules and runs via SSE transport."""

from fastmcp import FastMCP
from f1_mcp.config import initialize_cache

import f1_mcp.tools.session_tools as session_tools
import f1_mcp.tools.driver_tools as driver_tools
import f1_mcp.tools.lap_tools as lap_tools
import f1_mcp.tools.sector_tools as sector_tools
import f1_mcp.tools.telemetry_tools as telemetry_tools
import f1_mcp.tools.strategy_tools as strategy_tools
import f1_mcp.tools.pitstop_tools as pitstop_tools
import f1_mcp.tools.race_position_tools as race_position_tools
import f1_mcp.tools.strategy_intelligence_tools as strategy_intelligence_tools
import f1_mcp.tools.telemetry_intelligence_tools as telemetry_intelligence_tools
import f1_mcp.tools.advanced_analytics_tools as advanced_analytics_tools
import f1_mcp.tools.predictive_ai_tools as predictive_ai_tools
import f1_mcp.tools.visualization_tools as visualization_tools
import f1_mcp.tools.provider_tools as provider_tools

initialize_cache()

mcp = FastMCP("F1 Analytics MCP")

# Register tools
session_tools.register_tools(mcp)
driver_tools.register_tools(mcp)
lap_tools.register_tools(mcp)
sector_tools.register_tools(mcp)
telemetry_tools.register_tools(mcp)
strategy_tools.register_tools(mcp)
pitstop_tools.register_tools(mcp)
race_position_tools.register_tools(mcp)
strategy_intelligence_tools.register_tools(mcp)
telemetry_intelligence_tools.register_tools(mcp)
advanced_analytics_tools.register_tools(mcp)
predictive_ai_tools.register_tools(mcp)
visualization_tools.register_tools(mcp)
provider_tools.register_tools(mcp)


def main():
    """CLI entry point — runs the MCP server with stdio transport."""
    mcp.run()


if __name__ == "__main__":
    mcp.run(
        transport="sse",
        host="0.0.0.0",
        port=8000
    )

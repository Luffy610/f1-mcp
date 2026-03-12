"""F1 Analytics MCP Server entry point. Registers all tool modules and runs via SSE transport."""

from fastmcp import FastMCP
from config import initialize_cache

import tools.session_tools as session_tools
import tools.driver_tools as driver_tools
import tools.lap_tools as lap_tools
import tools.sector_tools as sector_tools
import tools.telemetry_tools as telemetry_tools
import tools.strategy_tools as strategy_tools
import tools.pitstop_tools as pitstop_tools
import tools.race_position_tools as race_position_tools
import tools.strategy_intelligence_tools as strategy_intelligence_tools
import tools.telemetry_intelligence_tools as telemetry_intelligence_tools
import tools.advanced_analytics_tools as advanced_analytics_tools
import tools.predictive_ai_tools as predictive_ai_tools
import tools.visualization_tools as visualization_tools
import tools.provider_tools as provider_tools

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

if __name__ == "__main__":
    mcp.run(
        transport="sse",
        host="0.0.0.0",
        port=8000
    )
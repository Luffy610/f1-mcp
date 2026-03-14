from f1_mcp.services.strategy_intelligence_service import StrategyIntelligenceService

service = StrategyIntelligenceService()


def register_tools(mcp):

    """Register strategy intelligence tools with the MCP server."""
    @mcp.tool()
    def predict_undercut_success(year: int, grand_prix: str, session: str, driver: str):
        """Predict whether an undercut strategy would be effective for a driver."""
        return service.predict_undercut_success(year, grand_prix, session, driver)


    @mcp.tool()
    def predict_overcut_success(year: int, grand_prix: str, session: str, driver: str):
        """Predict whether an overcut strategy would be effective for a driver."""
        return service.predict_overcut_success(year, grand_prix, session, driver)


    @mcp.tool()
    def race_strategy_simulation(year: int, grand_prix: str, session: str, driver: str):
        """Simulate race strategy outcomes for a driver."""
        return service.race_strategy_simulation(year, grand_prix, session, driver)


    @mcp.tool()
    def two_stop_vs_one_stop_simulation(year: int, grand_prix: str, session: str, driver: str):
        """Compare one-stop vs two-stop strategy outcomes for a driver."""
        return service.two_stop_vs_one_stop_simulation(year, grand_prix, session, driver)


    @mcp.tool()
    def predict_optimal_strategy(year: int, grand_prix: str, session: str, driver: str):
        """Recommend optimal pit strategy based on tyre degradation rate."""
        return service.predict_optimal_strategy(year, grand_prix, session, driver)


    @mcp.tool()
    def track_position_importance(year: int, grand_prix: str, session: str):
        """Measure how much track position correlates with lap time."""
        return service.track_position_importance(year, grand_prix, session)
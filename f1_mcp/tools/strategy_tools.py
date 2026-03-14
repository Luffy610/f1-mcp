from f1_mcp.services.strategy_service import StrategyService

service = StrategyService()


def register_tools(mcp):

    """Register tyre strategy tools with the MCP server."""
    @mcp.tool()
    def get_tyre_strategy(year: int, grand_prix: str, session: str, driver: str):
        """Get a driver's tyre strategy with compounds and stint details."""
        return service.get_tyre_strategy(year, grand_prix, session, driver)


    @mcp.tool()
    def get_stints(year: int, grand_prix: str, session: str, driver: str):
        """Get stint breakdown with compound and lap count for a driver."""
        return service.get_stints(year, grand_prix, session, driver)


    @mcp.tool()
    def get_tyre_compound_usage(year: int, grand_prix: str, session: str):
        """Get total lap count per tyre compound across the session."""
        return service.get_tyre_compound_usage(year, grand_prix, session)


    @mcp.tool()
    def get_average_stint_length(year: int, grand_prix: str, session: str):
        """Get the average stint length across all drivers in laps."""
        return service.get_average_stint_length(year, grand_prix, session)


    @mcp.tool()
    def get_tyre_degradation_rate(year: int, grand_prix: str, session: str, driver: str):
        """Get lap time degradation slope per compound for a driver."""
        return service.get_tyre_degradation_rate(year, grand_prix, session, driver)


    @mcp.tool()
    def predict_tyre_cliff(year: int, grand_prix: str, session: str, driver: str):
        """Predict the lap where each tyre compound's performance drops off."""
        return service.predict_tyre_cliff(year, grand_prix, session, driver)


    @mcp.tool()
    def compare_tyre_performance(year: int, grand_prix: str, session: str):
        """Compare average and best lap times across tyre compounds."""
        return service.compare_tyre_performance(year, grand_prix, session)


    @mcp.tool()
    def tyre_strategy_comparison(year: int, grand_prix: str, session: str, driver_a: str, driver_b: str):
        """Compare tyre strategies between two drivers side by side."""
        return service.tyre_strategy_comparison(year, grand_prix, session, driver_a, driver_b)
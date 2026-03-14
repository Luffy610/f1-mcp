from f1_mcp.services.advanced_analytics_service import AdvancedAnalyticsService

service = AdvancedAnalyticsService()


def register_tools(mcp):

    """Register advanced analytics tools with the MCP server."""
    @mcp.tool()
    def driver_consistency_score(year: int, grand_prix: str, session: str, driver: str):
        """Calculate a 0-1 consistency score based on lap time variance."""
        return service.driver_consistency_score(year, grand_prix, session, driver)


    @mcp.tool()
    def driver_aggression_index(year: int, grand_prix: str, session: str, driver: str):
        """Calculate an aggression index based on overtake frequency."""
        return service.driver_aggression_index(year, grand_prix, session, driver)


    @mcp.tool()
    def driver_risk_index(year: int, grand_prix: str, session: str, driver: str):
        """Calculate a risk index based on deleted lap frequency."""
        return service.driver_risk_index(year, grand_prix, session, driver)


    @mcp.tool()
    def qualifying_improvement_analysis(year: int, grand_prix: str, driver: str):
        """Measure a driver's lap time improvement across qualifying."""
        return service.qualifying_improvement_analysis(year, grand_prix, driver)


    @mcp.tool()
    def lap_time_variance(year: int, grand_prix: str, session: str, driver: str):
        """Get the statistical variance of a driver's lap times."""
        return service.lap_time_variance(year, grand_prix, session, driver)


    @mcp.tool()
    def performance_trend(year: int, grand_prix: str, session: str, driver: str):
        """Detect whether a driver's pace is improving, stable, or declining."""
        return service.performance_trend(year, grand_prix, session, driver)


    @mcp.tool()
    def driver_style_clustering(year: int, grand_prix: str, session: str):
        """Cluster drivers into driving style groups using K-means."""
        return service.driver_style_clustering(year, grand_prix, session)
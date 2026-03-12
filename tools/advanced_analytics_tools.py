from services.advanced_analytics_service import AdvancedAnalyticsService

service = AdvancedAnalyticsService()


def register_tools(mcp):

    @mcp.tool()
    def driver_consistency_score(year: int, grand_prix: str, session: str, driver: str):
        return service.driver_consistency_score(year, grand_prix, session, driver)


    @mcp.tool()
    def driver_aggression_index(year: int, grand_prix: str, session: str, driver: str):
        return service.driver_aggression_index(year, grand_prix, session, driver)


    @mcp.tool()
    def driver_risk_index(year: int, grand_prix: str, session: str, driver: str):
        return service.driver_risk_index(year, grand_prix, session, driver)


    @mcp.tool()
    def qualifying_improvement_analysis(year: int, grand_prix: str, driver: str):
        return service.qualifying_improvement_analysis(year, grand_prix, driver)


    @mcp.tool()
    def lap_time_variance(year: int, grand_prix: str, session: str, driver: str):
        return service.lap_time_variance(year, grand_prix, session, driver)


    @mcp.tool()
    def performance_trend(year: int, grand_prix: str, session: str, driver: str):
        return service.performance_trend(year, grand_prix, session, driver)


    @mcp.tool()
    def driver_style_clustering(year: int, grand_prix: str, session: str):
        return service.driver_style_clustering(year, grand_prix, session)
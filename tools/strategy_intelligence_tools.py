from services.strategy_intelligence_service import StrategyIntelligenceService

service = StrategyIntelligenceService()


def register_tools(mcp):

    @mcp.tool()
    def predict_undercut_success(year: int, grand_prix: str, session: str, driver: str):
        return service.predict_undercut_success(year, grand_prix, session, driver)


    @mcp.tool()
    def predict_overcut_success(year: int, grand_prix: str, session: str, driver: str):
        return service.predict_overcut_success(year, grand_prix, session, driver)


    @mcp.tool()
    def race_strategy_simulation(year: int, grand_prix: str, session: str, driver: str):
        return service.race_strategy_simulation(year, grand_prix, session, driver)


    @mcp.tool()
    def two_stop_vs_one_stop_simulation(year: int, grand_prix: str, session: str, driver: str):
        return service.two_stop_vs_one_stop_simulation(year, grand_prix, session, driver)


    @mcp.tool()
    def predict_optimal_strategy(year: int, grand_prix: str, session: str, driver: str):
        return service.predict_optimal_strategy(year, grand_prix, session, driver)


    @mcp.tool()
    def track_position_importance(year: int, grand_prix: str, session: str):
        return service.track_position_importance(year, grand_prix, session)
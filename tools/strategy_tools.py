from services.strategy_service import StrategyService

service = StrategyService()


def register_tools(mcp):

    @mcp.tool()
    def get_tyre_strategy(year: int, grand_prix: str, session: str, driver: str):
        return service.get_tyre_strategy(year, grand_prix, session, driver)


    @mcp.tool()
    def get_stints(year: int, grand_prix: str, session: str, driver: str):
        return service.get_stints(year, grand_prix, session, driver)


    @mcp.tool()
    def get_tyre_compound_usage(year: int, grand_prix: str, session: str):
        return service.get_tyre_compound_usage(year, grand_prix, session)


    @mcp.tool()
    def get_average_stint_length(year: int, grand_prix: str, session: str):
        return service.get_average_stint_length(year, grand_prix, session)


    @mcp.tool()
    def get_tyre_degradation_rate(year: int, grand_prix: str, session: str, driver: str):
        return service.get_tyre_degradation_rate(year, grand_prix, session, driver)


    @mcp.tool()
    def predict_tyre_cliff(year: int, grand_prix: str, session: str, driver: str):
        return service.predict_tyre_cliff(year, grand_prix, session, driver)


    @mcp.tool()
    def compare_tyre_performance(year: int, grand_prix: str, session: str):
        return service.compare_tyre_performance(year, grand_prix, session)


    @mcp.tool()
    def tyre_strategy_comparison(year: int, grand_prix: str, session: str, driver_a: str, driver_b: str):
        return service.tyre_strategy_comparison(year, grand_prix, session, driver_a, driver_b)
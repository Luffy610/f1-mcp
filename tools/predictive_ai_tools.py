from services.predictive_ai_service import PredictiveAIService

service = PredictiveAIService()


def register_tools(mcp):

    @mcp.tool()
    def predict_overtake_probability(year: int, grand_prix: str, session: str,
                                     driver_a: str, driver_b: str):
        return service.predict_overtake_probability(year, grand_prix, session,
                                                    driver_a, driver_b)


    @mcp.tool()
    def predict_safety_car_probability(year: int, grand_prix: str, session: str):
        return service.predict_safety_car_probability(year, grand_prix, session)


    @mcp.tool()
    def predict_virtual_safety_car_probability(year: int, grand_prix: str, session: str):
        return service.predict_virtual_safety_car_probability(year, grand_prix, session)


    @mcp.tool()
    def predict_race_winner(year: int, grand_prix: str, session: str):
        return service.predict_race_winner(year, grand_prix, session)


    @mcp.tool()
    def predict_next_pit_stop(year: int, grand_prix: str, session: str, driver: str):
        return service.predict_next_pit_stop(year, grand_prix, session, driver)


    @mcp.tool()
    def predict_battle_outcome(year: int, grand_prix: str, session: str,
                               driver_a: str, driver_b: str):
        return service.predict_battle_outcome(year, grand_prix, session,
                                              driver_a, driver_b)


    @mcp.tool()
    def predict_tyre_strategy(year: int, grand_prix: str, session: str, driver: str):
        return service.predict_tyre_strategy(year, grand_prix, session, driver)


    @mcp.tool()
    def predict_lap_time(year: int, grand_prix: str, session: str, driver: str):
        return service.predict_lap_time(year, grand_prix, session, driver)


    @mcp.tool()
    def predict_race_podium(year: int, grand_prix: str, session: str):
        return service.predict_race_podium(year, grand_prix, session)


    @mcp.tool()
    def predict_driver_position_end_of_race(year: int, grand_prix: str, session: str,
                                            driver: str):
        return service.predict_driver_position_end_of_race(year, grand_prix, session,
                                                           driver)
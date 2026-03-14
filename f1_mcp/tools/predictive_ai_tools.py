from f1_mcp.services.predictive_ai_service import PredictiveAIService

service = PredictiveAIService()


def register_tools(mcp):

    """Register predictive AI tools with the MCP server."""
    @mcp.tool()
    def predict_overtake_probability(year: int, grand_prix: str, session: str,
                                     driver_a: str, driver_b: str):
        """Predict the probability of one driver overtaking another."""
        return service.predict_overtake_probability(year, grand_prix, session,
                                                    driver_a, driver_b)


    @mcp.tool()
    def predict_safety_car_probability(year: int, grand_prix: str, session: str):
        """Estimate the probability of a safety car deployment."""
        return service.predict_safety_car_probability(year, grand_prix, session)


    @mcp.tool()
    def predict_virtual_safety_car_probability(year: int, grand_prix: str, session: str):
        """Estimate the probability of a VSC deployment."""
        return service.predict_virtual_safety_car_probability(year, grand_prix, session)


    @mcp.tool()
    def predict_race_winner(year: int, grand_prix: str, session: str):
        """Predict the race winner based on average lap pace."""
        return service.predict_race_winner(year, grand_prix, session)


    @mcp.tool()
    def predict_next_pit_stop(year: int, grand_prix: str, session: str, driver: str):
        """Predict a driver's next pit stop lap based on stint intervals."""
        return service.predict_next_pit_stop(year, grand_prix, session, driver)


    @mcp.tool()
    def predict_battle_outcome(year: int, grand_prix: str, session: str,
                               driver_a: str, driver_b: str):
        """Predict which driver will win a head-to-head battle."""
        return service.predict_battle_outcome(year, grand_prix, session,
                                              driver_a, driver_b)


    @mcp.tool()
    def predict_tyre_strategy(year: int, grand_prix: str, session: str, driver: str):
        """Predict a driver's likely tyre strategy type."""
        return service.predict_tyre_strategy(year, grand_prix, session, driver)


    @mcp.tool()
    def predict_lap_time(year: int, grand_prix: str, session: str, driver: str):
        """Predict a driver's next lap time using linear regression."""
        return service.predict_lap_time(year, grand_prix, session, driver)


    @mcp.tool()
    def predict_race_podium(year: int, grand_prix: str, session: str):
        """Predict the top 3 finishers based on average race pace."""
        return service.predict_race_podium(year, grand_prix, session)


    @mcp.tool()
    def predict_driver_position_end_of_race(year: int, grand_prix: str, session: str,
                                            driver: str):
        """Predict a driver's finishing position from position trend."""
        return service.predict_driver_position_end_of_race(year, grand_prix, session,
                                                           driver)

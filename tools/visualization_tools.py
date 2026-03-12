from services.visualization_service import VisualizationService

service = VisualizationService()


def register_tools(mcp):

    @mcp.tool()
    def generate_speed_map(year: int, grand_prix: str, session: str, driver: str, lap: int):
        return service.generate_speed_map(year, grand_prix, session, driver, lap)


    @mcp.tool()
    def generate_track_dominance_map(year: int, grand_prix: str, session: str,
                                     driver_a: str, lap_a: int,
                                     driver_b: str, lap_b: int):
        return service.generate_track_dominance_map(year, grand_prix, session,
                                                    driver_a, lap_a,
                                                    driver_b, lap_b)


    @mcp.tool()
    def generate_lap_delta_plot(year: int, grand_prix: str, session: str,
                                driver_a: str, lap_a: int,
                                driver_b: str, lap_b: int):
        return service.generate_lap_delta_plot(year, grand_prix, session,
                                               driver_a, lap_a,
                                               driver_b, lap_b)


    @mcp.tool()
    def generate_tyre_degradation_plot(year: int, grand_prix: str, session: str, driver: str):
        return service.generate_tyre_degradation_plot(year, grand_prix, session, driver)


    @mcp.tool()
    def generate_sector_performance_chart(year: int, grand_prix: str, session: str, driver: str):
        return service.generate_sector_performance_chart(year, grand_prix, session, driver)


    @mcp.tool()
    def generate_race_progression_chart(year: int, grand_prix: str, session: str, driver: str):
        return service.generate_race_progression_chart(year, grand_prix, session, driver)
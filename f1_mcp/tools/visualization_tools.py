from f1_mcp.services.visualization_service import VisualizationService

service = VisualizationService()


def register_tools(mcp):

    """Register visualization and plotting tools with the MCP server."""
    @mcp.tool()
    def generate_speed_map(year: int, grand_prix: str, session: str, driver: str, lap: int):
        """Generate a speed vs distance scatter plot for a lap and save as PNG."""
        return service.generate_speed_map(year, grand_prix, session, driver, lap)


    @mcp.tool()
    def generate_track_dominance_map(year: int, grand_prix: str, session: str,
                                     driver_a: str, lap_a: int,
                                     driver_b: str, lap_b: int):
        """Generate a speed comparison overlay plot for two drivers."""
        return service.generate_track_dominance_map(year, grand_prix, session,
                                                    driver_a, lap_a,
                                                    driver_b, lap_b)


    @mcp.tool()
    def generate_lap_delta_plot(year: int, grand_prix: str, session: str,
                                driver_a: str, lap_a: int,
                                driver_b: str, lap_b: int):
        """Generate a speed delta plot between two driver laps."""
        return service.generate_lap_delta_plot(year, grand_prix, session,
                                               driver_a, lap_a,
                                               driver_b, lap_b)


    @mcp.tool()
    def generate_tyre_degradation_plot(year: int, grand_prix: str, session: str, driver: str):
        """Generate a lap time progression plot showing tyre degradation."""
        return service.generate_tyre_degradation_plot(year, grand_prix, session, driver)


    @mcp.tool()
    def generate_sector_performance_chart(year: int, grand_prix: str, session: str, driver: str):
        """Generate a bar chart of average sector times for a driver."""
        return service.generate_sector_performance_chart(year, grand_prix, session, driver)


    @mcp.tool()
    def generate_race_progression_chart(year: int, grand_prix: str, session: str, driver: str):
        """Generate a position vs lap chart for a driver's race."""
        return service.generate_race_progression_chart(year, grand_prix, session, driver)

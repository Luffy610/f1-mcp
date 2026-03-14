from f1_mcp.services.telemetry_intelligence_service import TelemetryIntelligenceService

service = TelemetryIntelligenceService()


def register_tools(mcp):

    """Register telemetry intelligence tools with the MCP server."""
    @mcp.tool()
    def corner_entry_speed(year: int, grand_prix: str, session: str, driver: str, lap: int, corner: int):
        """Get average speed in the braking zone before a corner."""
        return service.corner_entry_speed(year, grand_prix, session, driver, lap, corner)


    @mcp.tool()
    def corner_apex_speed(year: int, grand_prix: str, session: str, driver: str, lap: int, corner: int):
        """Get minimum speed through a corner's apex."""
        return service.corner_apex_speed(year, grand_prix, session, driver, lap, corner)


    @mcp.tool()
    def corner_exit_speed(year: int, grand_prix: str, session: str, driver: str, lap: int, corner: int):
        """Get average speed in the acceleration zone after a corner."""
        return service.corner_exit_speed(year, grand_prix, session, driver, lap, corner)


    @mcp.tool()
    def corner_speed_comparison(year: int, grand_prix: str, session: str,
                                driver_a: str, lap_a: int,
                                driver_b: str, lap_b: int,
                                corner: int):
        """Compare corner entry, apex, and exit speeds between two drivers."""
        return service.corner_speed_comparison(year, grand_prix, session,
                                               driver_a, lap_a,
                                               driver_b, lap_b,
                                               corner)


    @mcp.tool()
    def dirty_air_loss_estimation(year: int, grand_prix: str, session: str, driver: str, lap: int):
        """Estimate aerodynamic efficiency loss from dirty air on a lap."""
        return service.dirty_air_loss_estimation(year, grand_prix, session, driver, lap)


    @mcp.tool()
    def downforce_estimation(year: int, grand_prix: str, session: str, driver: str, lap: int):
        """Estimate relative downforce level based on speed-gear stability."""
        return service.downforce_estimation(year, grand_prix, session, driver, lap)


    @mcp.tool()
    def energy_deployment_pattern(year: int, grand_prix: str, session: str, driver: str, lap: int):
        """Analyze ERS energy deployment events and acceleration patterns."""
        return service.energy_deployment_pattern(year, grand_prix, session, driver, lap)

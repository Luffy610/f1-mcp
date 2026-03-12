from services.telemetry_intelligence_service import TelemetryIntelligenceService

service = TelemetryIntelligenceService()


def register_tools(mcp):

    @mcp.tool()
    def corner_entry_speed(year: int, grand_prix: str, session: str, driver: str, lap: int, corner: int):
        return service.corner_entry_speed(year, grand_prix, session, driver, lap, corner)


    @mcp.tool()
    def corner_apex_speed(year: int, grand_prix: str, session: str, driver: str, lap: int, corner: int):
        return service.corner_apex_speed(year, grand_prix, session, driver, lap, corner)


    @mcp.tool()
    def corner_exit_speed(year: int, grand_prix: str, session: str, driver: str, lap: int, corner: int):
        return service.corner_exit_speed(year, grand_prix, session, driver, lap, corner)


    @mcp.tool()
    def corner_speed_comparison(year: int, grand_prix: str, session: str,
                                driver_a: str, lap_a: int,
                                driver_b: str, lap_b: int,
                                corner: int):
        return service.corner_speed_comparison(year, grand_prix, session,
                                               driver_a, lap_a,
                                               driver_b, lap_b,
                                               corner)


    @mcp.tool()
    def dirty_air_loss_estimation(year: int, grand_prix: str, session: str, driver: str, lap: int):
        return service.dirty_air_loss_estimation(year, grand_prix, session, driver, lap)


    @mcp.tool()
    def downforce_estimation(year: int, grand_prix: str, session: str, driver: str, lap: int):
        return service.downforce_estimation(year, grand_prix, session, driver, lap)


    @mcp.tool()
    def energy_deployment_pattern(year: int, grand_prix: str, session: str, driver: str, lap: int):
        return service.energy_deployment_pattern(year, grand_prix, session, driver, lap)
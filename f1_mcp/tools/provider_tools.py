from f1_mcp.services.provider_service import ProviderService

service = ProviderService()


def register_tools(mcp):

    """Register data provider and utility tools with the MCP server."""
    @mcp.tool()
    def merge_fastf1_and_ergast_results(year: int, grand_prix: str, session: str):
        """Merge FastF1 session results with Ergast standings data."""
        return service.merge_fastf1_and_ergast_results(year, grand_prix, session)


    @mcp.tool()
    def validate_session_data(year: int, grand_prix: str, session: str):
        """Check if session data loaded correctly."""
        return service.validate_session_data(year, grand_prix, session)


    @mcp.tool()
    def fill_missing_telemetry(year: int, grand_prix: str, session: str,
                               driver: str, lap: int):
        """Interpolate missing values in telemetry data for a lap."""
        return service.fill_missing_telemetry(year, grand_prix, session,
                                              driver, lap)


    @mcp.tool()
    def provider_health_check():
        """Check health status of session cache, telemetry cache, and Ergast API."""
        return service.provider_health_check()

from services.provider_service import ProviderService

service = ProviderService()


def register_tools(mcp):

    @mcp.tool()
    def merge_fastf1_and_ergast_results(year: int, grand_prix: str, session: str):
        return service.merge_fastf1_and_ergast_results(year, grand_prix, session)


    @mcp.tool()
    def validate_session_data(year: int, grand_prix: str, session: str):
        return service.validate_session_data(year, grand_prix, session)


    @mcp.tool()
    def fill_missing_telemetry(year: int, grand_prix: str, session: str,
                               driver: str, lap: int):
        return service.fill_missing_telemetry(year, grand_prix, session,
                                              driver, lap)


    @mcp.tool()
    def provider_health_check():
        return service.provider_health_check()
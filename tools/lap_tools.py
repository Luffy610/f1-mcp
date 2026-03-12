from services.lap_service import LapService

service = LapService()


def register_tools(mcp):

    @mcp.tool()
    def get_all_laps(year: int, grand_prix: str, session: str):
        return service.get_all_laps(year, grand_prix, session)


    @mcp.tool()
    def get_driver_laps(year: int, grand_prix: str, session: str, driver: str):
        return service.get_driver_laps(year, grand_prix, session, driver)


    @mcp.tool()
    def get_lap_time(year: int, grand_prix: str, session: str, driver: str, lap_number: int):
        return service.get_lap_time(year, grand_prix, session, driver, lap_number)


    @mcp.tool()
    def get_fastest_lap(year: int, grand_prix: str, session: str):
        return service.get_fastest_lap(year, grand_prix, session)


    @mcp.tool()
    def get_lap_delta(year: int, grand_prix: str, session: str, driver_a: str, driver_b: str, lap_number: int):
        return service.get_lap_delta(year, grand_prix, session, driver_a, driver_b, lap_number)


    @mcp.tool()
    def get_lap_times_series(year: int, grand_prix: str, session: str, driver: str):
        return service.get_lap_times_series(year, grand_prix, session, driver)


    @mcp.tool()
    def get_clean_laps(year: int, grand_prix: str, session: str, driver: str):
        return service.get_clean_laps(year, grand_prix, session, driver)


    @mcp.tool()
    def get_deleted_laps(year: int, grand_prix: str, session: str, driver: str):
        return service.get_deleted_laps(year, grand_prix, session, driver)


    @mcp.tool()
    def get_lap_position(year: int, grand_prix: str, session: str, driver: str, lap_number: int):
        return service.get_lap_position(year, grand_prix, session, driver, lap_number)


    @mcp.tool()
    def get_lap_leader(year: int, grand_prix: str, session: str, lap_number: int):
        return service.get_lap_leader(year, grand_prix, session, lap_number)


    @mcp.tool()
    def get_lap_time_distribution(year: int, grand_prix: str, session: str):
        return service.get_lap_time_distribution(year, grand_prix, session)
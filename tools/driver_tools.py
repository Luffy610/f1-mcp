from services.driver_service import DriverService

service = DriverService()


def register_tools(mcp):

    @mcp.tool()
    def list_drivers(year: int, grand_prix: str, session: str):
        return service.list_drivers(year, grand_prix, session)


    @mcp.tool()
    def get_driver_info(year: int, grand_prix: str, session: str, driver: str):
        return service.get_driver_info(year, grand_prix, session, driver)


    @mcp.tool()
    def get_driver_team(year: int, grand_prix: str, session: str, driver: str):
        return service.get_driver_team(year, grand_prix, session, driver)


    @mcp.tool()
    def get_driver_number(year: int, grand_prix: str, session: str, driver: str):
        return service.get_driver_number(year, grand_prix, session, driver)


    @mcp.tool()
    def get_teammate(year: int, grand_prix: str, session: str, driver: str):
        return service.get_teammate(year, grand_prix, session, driver)


    @mcp.tool()
    def get_driver_grid_position(year: int, grand_prix: str, session: str, driver: str):
        return service.get_driver_grid_position(year, grand_prix, session, driver)


    @mcp.tool()
    def get_driver_finish_position(year: int, grand_prix: str, session: str, driver: str):
        return service.get_driver_finish_position(year, grand_prix, session, driver)


    @mcp.tool()
    def get_driver_points(year: int, grand_prix: str, session: str, driver: str):
        return service.get_driver_points(year, grand_prix, session, driver)


    @mcp.tool()
    def get_constructor_standings(year: int):
        return service.get_constructor_standings(year)


    @mcp.tool()
    def get_driver_standings(year: int):
        return service.get_driver_standings(year)
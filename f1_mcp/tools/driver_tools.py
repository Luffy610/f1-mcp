from f1_mcp.services.driver_service import DriverService

service = DriverService()


def register_tools(mcp):

    """Register driver information tools with the MCP server."""
    @mcp.tool()
    def list_drivers(year: int, grand_prix: str, session: str):
        """List all drivers participating in a session with codes and names."""
        return service.list_drivers(year, grand_prix, session)


    @mcp.tool()
    def get_driver_info(year: int, grand_prix: str, session: str, driver: str):
        """Get detailed driver metadata including name, team, and number."""
        return service.get_driver_info(year, grand_prix, session, driver)


    @mcp.tool()
    def get_driver_team(year: int, grand_prix: str, session: str, driver: str):
        """Get the team name for a specific driver."""
        return service.get_driver_team(year, grand_prix, session, driver)


    @mcp.tool()
    def get_driver_number(year: int, grand_prix: str, session: str, driver: str):
        """Get the car number for a specific driver."""
        return service.get_driver_number(year, grand_prix, session, driver)


    @mcp.tool()
    def get_teammate(year: int, grand_prix: str, session: str, driver: str):
        """Find the teammate of a driver based on team assignment."""
        return service.get_teammate(year, grand_prix, session, driver)


    @mcp.tool()
    def get_driver_grid_position(year: int, grand_prix: str, session: str, driver: str):
        """Get a driver's starting grid position for a session."""
        return service.get_driver_grid_position(year, grand_prix, session, driver)


    @mcp.tool()
    def get_driver_finish_position(year: int, grand_prix: str, session: str, driver: str):
        """Get a driver's finishing position in a session."""
        return service.get_driver_finish_position(year, grand_prix, session, driver)


    @mcp.tool()
    def get_driver_points(year: int, grand_prix: str, session: str, driver: str):
        """Get the points scored by a driver in a session."""
        return service.get_driver_points(year, grand_prix, session, driver)


    @mcp.tool()
    def get_constructor_standings(year: int):
        """Get constructor championship standings for a season."""
        return service.get_constructor_standings(year)


    @mcp.tool()
    def get_driver_standings(year: int):
        """Get driver championship standings for a season."""
        return service.get_driver_standings(year)
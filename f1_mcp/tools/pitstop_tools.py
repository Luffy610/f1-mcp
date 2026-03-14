from f1_mcp.services.pitstop_service import PitStopService

service = PitStopService()


def register_tools(mcp):

    """Register pit stop analysis tools with the MCP server."""
    @mcp.tool()
    def get_pit_stops(year: int, grand_prix: str, session: str):
        """Get all pit stops in the session with driver, lap, and compound."""
        return service.get_pit_stops(year, grand_prix, session)


    @mcp.tool()
    def get_pit_stop_time(year: int, grand_prix: str, session: str, driver: str):
        """Get pit stop durations for a driver across their stops."""
        return service.get_pit_stop_time(year, grand_prix, session, driver)


    @mcp.tool()
    def get_pit_lane_loss(year: int, grand_prix: str, session: str):
        """Get the average time lost in the pit lane versus a clean lap."""
        return service.get_pit_lane_loss(year, grand_prix, session)


    @mcp.tool()
    def undercut_effectiveness(year: int, grand_prix: str, session: str, driver: str):
        """Measure pace gain from pitting early (undercut) for a driver."""
        return service.undercut_effectiveness(year, grand_prix, session, driver)


    @mcp.tool()
    def overcut_effectiveness(year: int, grand_prix: str, session: str, driver: str):
        """Measure pace gain from pitting late (overcut) for a driver."""
        return service.overcut_effectiveness(year, grand_prix, session, driver)


    @mcp.tool()
    def optimal_pit_window(year: int, grand_prix: str, session: str, driver: str):
        """Find the optimal pit stop lap based on rolling lap time average."""
        return service.optimal_pit_window(year, grand_prix, session, driver)


    @mcp.tool()
    def pit_stop_summary(year: int, grand_prix: str, session: str):
        """Get pit stop count and laps for all drivers in the session."""
        return service.pit_stop_summary(year, grand_prix, session)
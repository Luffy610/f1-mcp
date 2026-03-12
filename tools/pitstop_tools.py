from services.pitstop_service import PitStopService

service = PitStopService()


def register_tools(mcp):

    @mcp.tool()
    def get_pit_stops(year: int, grand_prix: str, session: str):
        return service.get_pit_stops(year, grand_prix, session)


    @mcp.tool()
    def get_pit_stop_time(year: int, grand_prix: str, session: str, driver: str):
        return service.get_pit_stop_time(year, grand_prix, session, driver)


    @mcp.tool()
    def get_pit_lane_loss(year: int, grand_prix: str, session: str):
        return service.get_pit_lane_loss(year, grand_prix, session)


    @mcp.tool()
    def undercut_effectiveness(year: int, grand_prix: str, session: str, driver: str):
        return service.undercut_effectiveness(year, grand_prix, session, driver)


    @mcp.tool()
    def overcut_effectiveness(year: int, grand_prix: str, session: str, driver: str):
        return service.overcut_effectiveness(year, grand_prix, session, driver)


    @mcp.tool()
    def optimal_pit_window(year: int, grand_prix: str, session: str, driver: str):
        return service.optimal_pit_window(year, grand_prix, session, driver)


    @mcp.tool()
    def pit_stop_summary(year: int, grand_prix: str, session: str):
        return service.pit_stop_summary(year, grand_prix, session)
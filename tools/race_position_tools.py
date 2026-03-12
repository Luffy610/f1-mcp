from services.race_position_service import RacePositionService

service = RacePositionService()


def register_tools(mcp):

    @mcp.tool()
    def get_position_changes(year: int, grand_prix: str, session: str):
        return service.get_position_changes(year, grand_prix, session)


    @mcp.tool()
    def get_race_lead_changes(year: int, grand_prix: str, session: str):
        return service.get_race_lead_changes(year, grand_prix, session)


    @mcp.tool()
    def get_overtakes(year: int, grand_prix: str, session: str):
        return service.get_overtakes(year, grand_prix, session)


    @mcp.tool()
    def get_driver_race_progression(year: int, grand_prix: str, session: str, driver: str):
        return service.get_driver_race_progression(year, grand_prix, session, driver)


    @mcp.tool()
    def get_gap_to_leader(year: int, grand_prix: str, session: str, driver: str):
        return service.get_gap_to_leader(year, grand_prix, session, driver)


    @mcp.tool()
    def get_gap_between_drivers(year: int, grand_prix: str, session: str, driver_a: str, driver_b: str):
        return service.get_gap_between_drivers(year, grand_prix, session, driver_a, driver_b)


    @mcp.tool()
    def get_battle_detection(year: int, grand_prix: str, session: str, gap_threshold: float = 1.5):
        return service.get_battle_detection(year, grand_prix, session, gap_threshold)
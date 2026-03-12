from services.sector_service import SectorService

service = SectorService()


def register_tools(mcp):

    @mcp.tool()
    def get_sector_times(year: int, grand_prix: str, session: str, driver: str, lap_number: int):
        return service.get_sector_times(year, grand_prix, session, driver, lap_number)


    @mcp.tool()
    def get_sector_delta(year: int, grand_prix: str, session: str, driver_a: str, driver_b: str, lap_number: int):
        return service.get_sector_delta(year, grand_prix, session, driver_a, driver_b, lap_number)


    @mcp.tool()
    def get_best_sector_times(year: int, grand_prix: str, session: str):
        return service.get_best_sector_times(year, grand_prix, session)


    @mcp.tool()
    def get_driver_best_sectors(year: int, grand_prix: str, session: str, driver: str):
        return service.get_driver_best_sectors(year, grand_prix, session, driver)


    @mcp.tool()
    def sector_delta_vs_teammate(year: int, grand_prix: str, session: str, driver: str):
        return service.sector_delta_vs_teammate(year, grand_prix, session, driver)


    @mcp.tool()
    def sector_performance_summary(year: int, grand_prix: str, session: str, driver: str):
        return service.sector_performance_summary(year, grand_prix, session, driver)


    @mcp.tool()
    def sector_consistency(year: int, grand_prix: str, session: str, driver: str):
        return service.sector_consistency(year, grand_prix, session, driver)


    @mcp.tool()
    def sector_improvement_over_time(year: int, grand_prix: str, session: str, driver: str):
        return service.sector_improvement_over_time(year, grand_prix, session, driver)
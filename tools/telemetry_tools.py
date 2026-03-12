from services.telemetry_service import TelemetryService

service = TelemetryService()


def register_tools(mcp):

    @mcp.tool()
    def get_lap_telemetry(year: int, grand_prix: str, session: str, driver: str, lap: int):
        return service.get_lap_telemetry(year, grand_prix, session, driver, lap)


    @mcp.tool()
    def get_speed_trace(year: int, grand_prix: str, session: str, driver: str, lap: int):
        return service.get_speed_trace(year, grand_prix, session, driver, lap)


    @mcp.tool()
    def get_throttle_trace(year: int, grand_prix: str, session: str, driver: str, lap: int):
        return service.get_throttle_trace(year, grand_prix, session, driver, lap)


    @mcp.tool()
    def get_brake_trace(year: int, grand_prix: str, session: str, driver: str, lap: int):
        return service.get_brake_trace(year, grand_prix, session, driver, lap)


    @mcp.tool()
    def get_gear_trace(year: int, grand_prix: str, session: str, driver: str, lap: int):
        return service.get_gear_trace(year, grand_prix, session, driver, lap)


    @mcp.tool()
    def get_rpm_trace(year: int, grand_prix: str, session: str, driver: str, lap: int):
        return service.get_rpm_trace(year, grand_prix, session, driver, lap)


    @mcp.tool()
    def get_drs_usage(year: int, grand_prix: str, session: str, driver: str, lap: int):
        return service.get_drs_usage(year, grand_prix, session, driver, lap)


    @mcp.tool()
    def get_distance_telemetry(year: int, grand_prix: str, session: str, driver: str, lap: int):
        return service.get_distance_telemetry(year, grand_prix, session, driver, lap)


    @mcp.tool()
    def get_telemetry_segment(year: int, grand_prix: str, session: str, driver: str, lap: int, start: float, end: float):
        return service.get_telemetry_segment(year, grand_prix, session, driver, lap, start, end)


    @mcp.tool()
    def get_corner_telemetry(year: int, grand_prix: str, session: str, driver: str, lap: int, corner_number: int):
        return service.get_corner_telemetry(year, grand_prix, session, driver, lap, corner_number)


    @mcp.tool()
    def compare_lap_telemetry(year: int, grand_prix: str, session: str, driver_a: str, lap_a: int, driver_b: str, lap_b: int):
        return service.compare_lap_telemetry(year, grand_prix, session, driver_a, lap_a, driver_b, lap_b)


    @mcp.tool()
    def find_max_speed(year: int, grand_prix: str, session: str, driver: str, lap: int):
        return service.find_max_speed(year, grand_prix, session, driver, lap)


    @mcp.tool()
    def find_min_speed_corner(year: int, grand_prix: str, session: str, driver: str, lap: int):
        return service.find_min_speed_corner(year, grand_prix, session, driver, lap)


    @mcp.tool()
    def throttle_application_analysis(year: int, grand_prix: str, session: str, driver: str, lap: int):
        return service.throttle_application_analysis(year, grand_prix, session, driver, lap)


    @mcp.tool()
    def braking_point_analysis(year: int, grand_prix: str, session: str, driver: str, lap: int):
        return service.braking_point_analysis(year, grand_prix, session, driver, lap)
    
    @mcp.tool()
    def preload_driver_telemetry(year: int, grand_prix: str, session: str, driver: str):

        from core.session_cache import session_cache

        s = session_cache.get_session(year, grand_prix, session)

        laps = s.laps.pick_drivers(driver)

        loaded = 0

        for _, lap in laps.iterlaps():

            tel = lap.get_car_data()

            if tel is not None and not tel.empty:
                loaded += 1

        return {
            "driver": driver,
            "laps_with_telemetry": loaded
        }
    
    @mcp.tool()
    def telemetry_available(year: int, grand_prix: str, session: str, driver: str):

        from core.session_cache import session_cache

        s = session_cache.get_session(year, grand_prix, session)

        laps = s.laps.pick_drivers(driver)

        if laps.empty:
            return {"available": False}

        lap = laps.pick_fastest()

        tel = lap.get_car_data()

        return {
            "available": tel is not None and not tel.empty,
            "points": len(tel) if tel is not None else 0
        }
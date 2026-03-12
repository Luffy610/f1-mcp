from services.session_service import SessionService
from core.session_cache import session_cache

service = SessionService()


def register_tools(mcp):

    @mcp.tool()
    def list_seasons():
        return service.list_seasons()


    @mcp.tool()
    def list_grand_prix(year: int):
        return service.list_grand_prix(year)


    @mcp.tool()
    def list_sessions(year: int, grand_prix: str):
        return service.list_sessions(year, grand_prix)


    @mcp.tool()
    def get_session_info(year: int, grand_prix: str, session: str):
        return service.get_session_info(year, grand_prix, session)


    @mcp.tool()
    def get_circuit_info(year: int, grand_prix: str, session: str):
        return service.get_circuit_info(year, grand_prix, session)


    @mcp.tool()
    def get_track_length(year: int, grand_prix: str, session: str):
        return service.get_track_length(year, grand_prix, session)


    @mcp.tool()
    def get_track_layout(year: int, grand_prix: str, session: str):
        return service.get_track_layout(year, grand_prix, session)


    @mcp.tool()
    def get_session_weather(year: int, grand_prix: str, session: str):
        return service.get_session_weather(year, grand_prix, session)


    @mcp.tool()
    def get_session_start_time(year: int, grand_prix: str, session: str):
        return service.get_session_start_time(year, grand_prix, session)


    @mcp.tool()
    def get_session_flag_events(year: int, grand_prix: str, session: str):
        return service.get_session_flag_events(year, grand_prix, session)


    @mcp.tool()
    def get_track_status_changes(year: int, grand_prix: str, session: str):
        return service.get_track_status_changes(year, grand_prix, session)


    @mcp.tool()
    def get_safety_car_periods(year: int, grand_prix: str, session: str):
        return service.get_safety_car_periods(year, grand_prix, session)

    @mcp.tool()
    def cache_stats():
        """
        Returns cached sessions in memory
        """
        return session_cache.stats()


    @mcp.tool()
    def clear_cache():
        """
        Clears session cache
        """
        session_cache.clear()
        return {"status": "cache cleared"}
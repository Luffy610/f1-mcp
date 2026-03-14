from f1_mcp.services.session_service import SessionService
from f1_mcp.core.session_cache import session_cache

service = SessionService()


def register_tools(mcp):

    """Register session and schedule tools with the MCP server."""
    @mcp.tool()
    def list_seasons():
        """List all F1 seasons available in the FastF1 database."""
        return service.list_seasons()


    @mcp.tool()
    def list_grand_prix(year: int):
        """List all Grand Prix events for a given season."""
        return service.list_grand_prix(year)


    @mcp.tool()
    def list_sessions(year: int, grand_prix: str):
        """List available sessions (FP1, FP2, FP3, Q, R) for a Grand Prix."""
        return service.list_sessions(year, grand_prix)


    @mcp.tool()
    def get_session_info(year: int, grand_prix: str, session: str):
        """Get metadata for a session including event name, location, and date."""
        return service.get_session_info(year, grand_prix, session)


    @mcp.tool()
    def get_circuit_info(year: int, grand_prix: str, session: str):
        """Get circuit corner positions, marshal lights, and marshal sectors."""
        return service.get_circuit_info(year, grand_prix, session)


    @mcp.tool()
    def get_track_length(year: int, grand_prix: str, session: str):
        """Get approximate track length in meters."""
        return service.get_track_length(year, grand_prix, session)


    @mcp.tool()
    def get_track_layout(year: int, grand_prix: str, session: str):
        """Get corner positions and distances for the track layout."""
        return service.get_track_layout(year, grand_prix, session)


    @mcp.tool()
    def get_session_weather(year: int, grand_prix: str, session: str):
        """Get weather data recorded during the session."""
        return service.get_session_weather(year, grand_prix, session)


    @mcp.tool()
    def get_session_start_time(year: int, grand_prix: str, session: str):
        """Get the official start time of a session."""
        return service.get_session_start_time(year, grand_prix, session)


    @mcp.tool()
    def get_session_flag_events(year: int, grand_prix: str, session: str):
        """Get all flag and track status events during a session."""
        return service.get_session_flag_events(year, grand_prix, session)


    @mcp.tool()
    def get_track_status_changes(year: int, grand_prix: str, session: str):
        """Get track status transitions (green, yellow, red, SC, VSC)."""
        return service.get_track_status_changes(year, grand_prix, session)


    @mcp.tool()
    def get_safety_car_periods(year: int, grand_prix: str, session: str):
        """Get safety car, VSC, and red flag periods with timing."""
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
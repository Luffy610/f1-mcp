import fastf1
from datetime import datetime
from functools import lru_cache
from f1_mcp.core.session_cache import session_cache
from f1_mcp.core.serialization import sanitize_df, sanitize_value
from f1_mcp.connectors.fastf1_loader import FastF1Loader


class SessionService:
    """Provides session, circuit, and schedule information for F1 events."""

    def __init__(self):
        self.loader = FastF1Loader()

    def load(self, year: int, gp: str, session: str):
        """Load a session via the shared session cache."""
        return session_cache.get_session(year, gp, session)

    # -----------------------------
    # Schedule helpers (cached)
    # -----------------------------

    @lru_cache(maxsize=32)
    def get_schedule(self, year: int):
        """Return the full event schedule for a given season year."""
        return fastf1.get_event_schedule(year)

    # -----------------------------
    # TOOL 1
    # -----------------------------

    def list_seasons(self):
        """
        Return available seasons supported by FastF1.
        FastF1 supports seasons from 2018 onward with full telemetry,
        and schedule data from 2018+.
        """
        current_year = datetime.now().year
        return list(range(2018, current_year + 1))

    # -----------------------------
    # TOOL 2
    # -----------------------------

    def list_grand_prix(self, year: int):
        """Return a list of Grand Prix event names for a given season."""
        schedule = self.get_schedule(year)

        return schedule["EventName"].tolist()

    # -----------------------------
    # TOOL 3
    # -----------------------------

    def list_sessions(self, year: int, grand_prix: str):
        """List available session types for a Grand Prix."""
        event = fastf1.get_event(year, grand_prix)

        sessions = []

        for attr in dir(event):
            if attr.startswith("Session"):
                value = getattr(event, attr)

                if value:
                    sessions.append(sanitize_value(value))

        return sessions

    # -----------------------------
    # TOOL 4
    # -----------------------------

    def get_session_info(self, year: int, gp: str, session: str):
        """Get metadata for a session including event name, location, and date."""
        s = self.load(year, gp, session)

        return {
            "event_name": str(s.event.EventName),
            "year": int(s.event.year),
            "round": int(s.event.RoundNumber),
            "location": str(s.event.Location),
            "country": str(s.event.Country),
            "session_name": str(s.name),
            "date": str(s.date)
        }

    # -----------------------------
    # TOOL 5
    # -----------------------------

    def get_circuit_info(self, year, gp, session):
        """Get circuit corner positions, marshal lights, and marshal sectors."""
        s = self.load(year, gp, session)

        circuit = s.get_circuit_info()

        if circuit is None:
            return {}

        marshal_lights = getattr(circuit, "marshal_lights", None)
        marshal_sectors = getattr(circuit, "marshal_sectors", None)

        return {
            "corners": sanitize_df(circuit.corners),
            "marshal_lights": sanitize_df(marshal_lights) if marshal_lights is not None else None,
            "marshal_sectors": sanitize_df(marshal_sectors) if marshal_sectors is not None else None,
        }

    # -----------------------------
    # TOOL 6
    # -----------------------------

    def get_track_length(self, year, gp, session):
        """Get approximate track length in meters from circuit data."""
        s = self.load(year, gp, session)

        circuit = s.get_circuit_info()

        if circuit is not None and hasattr(circuit, "corners") and not circuit.corners.empty:
            if "Distance" in circuit.corners.columns:
                # Last corner distance as approximation
                last_corner_dist = float(circuit.corners["Distance"].iloc[-1])
                return {
                    "track_length_meters": last_corner_dist,
                    "note": "Approximate (last corner distance)"
                }

        return None

    # -----------------------------
    # TOOL 7
    # -----------------------------

    def get_track_layout(self, year, gp, session):
        """Get corner positions and distances for the track layout."""
        s = self.load(year, gp, session)

        circuit = s.get_circuit_info()

        if circuit is None:
            return {}

        return sanitize_df(circuit.corners)

    # -----------------------------
    # TOOL 8
    # -----------------------------

    def get_session_weather(self, year, gp, session):
        """Get weather data recorded during the session."""
        s = self.load(year, gp, session)

        weather = s.weather_data

        if weather is None:
            return []

        return sanitize_df(weather)

    # -----------------------------
    # TOOL 9
    # -----------------------------

    def get_session_start_time(self, year, gp, session):
        """Get the official start time of a session."""
        s = self.load(year, gp, session)

        return str(s.date)

    # -----------------------------
    # TOOL 10
    # -----------------------------

    def get_session_flag_events(self, year, gp, session):
        """Get all flag and track status events during a session."""
        s = self.load(year, gp, session)

        status = s.track_status

        if status is None:
            return []

        return sanitize_df(status)

    # -----------------------------
    # TOOL 11
    # -----------------------------

    def get_track_status_changes(self, year, gp, session):
        """Get track status transitions during a session."""
        s = self.load(year, gp, session)

        status = s.track_status

        if status is None:
            return []

        return sanitize_df(status)

    # -----------------------------
    # TOOL 12
    # -----------------------------

    def get_safety_car_periods(self, year, gp, session):
        """Get safety car, VSC, and red flag periods with timing."""
        s = self.load(year, gp, session)

        status = s.track_status

        if status is None:
            return []

        status_labels = {
            "4": "Safety Car",
            "5": "Red Flag",
            "6": "VSC Deployed",
            "7": "VSC Ending",
        }

        # Filter for SC, Red Flag, VSC events
        safety_events = status[
            status["Status"].astype(str).isin(status_labels.keys())
        ].copy()

        if safety_events.empty:
            return []

        safety_events["Type"] = safety_events["Status"].astype(str).map(status_labels)

        return sanitize_df(safety_events)
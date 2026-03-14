import fastf1
import pandas as pd
from typing import Dict, Any


class FastF1Loader:
    """
    Loader responsible for retrieving F1 session data using FastF1.
    Ensures telemetry, laps, weather, and messages are loaded.
    """

    def __init__(self):
        # Ensure FastF1 cache is enabled
        fastf1.Cache.enable_cache("cache")

    def load_session(self, year: int, grand_prix: str, session_type: str):
        """
        Load a session with full telemetry support.
        """

        session = fastf1.get_session(year, grand_prix, session_type)

        session.load(
            laps=True,
            telemetry=True,
            weather=True,
            messages=True
        )

        return session

    def get_session_metadata(self, session) -> Dict[str, Any]:
        """
        Extract metadata from a FastF1 session.
        """

        return {
            "event_name": session.event.EventName,
            "year": session.event.year,
            "round": session.event.RoundNumber,
            "location": session.event.Location,
            "country": session.event.Country,
            "session_name": session.name,
            "session_date": str(session.date)
        }

    def get_drivers(self, session):
        """
        Return list of driver codes.
        """
        return session.drivers

    def get_driver_info(self, session, driver):
        """
        Return driver metadata.
        """

        try:
            return session.get_driver(driver)
        except Exception:
            return None

    def get_laps(self, session) -> pd.DataFrame:
        """
        Return laps dataframe.
        """

        if session.laps is None:
            return pd.DataFrame()

        return session.laps

    def get_weather(self, session) -> pd.DataFrame:
        """
        Return weather dataframe.
        """

        if session.weather_data is None:
            return pd.DataFrame()

        return session.weather_data

    def get_track_status(self, session) -> pd.DataFrame:
        """
        Return track status dataframe.
        """

        if session.track_status is None:
            return pd.DataFrame()

        return session.track_status

    def get_results(self, session):
        """
        Return race results dataframe.
        """

        if session.results is None:
            return None

        return session.results

    def get_circuit_info(self, session):
        """
        Return circuit information.
        """

        try:
            return session.get_circuit_info()
        except Exception:
            return None
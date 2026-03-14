import threading
from typing import Dict, Tuple
from f1_mcp.core.session_cache import session_cache


class TelemetryCacheManager:
    """Thread-safe cache for per-lap telemetry DataFrames."""

    def __init__(self):
        self._cache: Dict[Tuple, object] = {}
        self._lock = threading.Lock()

    def _key(self, year, gp, session, driver, lap):
        """Build a string cache key from telemetry lookup parameters."""
        return f"{year}_{gp}_{session}_{driver}_{lap}"

    def get_lap_telemetry(self, year, gp, session, driver, lap_number):
        """Return cached telemetry for a specific lap, loading from session data if needed."""
        key = self._key(year, gp, session, driver, lap_number)

        if key in self._cache:
            return self._cache[key]

        with self._lock:

            if key not in self._cache:

                s = session_cache.get_session(year, gp, session)

                laps = s.laps.pick_drivers(driver)

                lap = laps[laps["LapNumber"] == lap_number]

                if lap.empty:
                    return None

                telemetry = lap.iloc[0].get_car_data()

                if telemetry is None or telemetry.empty:
                    return None

                telemetry = telemetry.add_distance()

                self._cache[key] = telemetry

        return self._cache[key]

    def clear(self):
        """Remove all entries from the telemetry cache."""
        self._cache.clear()

    def stats(self):
        """Return cache statistics including count and cached keys."""
        return {
            "cached_telemetry": len(self._cache),
            "keys": list(self._cache.keys())
        }


telemetry_cache = TelemetryCacheManager()
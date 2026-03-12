import threading
from typing import Dict, Tuple
from connectors.fastf1_loader import FastF1Loader


class SessionCacheManager:
    """
    Central session cache to avoid repeated FastF1 loads.
    """

    def __init__(self):
        self.loader = FastF1Loader()
        self._cache: Dict[Tuple[int, str, str], object] = {}
        self._lock = threading.Lock()

    def _cache_key(self, year: int, gp: str, session: str):
        """Build a normalized cache key tuple from session parameters."""
        return (year, gp.lower(), session.upper())

    def get_session(self, year: int, gp: str, session: str):
        """Return a cached session, loading it from FastF1 if not already cached."""
        key = self._cache_key(year, gp, session)

        if key in self._cache:
            return self._cache[key]

        with self._lock:
            if key not in self._cache:
                session_obj = self.loader.load_session(year, gp, session)
                self._cache[key] = session_obj

        return self._cache[key]

    def clear(self):
        """Remove all entries from the session cache."""
        self._cache.clear()

    def stats(self):
        """Return cache statistics including count and cached keys."""
        return {
            "cached_sessions": len(self._cache),
            "keys": list(self._cache.keys())
        }


# Singleton instance
session_cache = SessionCacheManager()
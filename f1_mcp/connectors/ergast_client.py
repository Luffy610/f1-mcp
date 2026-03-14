import fastf1
import pandas as pd
from functools import lru_cache
from f1_mcp.core.serialization import sanitize_value


def _df_to_records(df):
    """Convert an Ergast DataFrame to a list of JSON-safe dicts."""
    if df is None or (hasattr(df, 'empty') and df.empty):
        return []
    records = df.to_dict(orient="records")
    sanitized = []
    for record in records:
        clean = {k: sanitize_value(v) for k, v in record.items()}
        sanitized.append(clean)
    return sanitized


class ErgastClient:
    """Client for querying historical F1 data via the Ergast API."""

    def __init__(self):
        self.ergast = fastf1.ergast.Ergast()

    @lru_cache(maxsize=32)
    def get_driver_standings(self, year: int):
        """Return driver championship standings for the given season."""
        data = self.ergast.get_driver_standings(season=year)
        if not data.content:
            return []
        return _df_to_records(data.content[0])

    @lru_cache(maxsize=32)
    def get_constructor_standings(self, year: int):
        """Return constructor championship standings for the given season."""
        data = self.ergast.get_constructor_standings(season=year)
        if not data.content:
            return []
        return _df_to_records(data.content[0])

    @lru_cache(maxsize=32)
    def get_driver_info(self, year: int):
        """Return biographical info for all drivers in the given season."""
        data = self.ergast.get_driver_info(season=year)
        if not data.content:
            return []
        return _df_to_records(data.content[0]) if isinstance(data.content[0], pd.DataFrame) else data.content
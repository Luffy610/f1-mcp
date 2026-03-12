import pandas as pd
from core.session_cache import session_cache
from core.telemetry_cache import telemetry_cache
from core.serialization import sanitize_df
from connectors.ergast_client import ErgastClient


class ProviderService:

    def __init__(self):
        self.ergast = ErgastClient()

    def load_session(self, year, gp, session):
        return session_cache.get_session(year, gp, session)

    # 115
    def merge_fastf1_and_ergast_results(self, year, gp, session):

        s = self.load_session(year, gp, session)

        fastf1_results = s.results

        ergast_results = self.ergast.get_driver_standings(year)

        ergast_df = pd.DataFrame(ergast_results)

        merged = fastf1_results.merge(
            ergast_df,
            left_on="Abbreviation",
            right_on="driverCode",
            how="left"
        )

        return sanitize_df(merged)

    # 116
    def validate_session_data(self, year, gp, session):

        s = self.load_session(year, gp, session)

        checks = {}

        checks["laps_loaded"] = s.laps is not None
        checks["drivers_available"] = len(s.drivers) > 0
        checks["results_available"] = s.results is not None
        checks["weather_data_available"] = s.weather_data is not None

        return checks

    # 117
    def fill_missing_telemetry(self, year, gp, session, driver, lap):

        tel = telemetry_cache.get_lap_telemetry(year, gp, session, driver, lap)

        if tel is None:
            return None

        df = pd.DataFrame(tel).infer_objects(copy=False)
        numeric_cols = df.select_dtypes(include="number").columns
        df[numeric_cols] = df[numeric_cols].interpolate()
        filled = df

        # Sanitize for JSON — telemetry contains Timestamps
        from core.serialization import sanitize_value
        result = filled.to_dict(orient="list")
        sanitized = {}
        for k, v in result.items():
            if isinstance(v, list) and len(v) > 0:
                if isinstance(v[0], (pd.Timestamp, pd.Timedelta)):
                    sanitized[k] = [str(x) if pd.notna(x) else None for x in v]
                else:
                    sanitized[k] = [sanitize_value(x) for x in v]
            else:
                sanitized[k] = v
        return sanitized

    # 118
    def provider_health_check(self):

        health = {}

        try:
            cache_stats = session_cache.stats()
            health["session_cache"] = "healthy" if cache_stats else "empty"
        except Exception:
            health["session_cache"] = "error"

        try:
            tel_stats = telemetry_cache.stats()
            health["telemetry_cache"] = "healthy" if tel_stats else "empty"
        except Exception:
            health["telemetry_cache"] = "error"

        try:
            ergast = ErgastClient()
            test = ergast.get_driver_standings(2023)
            health["ergast_api"] = "healthy" if test else "no_data"
        except Exception:
            health["ergast_api"] = "error"

        return health
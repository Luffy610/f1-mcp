import pandas as pd
from f1_mcp.core.session_cache import session_cache


class SectorService:

    """Service for sector time analysis and sector comparisons."""
    def load_session(self, year, gp, session):
        """Load a session via the shared session cache."""
        return session_cache.get_session(year, gp, session)

    def get_laps(self, year, gp, session):
        """Get the laps DataFrame for a session."""
        s = self.load_session(year, gp, session)
        return s.laps

    def _sector_columns(self, laps: pd.DataFrame):
        """Get the list of sector time column names from a laps DataFrame."""
        return [c for c in laps.columns if c.startswith("Sector") and c.endswith("Time")]

    # 34
    def get_sector_times(self, year, gp, session, driver, lap_number):
        """Get sector times for a driver on a specific lap."""
        laps = self.get_laps(year, gp, session)

        row = laps[(laps["Driver"] == driver) & (laps["LapNumber"] == lap_number)]

        if row.empty:
            return None

        sectors = self._sector_columns(laps)

        result = {}
        for s in sectors:
            val = row[s].values[0]
            result[s] = str(val) if pd.notna(val) else None

        return result

    # 35
    def get_sector_delta(self, year, gp, session, driver_a, driver_b, lap_number):
        """Get sector time deltas between two drivers on a specific lap."""
        laps = self.get_laps(year, gp, session)

        lap_a = laps[(laps["Driver"] == driver_a) & (laps["LapNumber"] == lap_number)]
        lap_b = laps[(laps["Driver"] == driver_b) & (laps["LapNumber"] == lap_number)]

        if lap_a.empty or lap_b.empty:
            return None

        sectors = self._sector_columns(laps)

        deltas = {}

        for s in sectors:
            a = lap_a[s].values[0]
            b = lap_b[s].values[0]

            if pd.isna(a) or pd.isna(b):
                deltas[s] = None
            else:
                deltas[s] = str(a - b)

        return deltas

    # 36
    def get_best_sector_times(self, year, gp, session):
        """Get the best sector times across all drivers in the session."""
        laps = self.get_laps(year, gp, session)

        sectors = self._sector_columns(laps)

        best = {}

        for s in sectors:

            valid = laps.dropna(subset=[s])

            if valid.empty:
                best[s] = None
                continue

            idx = valid[s].idxmin()

            best[s] = {
                "driver": valid.loc[idx, "Driver"],
                "lap": int(valid.loc[idx, "LapNumber"]),
                "time": str(valid.loc[idx, s])
            }

        return best

    # 37
    def get_driver_best_sectors(self, year, gp, session, driver):
        """Get a driver's personal best sector times."""
        laps = self.get_laps(year, gp, session)

        drv = laps[laps["Driver"] == driver]

        if drv.empty:
            return None

        sectors = self._sector_columns(laps)

        best = {}

        for s in sectors:
            valid = drv.dropna(subset=[s])

            if valid.empty:
                best[s] = None
                continue

            best[s] = str(valid[s].min())

        return best

    # 38
    def sector_delta_vs_teammate(self, year, gp, session, driver):
        """Get average sector time deltas between a driver and teammate."""
        s = self.load_session(year, gp, session)
        laps = s.laps

        info = s.get_driver(driver)
        team = info.get("TeamName")

        teammate = None
        for num in s.drivers:
            d_info = s.get_driver(num)
            abbrev = d_info.get("Abbreviation")
            if abbrev == driver:
                continue
            if d_info.get("TeamName") == team:
                teammate = abbrev
                break

        if teammate is None:
            return None

        drv = laps[laps["Driver"] == driver]
        mate = laps[laps["Driver"] == teammate]

        sectors = self._sector_columns(laps)

        delta = {}

        for sct in sectors:

            a = drv[sct].dropna().dt.total_seconds()
            b = mate[sct].dropna().dt.total_seconds()

            if a.empty or b.empty:
                delta[sct] = None
            else:
                delta[sct] = float(a.mean() - b.mean())

        return {
            "driver": driver,
            "teammate": teammate,
            "sector_delta_seconds": delta
        }

    # 39
    def sector_performance_summary(self, year, gp, session, driver):
        """Get best, average, and median sector times for a driver."""
        laps = self.get_laps(year, gp, session)

        drv = laps[laps["Driver"] == driver]

        sectors = self._sector_columns(laps)

        summary = {}

        for s in sectors:

            sec = drv[s].dropna().dt.total_seconds()

            if sec.empty:
                summary[s] = None
                continue

            summary[s] = {
                "best": float(sec.min()),
                "average": float(sec.mean()),
                "median": float(sec.median())
            }

        return summary

    # 40
    def sector_consistency(self, year, gp, session, driver):
        """Get sector time standard deviation as a consistency metric."""
        laps = self.get_laps(year, gp, session)

        drv = laps[laps["Driver"] == driver]

        sectors = self._sector_columns(laps)

        consistency = {}

        for s in sectors:

            sec = drv[s].dropna().dt.total_seconds()

            if sec.empty:
                consistency[s] = None
                continue

            consistency[s] = float(sec.std())

        return consistency

    # 41
    def sector_improvement_over_time(self, year, gp, session, driver):
        """Get sector time improvement from first to last lap."""
        laps = self.get_laps(year, gp, session)

        drv = laps[laps["Driver"] == driver].sort_values("LapNumber")

        sectors = self._sector_columns(laps)

        improvement = {}

        for s in sectors:

            sec = drv[s].dropna().dt.total_seconds()

            if len(sec) < 2:
                improvement[s] = None
                continue

            improvement[s] = float(sec.iloc[0] - sec.iloc[-1])

        return improvement
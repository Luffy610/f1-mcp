import numpy as np
import pandas as pd
from f1_mcp.core.session_cache import session_cache


class PitStopService:
    """Analyzes pit stop timing, strategy effectiveness, and pit lane time losses."""

    def load_session(self, year, gp, session):
        """Load a session via the shared session cache."""
        return session_cache.get_session(year, gp, session)

    def get_laps(self, year, gp, session):
        """Get the laps DataFrame for a session."""
        s = self.load_session(year, gp, session)
        return s.laps

    # 65
    def get_pit_stops(self, year, gp, session):
        """Get all pit stops in the session with driver, lap, and compound."""
        laps = self.get_laps(year, gp, session)

        pit = laps[laps["PitInTime"].notna()]

        stops = []

        for _, lap in pit.iterrows():
            stops.append({
                "driver": lap["Driver"],
                "lap": int(lap["LapNumber"]),
                "stint": int(lap["Stint"]),
                "compound_before": lap["Compound"],
                "pit_in_time": str(lap["PitInTime"])
            })

        return stops

    # 66
    def get_pit_stop_time(self, year, gp, session, driver):
        """Get pit stop durations for a driver across their stops."""
        laps = self.get_laps(year, gp, session)

        drv = laps[laps["Driver"] == driver].sort_values("LapNumber")

        pit_in_laps = drv[drv["PitInTime"].notna()]

        results = []

        for _, lap in pit_in_laps.iterrows():
            pit_in_time = lap["PitInTime"]
            lap_num = lap["LapNumber"]

            # Find the next lap which should have PitOutTime
            next_lap = drv[drv["LapNumber"] == lap_num + 1]

            if not next_lap.empty and pd.notna(next_lap.iloc[0]["PitOutTime"]):
                stop_time = next_lap.iloc[0]["PitOutTime"] - pit_in_time
                results.append({
                    "lap": int(lap_num),
                    "pit_stop_time": str(stop_time)
                })
            else:
                # Fallback: estimate from lap time vs median clean lap time
                clean = drv[drv["PitInTime"].isna() & drv["PitOutTime"].isna()]
                clean = clean.dropna(subset=["LapTime"])
                if not clean.empty and pd.notna(lap["LapTime"]):
                    median_clean = clean["LapTime"].dt.total_seconds().median()
                    pit_loss = lap["LapTime"].total_seconds() - median_clean
                    results.append({
                        "lap": int(lap_num),
                        "pit_stop_time": f"~{pit_loss:.3f}s (estimated)"
                    })

        return results

    # 67
    def get_pit_lane_loss(self, year, gp, session):
        """Get the average time lost in the pit lane versus a clean lap."""
        laps = self.get_laps(year, gp, session)

        # Clean laps: no pit in or pit out
        clean = laps[laps["PitInTime"].isna() & laps["PitOutTime"].isna()]
        clean = clean.dropna(subset=["LapTime"])

        if clean.empty:
            return None

        avg_clean = clean["LapTime"].dt.total_seconds().median()

        # Pit laps: laps where driver entered pit
        pit = laps[laps["PitInTime"].notna()].dropna(subset=["LapTime"])

        losses = []

        for _, lap in pit.iterrows():
            pit_lap_time = lap["LapTime"].total_seconds()
            loss = pit_lap_time - avg_clean
            if loss > 0:
                losses.append(loss)

        if not losses:
            return None

        return {
            "average_pit_lane_loss_seconds": float(np.mean(losses)),
            "min_loss": float(np.min(losses)),
            "max_loss": float(np.max(losses))
        }

    # 68
    def undercut_effectiveness(self, year, gp, session, driver):
        """Measure pace gain from pitting early (undercut) for a driver."""
        laps = self.get_laps(year, gp, session)

        drv = laps[laps["Driver"] == driver]

        pit = drv[drv["PitInTime"].notna()]

        if pit.empty:
            return None

        results = []

        for _, lap in pit.iterrows():

            before = drv[drv["LapNumber"] < lap["LapNumber"]].tail(3)
            after = drv[drv["LapNumber"] > lap["LapNumber"]].head(3)

            if before.empty or after.empty:
                continue

            before_avg = before["LapTime"].dt.total_seconds().mean()
            after_avg = after["LapTime"].dt.total_seconds().mean()

            results.append(before_avg - after_avg)

        if not results:
            return None

        return {
            "average_time_gain": float(np.mean(results))
        }

    # 69
    def overcut_effectiveness(self, year, gp, session, driver):
        """Measure pace gain from pitting late (overcut) for a driver."""
        laps = self.get_laps(year, gp, session)

        drv = laps[laps["Driver"] == driver]

        pit = drv[drv["PitInTime"].notna()]

        if pit.empty:
            return None

        gains = []

        for _, lap in pit.iterrows():

            before = drv[drv["LapNumber"] < lap["LapNumber"]].tail(5)
            late = drv[drv["LapNumber"] > lap["LapNumber"]].head(1)

            if before.empty or late.empty:
                continue

            before_avg = before["LapTime"].dt.total_seconds().mean()
            late_time = late["LapTime"].dt.total_seconds().values[0]

            gains.append(before_avg - late_time)

        if not gains:
            return None

        return {
            "average_overcut_gain": float(np.mean(gains))
        }

    # 70
    def optimal_pit_window(self, year, gp, session, driver):
        """Find the optimal pit stop lap based on rolling lap time average."""
        laps = self.get_laps(year, gp, session)

        drv = laps[laps["Driver"] == driver]

        drv = drv.dropna(subset=["LapTime"])

        times = drv["LapTime"].dt.total_seconds()

        rolling = times.rolling(5).mean()

        best = rolling.idxmin()

        if best is None:
            return None

        return {
            "optimal_pit_lap": int(drv.loc[best]["LapNumber"])
        }

    # 71
    def pit_stop_summary(self, year, gp, session):
        """Get pit stop count and laps for all drivers in the session."""
        laps = self.get_laps(year, gp, session)

        pit = laps[laps["PitInTime"].notna()]

        drivers = pit["Driver"].unique()

        summary = {}

        for d in drivers:

            stops = pit[pit["Driver"] == d]

            summary[d] = {
                "pit_stops": int(len(stops)),
                "laps": [int(x) for x in stops["LapNumber"].tolist()]
            }

        return summary
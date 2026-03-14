import numpy as np
import pandas as pd
from f1_mcp.core.session_cache import session_cache


class StrategyService:
    """Provides tyre strategy analysis including stint data, degradation, and compound comparisons."""

    def load_session(self, year, gp, session):
        """Load a session via the shared session cache."""
        return session_cache.get_session(year, gp, session)

    def get_laps(self, year, gp, session):
        """Get the laps DataFrame for a session."""
        s = self.load_session(year, gp, session)
        return s.laps

    # 57
    def get_tyre_strategy(self, year, gp, session, driver):
        """Get a driver's tyre strategy with compounds and stint details."""
        laps = self.get_laps(year, gp, session)

        drv = laps[laps["Driver"] == driver]

        strategy = []

        for stint, data in drv.groupby("Stint"):

            compound = data["Compound"].iloc[0]

            strategy.append({
                "stint": int(stint),
                "compound": compound,
                "start_lap": int(data["LapNumber"].min()),
                "end_lap": int(data["LapNumber"].max()),
                "laps": len(data)
            })

        return strategy

    # 58
    def get_stints(self, year, gp, session, driver):
        """Get stint breakdown with compound and lap count for a driver."""
        laps = self.get_laps(year, gp, session)

        drv = laps[laps["Driver"] == driver]

        stints = []

        for stint, data in drv.groupby("Stint"):

            stints.append({
                "stint": int(stint),
                "compound": data["Compound"].iloc[0],
                "laps": len(data)
            })

        return stints

    # 59
    def get_tyre_compound_usage(self, year, gp, session):
        """Get total lap count per tyre compound across the session."""
        laps = self.get_laps(year, gp, session)

        usage = laps.groupby("Compound").size()

        return usage.to_dict()

    # 60
    def get_average_stint_length(self, year, gp, session):
        """Get the average stint length across all drivers."""
        laps = self.get_laps(year, gp, session)

        stint_lengths = laps.groupby(["Driver", "Stint"]).size()

        return float(stint_lengths.mean())

    # 61
    def get_tyre_degradation_rate(self, year, gp, session, driver):
        """Get lap time degradation slope per compound for a driver."""
        laps = self.get_laps(year, gp, session)

        drv = laps[laps["Driver"] == driver]

        drv = drv.dropna(subset=["LapTime"])

        degradation = {}

        for compound, data in drv.groupby("Compound"):

            times = data["LapTime"].dt.total_seconds()

            if len(times) < 2:
                continue

            lap_numbers = data["LapNumber"]

            slope = np.polyfit(lap_numbers, times, 1)[0]

            degradation[compound] = float(slope)

        return degradation

    # 62
    def predict_tyre_cliff(self, year, gp, session, driver):
        """Predict the lap where each compound's performance drops off."""
        laps = self.get_laps(year, gp, session)

        drv = laps[laps["Driver"] == driver]

        drv = drv.dropna(subset=["LapTime"])

        cliffs = {}

        for compound, data in drv.groupby("Compound"):

            times = data["LapTime"].dt.total_seconds()

            if len(times) < 5:
                continue

            deltas = np.diff(times)

            cliff_index = np.argmax(deltas)

            cliffs[compound] = int(data.iloc[cliff_index]["LapNumber"])

        return cliffs

    # 63
    def compare_tyre_performance(self, year, gp, session):
        """Compare average and best lap times across tyre compounds."""
        laps = self.get_laps(year, gp, session)

        laps = laps.dropna(subset=["LapTime"])

        performance = {}

        for compound, data in laps.groupby("Compound"):

            times = data["LapTime"].dt.total_seconds()

            performance[compound] = {
                "average_lap": float(times.mean()),
                "best_lap": float(times.min()),
                "lap_count": int(len(times))
            }

        return performance

    # 64
    def tyre_strategy_comparison(self, year, gp, session, driver_a, driver_b):
        """Compare tyre strategies between two drivers."""
        strat_a = self.get_tyre_strategy(year, gp, session, driver_a)
        strat_b = self.get_tyre_strategy(year, gp, session, driver_b)

        return {
            "driver_a": driver_a,
            "strategy_a": strat_a,
            "driver_b": driver_b,
            "strategy_b": strat_b
        }
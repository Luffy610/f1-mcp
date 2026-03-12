import numpy as np
import pandas as pd
from core.session_cache import session_cache


class StrategyIntelligenceService:
    """Predicts and simulates race strategies including undercut/overcut viability and optimal stop counts."""

    def load_session(self, year, gp, session):
        return session_cache.get_session(year, gp, session)

    def get_laps(self, year, gp, session):
        s = self.load_session(year, gp, session)
        return s.laps

    # 79
    def predict_undercut_success(self, year, gp, session, driver):

        laps = self.get_laps(year, gp, session)

        drv = laps[laps["Driver"] == driver].dropna(subset=["LapTime"])

        if drv.empty:
            return None

        stint_groups = drv.groupby("Stint")

        gains = []

        for stint, data in stint_groups:

            if len(data) < 5:
                continue

            early = data.head(3)["LapTime"].dt.total_seconds().mean()
            late = data.tail(3)["LapTime"].dt.total_seconds().mean()

            gains.append(late - early)

        if not gains:
            return None

        avg_gain = float(np.mean(gains))

        return {
            "driver": driver,
            "expected_undercut_gain_seconds": avg_gain,
            "undercut_viable": avg_gain > 0
        }

    # 80
    def predict_overcut_success(self, year, gp, session, driver):

        laps = self.get_laps(year, gp, session)

        drv = laps[laps["Driver"] == driver].dropna(subset=["LapTime"])

        if drv.empty:
            return None

        gains = []

        for stint, data in drv.groupby("Stint"):

            if len(data) < 5:
                continue

            early = data.head(3)["LapTime"].dt.total_seconds().mean()
            late = data.tail(3)["LapTime"].dt.total_seconds().mean()

            gains.append(early - late)

        if not gains:
            return None

        avg = float(np.mean(gains))

        return {
            "driver": driver,
            "expected_overcut_gain_seconds": avg,
            "overcut_viable": avg > 0
        }

    # 81
    def race_strategy_simulation(self, year, gp, session, driver):

        laps = self.get_laps(year, gp, session)

        drv = laps[laps["Driver"] == driver].dropna(subset=["LapTime"])

        total_time = drv["LapTime"].dt.total_seconds().sum()

        pit_stops = drv["PitInTime"].notna().sum()

        avg_lap = drv["LapTime"].dt.total_seconds().mean()

        simulated = total_time + (pit_stops * 20)

        return {
            "driver": driver,
            "actual_race_time": float(total_time),
            "simulated_strategy_time": float(simulated),
            "pit_stops": int(pit_stops),
            "avg_lap_time": float(avg_lap)
        }

    # 82
    def two_stop_vs_one_stop_simulation(self, year, gp, session, driver):

        laps = self.get_laps(year, gp, session)

        drv = laps[laps["Driver"] == driver].dropna(subset=["LapTime"])

        race_time = drv["LapTime"].dt.total_seconds().sum()

        avg_lap = drv["LapTime"].dt.total_seconds().mean()

        one_stop = race_time + 20
        two_stop = race_time + 40

        degradation_penalty = avg_lap * 0.02 * len(drv)

        one_stop_adjusted = one_stop + degradation_penalty

        return {
            "driver": driver,
            "one_stop_time": float(one_stop_adjusted),
            "two_stop_time": float(two_stop),
            "recommended_strategy": "two_stop" if two_stop < one_stop_adjusted else "one_stop"
        }

    # 83
    def predict_optimal_strategy(self, year, gp, session, driver):

        laps = self.get_laps(year, gp, session)

        drv = laps[laps["Driver"] == driver].dropna(subset=["LapTime"])

        degradation = drv.groupby("Stint")["LapTime"].apply(
            lambda x: x.dt.total_seconds().diff().mean()
        )

        avg_deg = degradation.mean()

        if avg_deg > 0.15:
            strategy = "two_stop"
        elif avg_deg > 0.07:
            strategy = "flexible"
        else:
            strategy = "one_stop"

        return {
            "driver": driver,
            "average_degradation": float(avg_deg),
            "recommended_strategy": strategy
        }

    # 84
    def track_position_importance(self, year, gp, session):

        laps = self.get_laps(year, gp, session)

        laps = laps.dropna(subset=["Position", "LapTime"])

        correlation = np.corrcoef(
            laps["Position"],
            laps["LapTime"].dt.total_seconds()
        )[0][1]

        importance = abs(correlation)

        if importance > 0.7:
            level = "high"
        elif importance > 0.4:
            level = "medium"
        else:
            level = "low"

        return {
            "track_position_correlation": float(correlation),
            "importance_level": level
        }
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from f1_mcp.core.session_cache import session_cache


class PredictiveAIService:

    """Service for ML-based race predictions and probabilistic analysis."""
    def load_session(self, year, gp, session):
        """Load a session via the shared session cache."""
        return session_cache.get_session(year, gp, session)

    def get_laps(self, year, gp, session):
        """Get the laps DataFrame for a session."""
        s = self.load_session(year, gp, session)
        return s.laps

    # 99
    def predict_overtake_probability(self, year, gp, session, driver_a, driver_b):
        """Predict the probability of one driver overtaking another."""
        laps = self.get_laps(year, gp, session)

        a = laps[laps["Driver"] == driver_a].dropna(subset=["LapTime"])
        b = laps[laps["Driver"] == driver_b].dropna(subset=["LapTime"])

        if a.empty or b.empty:
            return None

        pace_a = a["LapTime"].dt.total_seconds().mean()
        pace_b = b["LapTime"].dt.total_seconds().mean()

        delta = pace_b - pace_a

        probability = 1 / (1 + np.exp(-delta))

        return {
            "driver_a": driver_a,
            "driver_b": driver_b,
            "overtake_probability": float(probability)
        }

    # 100
    def predict_safety_car_probability(self, year, gp, session):
        """Estimate the probability of a safety car deployment."""
        laps = self.get_laps(year, gp, session)

        incidents = laps["TrackStatus"].astype(str).str.contains("4").sum()

        probability = incidents / len(laps) if len(laps) else 0

        return {
            "safety_car_probability": float(probability)
        }

    # 101
    def predict_virtual_safety_car_probability(self, year, gp, session):
        """Estimate the probability of a VSC deployment."""
        laps = self.get_laps(year, gp, session)

        incidents = laps["TrackStatus"].astype(str).str.contains("6").sum()

        probability = incidents / len(laps) if len(laps) else 0

        return {
            "virtual_safety_car_probability": float(probability)
        }

    # 102
    def predict_race_winner(self, year, gp, session):
        """Predict the race winner based on average lap pace."""
        laps = self.get_laps(year, gp, session)

        laps = laps.dropna(subset=["LapTime"])

        avg_pace = laps.groupby("Driver")["LapTime"].apply(
            lambda x: x.dt.total_seconds().mean()
        )

        winner = avg_pace.idxmin()

        return {
            "predicted_winner": winner
        }

    # 103
    def predict_next_pit_stop(self, year, gp, session, driver):
        """Predict a driver's next pit stop lap based on stint intervals."""
        laps = self.get_laps(year, gp, session)

        drv = laps[laps["Driver"] == driver]

        pit_laps = drv[drv["PitInTime"].notna()]["LapNumber"]

        if len(pit_laps) < 2:
            return None

        intervals = pit_laps.diff().dropna()

        next_lap = pit_laps.iloc[-1] + intervals.mean()

        return {
            "driver": driver,
            "predicted_next_pit_lap": int(next_lap)
        }

    # 104
    def predict_battle_outcome(self, year, gp, session, driver_a, driver_b):
        """Predict which driver will win a head-to-head battle."""
        laps = self.get_laps(year, gp, session)

        a = laps[laps["Driver"] == driver_a].dropna(subset=["LapTime"])
        b = laps[laps["Driver"] == driver_b].dropna(subset=["LapTime"])

        if a.empty or b.empty:
            return None

        pace_a = a["LapTime"].dt.total_seconds().mean()
        pace_b = b["LapTime"].dt.total_seconds().mean()

        winner = driver_a if pace_a < pace_b else driver_b

        return {
            "predicted_battle_winner": winner
        }

    # 105
    def predict_tyre_strategy(self, year, gp, session, driver):
        """Predict a driver's likely tyre strategy type."""
        laps = self.get_laps(year, gp, session)

        drv = laps[laps["Driver"] == driver]

        stint_lengths = drv.groupby("Stint").size()

        avg = stint_lengths.mean()

        if avg < 10:
            strategy = "aggressive_multi_stop"
        elif avg < 18:
            strategy = "two_stop"
        else:
            strategy = "one_stop"

        return {
            "driver": driver,
            "predicted_strategy": strategy
        }

    # 106
    def predict_lap_time(self, year, gp, session, driver):
        """Predict a driver's next lap time using linear regression."""
        laps = self.get_laps(year, gp, session)

        drv = laps[laps["Driver"] == driver].dropna(subset=["LapTime"])

        if len(drv) < 5:
            return None

        X = drv["LapNumber"].values.reshape(-1, 1)
        y = drv["LapTime"].dt.total_seconds().values

        model = LinearRegression()
        model.fit(X, y)

        next_lap = drv["LapNumber"].max() + 1

        pred = model.predict([[next_lap]])[0]

        return {
            "driver": driver,
            "predicted_lap_time_seconds": float(pred)
        }

    # 107
    def predict_race_podium(self, year, gp, session):
        """Predict the top 3 finishers based on average race pace."""
        laps = self.get_laps(year, gp, session)

        laps = laps.dropna(subset=["LapTime"])

        avg_pace = laps.groupby("Driver")["LapTime"].apply(
            lambda x: x.dt.total_seconds().mean()
        )

        podium = avg_pace.sort_values().head(3).index.tolist()

        return {
            "predicted_podium": podium
        }

    # 108
    def predict_driver_position_end_of_race(self, year, gp, session, driver):
        """Predict a driver's finishing position from position trend."""
        laps = self.get_laps(year, gp, session)

        drv = laps[laps["Driver"] == driver].dropna(subset=["Position"])

        if drv.empty:
            return None

        trend = np.polyfit(drv["LapNumber"], drv["Position"], 1)[0]

        last_pos = drv["Position"].iloc[-1]

        s = self.load_session(year, gp, session)
        num_drivers = len(s.drivers)

        predicted = max(1, min(num_drivers, int(last_pos + trend)))

        return {
            "driver": driver,
            "predicted_finish_position": predicted
        }
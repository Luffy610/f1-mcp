import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from core.session_cache import session_cache


class AdvancedAnalyticsService:

    def load_session(self, year, gp, session):
        return session_cache.get_session(year, gp, session)

    def get_laps(self, year, gp, session):
        s = self.load_session(year, gp, session)
        return s.laps

    # 92
    def driver_consistency_score(self, year, gp, session, driver):

        laps = self.get_laps(year, gp, session)

        drv = laps[laps["Driver"] == driver].dropna(subset=["LapTime"])

        times = drv["LapTime"].dt.total_seconds()

        if len(times) < 2:
            return None

        std = np.std(times)
        mean = np.mean(times)

        score = 1 - (std / mean)

        return {
            "driver": driver,
            "consistency_score": float(score)
        }

    # 93
    def driver_aggression_index(self, year, gp, session, driver):

        laps = self.get_laps(year, gp, session)

        drv = laps[laps["Driver"] == driver].sort_values("LapNumber")

        pos = drv["Position"].dropna()

        changes = pos.diff()

        overtakes = (changes < 0).sum()

        total_laps = len(pos)

        if total_laps == 0:
            return None

        index = overtakes / total_laps

        return {
            "driver": driver,
            "aggression_index": float(index)
        }

    # 94
    def driver_risk_index(self, year, gp, session, driver):

        laps = self.get_laps(year, gp, session)

        drv = laps[laps["Driver"] == driver]

        deleted = drv["Deleted"].sum() if "Deleted" in drv else 0

        total = len(drv)

        if total == 0:
            return None

        risk = deleted / total

        return {
            "driver": driver,
            "risk_index": float(risk)
        }

    # 95
    def qualifying_improvement_analysis(self, year, gp, driver):

        session = self.load_session(year, gp, "Q")

        laps = session.laps

        drv = laps[laps["Driver"] == driver].dropna(subset=["LapTime"])

        drv = drv.sort_values("LapNumber")

        times = drv["LapTime"].dt.total_seconds()

        if len(times) < 2:
            return None

        improvement = times.iloc[0] - times.min()

        return {
            "driver": driver,
            "qualifying_improvement_seconds": float(improvement)
        }

    # 96
    def lap_time_variance(self, year, gp, session, driver):

        laps = self.get_laps(year, gp, session)

        drv = laps[laps["Driver"] == driver].dropna(subset=["LapTime"])

        times = drv["LapTime"].dt.total_seconds()

        if len(times) < 2:
            return None

        return {
            "driver": driver,
            "lap_time_variance": float(np.var(times))
        }

    # 97
    def performance_trend(self, year, gp, session, driver):

        laps = self.get_laps(year, gp, session)

        drv = laps[laps["Driver"] == driver].dropna(subset=["LapTime"])

        drv = drv.sort_values("LapNumber")

        laps_num = drv["LapNumber"]
        times = drv["LapTime"].dt.total_seconds()

        if len(times) < 3:
            return None

        slope = np.polyfit(laps_num, times, 1)[0]

        if slope < -0.01:
            trend = "improving"
        elif slope > 0.01:
            trend = "declining"
        else:
            trend = "stable"

        return {
            "driver": driver,
            "trend_slope": float(slope),
            "trend": trend
        }

    # 98
    def driver_style_clustering(self, year, gp, session):

        laps = self.get_laps(year, gp, session)

        laps = laps.dropna(subset=["LapTime"])

        drivers = []

        features = []

        for driver, drv in laps.groupby("Driver"):

            times = drv["LapTime"].dt.total_seconds()

            if len(times) < 5:
                continue

            mean = np.mean(times)
            std = np.std(times)

            drivers.append(driver)
            features.append([mean, std])

        if len(features) < 2:
            return None

        kmeans = KMeans(n_clusters=2, n_init=10)

        labels = kmeans.fit_predict(features)

        result = []

        for i, driver in enumerate(drivers):
            result.append({
                "driver": driver,
                "cluster": int(labels[i])
            })

        return result
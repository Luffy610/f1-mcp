import pandas as pd
import numpy as np
from core.session_cache import session_cache


class RacePositionService:
    """Tracks race position changes, overtakes, gaps, and on-track battles between drivers."""

    def load_session(self, year, gp, session):
        return session_cache.get_session(year, gp, session)

    def get_laps(self, year, gp, session):
        s = self.load_session(year, gp, session)
        return s.laps

    # 72
    def get_position_changes(self, year, gp, session):

        laps = self.get_laps(year, gp, session)

        changes = []

        for driver, drv in laps.groupby("Driver"):

            drv = drv.sort_values("LapNumber")

            positions = drv["Position"].dropna()

            if len(positions) < 2:
                continue

            diff = positions.diff()

            overtakes = int((diff < 0).sum())
            losses = int((diff > 0).sum())

            changes.append({
                "driver": driver,
                "positions_gained": overtakes,
                "positions_lost": losses,
                "net_change": int(positions.iloc[0] - positions.iloc[-1])
            })

        return changes

    # 73
    def get_race_lead_changes(self, year, gp, session):

        laps = self.get_laps(year, gp, session)

        leaders = laps[laps["Position"] == 1]

        leaders = leaders.sort_values("LapNumber")

        lead_changes = []

        prev_driver = None

        for _, row in leaders.iterrows():

            driver = row["Driver"]

            if prev_driver is None:
                prev_driver = driver
                continue

            if driver != prev_driver:

                lead_changes.append({
                    "lap": int(row["LapNumber"]),
                    "new_leader": driver
                })

                prev_driver = driver

        return lead_changes

    # 74
    def get_overtakes(self, year, gp, session):

        laps = self.get_laps(year, gp, session)

        overtakes = []

        for driver, drv in laps.groupby("Driver"):

            drv = drv.sort_values("LapNumber")

            positions = drv[["LapNumber", "Position"]].dropna()

            diff = positions["Position"].diff()

            for i, d in enumerate(diff):

                if pd.notna(d) and d < 0:

                    overtakes.append({
                        "driver": driver,
                        "lap": int(positions.iloc[i]["LapNumber"]),
                        "positions_gained": int(abs(d))
                    })

        return overtakes

    # 75
    def get_driver_race_progression(self, year, gp, session, driver):

        laps = self.get_laps(year, gp, session)

        drv = laps[laps["Driver"] == driver]

        drv = drv.sort_values("LapNumber")

        progression = []

        for _, row in drv.iterrows():

            if pd.isna(row["Position"]):
                continue

            progression.append({
                "lap": int(row["LapNumber"]),
                "position": int(row["Position"])
            })

        return progression

    # 76
    def get_gap_to_leader(self, year, gp, session, driver):

        laps = self.get_laps(year, gp, session)

        # Build leader time per lap
        leaders = laps[laps["Position"] == 1][["LapNumber", "Time"]].dropna()
        leader_times = dict(zip(leaders["LapNumber"], leaders["Time"]))

        drv = laps[laps["Driver"] == driver].sort_values("LapNumber")

        gaps = []

        for _, row in drv.iterrows():

            if pd.isna(row["Time"]):
                continue

            lap_num = row["LapNumber"]
            leader_time = leader_times.get(lap_num)

            if leader_time is None or pd.isna(leader_time):
                continue

            gap = (row["Time"] - leader_time).total_seconds()

            gaps.append({
                "lap": int(lap_num),
                "gap_seconds": float(gap)
            })

        return gaps

    # 77
    def get_gap_between_drivers(self, year, gp, session, driver_a, driver_b):

        laps = self.get_laps(year, gp, session)

        a = laps[laps["Driver"] == driver_a]
        b = laps[laps["Driver"] == driver_b]

        merged = pd.merge(
            a[["LapNumber", "LapTime"]],
            b[["LapNumber", "LapTime"]],
            on="LapNumber",
            suffixes=("_a", "_b")
        )

        merged = merged.dropna()

        gaps = []

        for _, row in merged.iterrows():

            delta = row["LapTime_a"] - row["LapTime_b"]

            gaps.append({
                "lap": int(row["LapNumber"]),
                "gap_seconds": float(delta.total_seconds())
            })

        return gaps

    # 78
    def get_battle_detection(self, year, gp, session, gap_threshold=1.5):

        laps = self.get_laps(year, gp, session)

        laps = laps.dropna(subset=["Position", "LapTime"])

        battles = []

        for lap_number, lap in laps.groupby("LapNumber"):

            lap = lap.sort_values("Position")

            for i in range(len(lap) - 1):

                d1 = lap.iloc[i]
                d2 = lap.iloc[i + 1]

                gap = abs(
                    d1["LapTime"].total_seconds() -
                    d2["LapTime"].total_seconds()
                )

                if gap < gap_threshold:

                    battles.append({
                        "lap": int(lap_number),
                        "driver_a": d1["Driver"],
                        "driver_b": d2["Driver"],
                        "gap_seconds": float(gap)
                    })

        return battles
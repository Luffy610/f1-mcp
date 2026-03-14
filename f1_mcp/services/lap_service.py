import pandas as pd
from f1_mcp.core.session_cache import session_cache
from f1_mcp.core.serialization import sanitize_df


class LapService:

    """Service for lap time analysis and lap data retrieval."""
    def load_session(self, year, gp, session):
        """Load a session via the shared session cache."""
        return session_cache.get_session(year, gp, session)

    def get_laps(self, year, gp, session):
        """Get the laps DataFrame for a session."""
        s = self.load_session(year, gp, session)
        return s.laps

    # TOOL 23
    def get_all_laps(self, year, gp, session):
        """Get all lap data for every driver in a session."""
        laps = self.get_laps(year, gp, session)

        if laps is None:
            return []

        return sanitize_df(laps)

    # TOOL 24
    def get_driver_laps(self, year, gp, session, driver):
        """Get all lap data for a specific driver."""
        laps = self.get_laps(year, gp, session)

        drv_laps = laps[laps["Driver"] == driver]

        return sanitize_df(drv_laps)

    # TOOL 25
    def get_lap_time(self, year, gp, session, driver, lap_number):
        """Get the lap time for a specific driver on a specific lap."""
        laps = self.get_laps(year, gp, session)

        lap = laps[
            (laps["Driver"] == driver) &
            (laps["LapNumber"] == lap_number)
        ]

        if lap.empty:
            return None

        return lap["LapTime"].astype(str).values[0]

    # TOOL 26
    def get_fastest_lap(self, year, gp, session):
        """Get the fastest lap of the session with driver and time."""
        laps = self.get_laps(year, gp, session)

        fastest = laps.pick_fastest()

        if fastest is None:
            return None

        lap_num = fastest["LapNumber"]
        if pd.isna(lap_num):
            return None

        return {
            "driver": fastest["Driver"],
            "lap_number": int(lap_num),
            "lap_time": str(fastest["LapTime"])
        }

    # TOOL 27
    def get_lap_delta(self, year, gp, session, driver_a, driver_b, lap_number):
        """Get the lap time difference between two drivers on a specific lap."""
        laps = self.get_laps(year, gp, session)

        lap_a = laps[
            (laps["Driver"] == driver_a) &
            (laps["LapNumber"] == lap_number)
        ]

        lap_b = laps[
            (laps["Driver"] == driver_b) &
            (laps["LapNumber"] == lap_number)
        ]

        if lap_a.empty or lap_b.empty:
            return None

        delta = lap_a["LapTime"].values[0] - lap_b["LapTime"].values[0]

        return str(delta)

    # TOOL 28
    def get_lap_times_series(self, year, gp, session, driver):
        """Get the full series of lap times for a driver."""
        laps = self.get_laps(year, gp, session)

        drv_laps = laps[laps["Driver"] == driver]

        data = []

        for _, lap in drv_laps.iterrows():
            data.append({
                "lap": int(lap["LapNumber"]),
                "lap_time": str(lap["LapTime"])
            })

        return data

    # TOOL 29
    def get_clean_laps(self, year, gp, session, driver):
        """Get only clean laps (green track status) for a driver."""
        laps = self.get_laps(year, gp, session)

        drv_laps = laps[laps["Driver"] == driver]

        clean = drv_laps[drv_laps["TrackStatus"] == "1"]

        return sanitize_df(clean)

    # TOOL 30
    def get_deleted_laps(self, year, gp, session, driver):
        """Get laps deleted for track limits for a driver."""
        laps = self.get_laps(year, gp, session)

        drv_laps = laps[laps["Driver"] == driver]

        deleted = drv_laps[drv_laps["Deleted"] == True]

        return sanitize_df(deleted)

    # TOOL 31
    def get_lap_position(self, year, gp, session, driver, lap_number):
        """Get a driver's race position on a specific lap."""
        laps = self.get_laps(year, gp, session)

        lap = laps[
            (laps["Driver"] == driver) &
            (laps["LapNumber"] == lap_number)
        ]

        if lap.empty:
            return None

        pos = lap["Position"].values[0]
        if pd.isna(pos):
            return None
        return int(pos)

    # TOOL 32
    def get_lap_leader(self, year, gp, session, lap_number):
        """Get the race leader on a specific lap."""
        laps = self.get_laps(year, gp, session)

        lap = laps[
            (laps["LapNumber"] == lap_number) &
            (laps["Position"] == 1)
        ]

        if lap.empty:
            return None

        return lap["Driver"].values[0]

    # TOOL 33
    def get_lap_time_distribution(self, year, gp, session):
        """Get statistical distribution of lap times across the session."""
        laps = self.get_laps(year, gp, session)

        if laps.empty:
            return {}

        lap_times = laps["LapTime"].dropna()

        seconds = lap_times.dt.total_seconds()

        return {
            "min": float(seconds.min()),
            "max": float(seconds.max()),
            "mean": float(seconds.mean()),
            "median": float(seconds.median()),
            "std": float(seconds.std())
        }
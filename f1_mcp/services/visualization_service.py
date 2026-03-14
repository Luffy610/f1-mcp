import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from f1_mcp.core.session_cache import session_cache
from f1_mcp.core.telemetry_cache import telemetry_cache


class VisualizationService:

    """Service for generating race analysis plots and charts."""
    def __init__(self):
        self.plot_dir = os.environ.get(
            "F1_PLOT_DIR",
            os.path.join(os.path.expanduser("~"), ".f1-mcp", "plots")
        )
        os.makedirs(self.plot_dir, exist_ok=True)

    def load_session(self, year, gp, session):
        """Load a session via the shared session cache."""
        return session_cache.get_session(year, gp, session)

    # 109
    def generate_speed_map(self, year, gp, session, driver, lap):
        """Generate a speed vs distance scatter plot and save as PNG."""
        tel = telemetry_cache.get_lap_telemetry(year, gp, session, driver, lap)

        if tel is None or tel.empty:
            return {"error": "Telemetry unavailable"}

        fig, ax = plt.subplots()

        ax.scatter(
            tel["Distance"],
            tel["Speed"],
            c=tel["Speed"],
            s=5
        )

        ax.set_title(f"{driver} Speed Map")
        ax.set_xlabel("Distance")
        ax.set_ylabel("Speed")

        path = f"{self.plot_dir}/speed_map_{driver}_{lap}.png"

        plt.savefig(path)
        plt.close()

        return {"plot_path": path}

    # 110
    def generate_track_dominance_map(self, year, gp, session, driver_a, lap_a, driver_b, lap_b):
        """Generate a speed comparison overlay plot for two drivers."""
        tel_a = telemetry_cache.get_lap_telemetry(year, gp, session, driver_a, lap_a)
        tel_b = telemetry_cache.get_lap_telemetry(year, gp, session, driver_b, lap_b)

        if tel_a is None or tel_a.empty or tel_b is None or tel_b.empty:
            return {"error": "Telemetry unavailable"}

        fig, ax = plt.subplots()

        ax.plot(tel_a["Distance"], tel_a["Speed"], label=driver_a)
        ax.plot(tel_b["Distance"], tel_b["Speed"], label=driver_b)

        ax.set_title("Track Dominance Map")
        ax.set_xlabel("Distance")
        ax.set_ylabel("Speed")
        ax.legend()

        path = f"{self.plot_dir}/track_dominance_{driver_a}_{driver_b}.png"

        plt.savefig(path)
        plt.close()

        return {"plot_path": path}

    # 111
    def generate_lap_delta_plot(self, year, gp, session, driver_a, lap_a, driver_b, lap_b):
        """Generate a speed delta plot between two driver laps."""
        tel_a = telemetry_cache.get_lap_telemetry(year, gp, session, driver_a, lap_a)
        tel_b = telemetry_cache.get_lap_telemetry(year, gp, session, driver_b, lap_b)

        if tel_a is None or tel_a.empty or tel_b is None or tel_b.empty:
            return {"error": "Telemetry unavailable"}

        # Interpolate to common distance scale to handle different-length telemetry
        common_dist = np.linspace(
            max(tel_a["Distance"].min(), tel_b["Distance"].min()),
            min(tel_a["Distance"].max(), tel_b["Distance"].max()),
            min(len(tel_a), len(tel_b))
        )

        speed_a = np.interp(common_dist, tel_a["Distance"].values, tel_a["Speed"].values)
        speed_b = np.interp(common_dist, tel_b["Distance"].values, tel_b["Speed"].values)

        delta = speed_a - speed_b

        fig, ax = plt.subplots()

        ax.plot(common_dist, delta)
        ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)

        ax.set_title(f"Speed Delta: {driver_a} vs {driver_b}")
        ax.set_xlabel("Distance (m)")
        ax.set_ylabel(f"Speed Delta (km/h) [+ve = {driver_a} faster]")

        path = f"{self.plot_dir}/lap_delta_{driver_a}_{driver_b}.png"

        plt.savefig(path)
        plt.close()

        return {"plot_path": path}

    # 112
    def generate_tyre_degradation_plot(self, year, gp, session, driver):
        """Generate a lap time progression plot showing tyre degradation."""
        s = self.load_session(year, gp, session)

        laps = s.laps
        if laps is None or laps.empty:
            return {"error": "No lap data available"}

        drv = laps[laps["Driver"] == driver].dropna(subset=["LapTime"])

        times = drv["LapTime"].dt.total_seconds()

        fig, ax = plt.subplots()

        ax.plot(drv["LapNumber"], times)

        ax.set_title(f"{driver} Tyre Degradation")
        ax.set_xlabel("Lap")
        ax.set_ylabel("Lap Time")

        path = f"{self.plot_dir}/tyre_deg_{driver}.png"

        plt.savefig(path)
        plt.close()

        return {"plot_path": path}

    # 113
    def generate_sector_performance_chart(self, year, gp, session, driver):
        """Generate a bar chart of average sector times."""
        s = self.load_session(year, gp, session)

        laps = s.laps
        if laps is None or laps.empty:
            return {"error": "No lap data available"}

        drv = laps[laps["Driver"] == driver]

        sectors = [
            drv["Sector1Time"].dt.total_seconds().mean(),
            drv["Sector2Time"].dt.total_seconds().mean(),
            drv["Sector3Time"].dt.total_seconds().mean()
        ]

        fig, ax = plt.subplots()

        ax.bar(["S1", "S2", "S3"], sectors)

        ax.set_title(f"{driver} Sector Performance")
        ax.set_ylabel("Time")

        path = f"{self.plot_dir}/sector_perf_{driver}.png"

        plt.savefig(path)
        plt.close()

        return {"plot_path": path}

    # 114
    def generate_race_progression_chart(self, year, gp, session, driver):
        """Generate a position vs lap chart for a driver's race."""
        s = self.load_session(year, gp, session)

        laps = s.laps
        if laps is None or laps.empty:
            return {"error": "No lap data available"}

        drv = laps[laps["Driver"] == driver]

        fig, ax = plt.subplots()

        ax.plot(drv["LapNumber"], drv["Position"])

        ax.set_title(f"{driver} Race Progression")
        ax.set_xlabel("Lap")
        ax.set_ylabel("Position")

        ax.invert_yaxis()

        path = f"{self.plot_dir}/race_progression_{driver}.png"

        plt.savefig(path)
        plt.close()

        return {"plot_path": path}
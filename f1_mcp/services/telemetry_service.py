import numpy as np
import pandas as pd
from f1_mcp.core.telemetry_cache import telemetry_cache
from f1_mcp.core.session_cache import session_cache
from f1_mcp.core.serialization import sanitize_value


class TelemetryService:

    """Service for car telemetry data retrieval and analysis."""
    def load_session(self, year, gp, session):
        """Load a session via the shared session cache."""
        return session_cache.get_session(year, gp, session)

    def _sanitize_tel_dict(self, d):
        """Sanitize a telemetry dict-of-lists for JSON serialization."""
        result = {}
        for k, v in d.items():
            if isinstance(v, list) and len(v) > 0:
                if isinstance(v[0], (pd.Timestamp, pd.Timedelta)):
                    result[k] = [str(x) if pd.notna(x) else None for x in v]
                else:
                    result[k] = [sanitize_value(x) for x in v]
            else:
                result[k] = v
        return result

    def get_lap_telemetry(self, year, gp, session, driver, lap):
        """Get full car telemetry data for a specific lap."""
        tel = telemetry_cache.get_lap_telemetry(year, gp, session, driver, lap)

        if tel is None:
            return None

        return self._sanitize_tel_dict(tel.to_dict(orient="list"))

    def _get_tel(self, year, gp, session, driver, lap):
        """Get raw telemetry DataFrame for a lap from cache."""
        return telemetry_cache.get_lap_telemetry(year, gp, session, driver, lap)

    # 43
    def get_speed_trace(self, year, gp, session, driver, lap):
        """Get speed values across a lap as a list."""
        tel = self._get_tel(year, gp, session, driver, lap)
        if tel is None or tel.empty:
            return None

        return tel["Speed"].tolist()

    # 44
    def get_throttle_trace(self, year, gp, session, driver, lap):
        """Get throttle application values across a lap."""
        tel = self._get_tel(year, gp, session, driver, lap)
        if tel is None or tel.empty:
            return None

        return tel["Throttle"].tolist()

    # 45
    def get_brake_trace(self, year, gp, session, driver, lap):
        """Get brake application values across a lap."""
        tel = self._get_tel(year, gp, session, driver, lap)
        if tel is None or tel.empty:
            return None

        return tel["Brake"].tolist()

    # 46
    def get_gear_trace(self, year, gp, session, driver, lap):
        """Get gear selection values across a lap."""
        tel = self._get_tel(year, gp, session, driver, lap)
        if tel is None or tel.empty:
            return None

        return tel["nGear"].tolist()

    # 47
    def get_rpm_trace(self, year, gp, session, driver, lap):
        """Get engine RPM values across a lap."""
        tel = self._get_tel(year, gp, session, driver, lap)

        if tel is None or tel.empty or "RPM" not in tel:
            return None

        return tel["RPM"].tolist()

    # 48
    def get_drs_usage(self, year, gp, session, driver, lap):
        """Get DRS activation status across a lap."""
        tel = self._get_tel(year, gp, session, driver, lap)

        if tel is None or tel.empty or "DRS" not in tel:
            return None

        return tel["DRS"].tolist()

    # 49
    def get_distance_telemetry(self, year, gp, session, driver, lap):
        """Get distance-from-start values across a lap."""
        tel = self._get_tel(year, gp, session, driver, lap)
        if tel is None or tel.empty:
            return None

        return tel["Distance"].tolist()

    # 50
    def get_telemetry_segment(self, year, gp, session, driver, lap, start, end):
        """Get telemetry data for a specific distance segment."""
        tel = self._get_tel(year, gp, session, driver, lap)

        if tel is None or tel.empty:
            return None

        seg = tel[(tel["Distance"] >= start) & (tel["Distance"] <= end)]

        return self._sanitize_tel_dict(seg.to_dict(orient="list"))

    # 51
    def get_corner_telemetry(self, year, gp, session, driver, lap, corner_number):
        """Get telemetry data around a specific corner."""
        s = self.load_session(year, gp, session)

        circuit = s.get_circuit_info()

        if circuit is None:
            return None

        corner = circuit.corners[circuit.corners["Number"] == corner_number]

        if corner.empty:
            return None

        distance = corner.iloc[0]["Distance"]

        tel = self._get_tel(year, gp, session, driver, lap)

        if tel is None or tel.empty:
            return None

        window = tel[
            (tel["Distance"] >= distance - 50) &
            (tel["Distance"] <= distance + 50)
        ]

        return self._sanitize_tel_dict(window.to_dict(orient="list"))

    # 52
    def compare_lap_telemetry(self, year, gp, session, driver_a, lap_a, driver_b, lap_b):
        """Compare speed traces between two driver-lap combinations."""
        tel_a = self._get_tel(year, gp, session, driver_a, lap_a)
        tel_b = self._get_tel(year, gp, session, driver_b, lap_b)

        if tel_a is None or tel_a.empty or tel_b is None or tel_b.empty:
            return {"error": "Telemetry unavailable"}

        return {
            "driver_a_speed": tel_a["Speed"].tolist(),
            "driver_b_speed": tel_b["Speed"].tolist(),
            "distance": tel_a["Distance"].tolist()
        }

    # 53
    def find_max_speed(self, year, gp, session, driver, lap):
        """Find the maximum speed achieved during a lap."""
        tel = self._get_tel(year, gp, session, driver, lap)

        if tel is None or tel.empty:
            return None

        return float(np.max(tel["Speed"]))

    # 54
    def find_min_speed_corner(self, year, gp, session, driver, lap):
        """Find the lowest speed point during a lap."""
        tel = self._get_tel(year, gp, session, driver, lap)

        if tel is None or tel.empty:
            return None

        idx = tel["Speed"].idxmin()

        return {
            "speed": float(tel.loc[idx]["Speed"]),
            "distance": float(tel.loc[idx]["Distance"])
        }

    # 55
    def throttle_application_analysis(self, year, gp, session, driver, lap):
        """Analyze throttle usage statistics for a lap."""
        tel = self._get_tel(year, gp, session, driver, lap)

        if tel is None or tel.empty:
            return None

        throttle = tel["Throttle"]

        return {
            "avg_throttle": float(np.mean(throttle)),
            "max_throttle": float(np.max(throttle)),
            "throttle_std": float(np.std(throttle))
        }

    # 56
    def braking_point_analysis(self, year, gp, session, driver, lap):
        """Analyze braking events and average brake pressure for a lap."""
        tel = self._get_tel(year, gp, session, driver, lap)

        if tel is None or tel.empty:
            return None

        braking_points = tel[tel["Brake"] > 0]

        return {
            "brake_events": len(braking_points),
            "avg_brake_pressure": float(np.mean(braking_points["Brake"])) if not braking_points.empty else 0
        }
import numpy as np
from core.telemetry_cache import telemetry_cache
from core.session_cache import session_cache


class TelemetryIntelligenceService:

    def load_session(self, year, gp, session):
        return session_cache.get_session(year, gp, session)

    def get_telemetry(self, year, gp, session, driver, lap):

        tel = telemetry_cache.get_lap_telemetry(year, gp, session, driver, lap)

        if tel is None or tel.empty:
            raise ValueError("Telemetry not available for this lap")

        return tel

    def _get_corner_distance(self, session_obj, corner_number):

        circuit = session_obj.get_circuit_info()

        if circuit is None:
            return None

        corner = circuit.corners[circuit.corners["Number"] == corner_number]

        if corner.empty:
            return None

        return corner.iloc[0]["Distance"]

    # 85
    def corner_entry_speed(self, year, gp, session, driver, lap, corner):

        s = self.load_session(year, gp, session)

        dist = self._get_corner_distance(s, corner)

        tel = self.get_telemetry(year, gp, session, driver, lap)

        entry = tel[
            (tel["Distance"] >= dist - 80) &
            (tel["Distance"] <= dist - 20)
        ]

        return float(entry["Speed"].mean())

    # 86
    def corner_apex_speed(self, year, gp, session, driver, lap, corner):

        s = self.load_session(year, gp, session)

        dist = self._get_corner_distance(s, corner)

        tel = self.get_telemetry(year, gp, session, driver, lap)

        apex = tel[
            (tel["Distance"] >= dist - 10) &
            (tel["Distance"] <= dist + 10)
        ]

        return float(apex["Speed"].min())

    # 87
    def corner_exit_speed(self, year, gp, session, driver, lap, corner):

        s = self.load_session(year, gp, session)

        dist = self._get_corner_distance(s, corner)

        tel = self.get_telemetry(year, gp, session, driver, lap)

        exit_zone = tel[
            (tel["Distance"] >= dist + 20) &
            (tel["Distance"] <= dist + 80)
        ]

        return float(exit_zone["Speed"].mean())

    # 88
    def corner_speed_comparison(self, year, gp, session, driver_a, lap_a, driver_b, lap_b, corner):

        entry_a = self.corner_entry_speed(year, gp, session, driver_a, lap_a, corner)
        entry_b = self.corner_entry_speed(year, gp, session, driver_b, lap_b, corner)

        apex_a = self.corner_apex_speed(year, gp, session, driver_a, lap_a, corner)
        apex_b = self.corner_apex_speed(year, gp, session, driver_b, lap_b, corner)

        exit_a = self.corner_exit_speed(year, gp, session, driver_a, lap_a, corner)
        exit_b = self.corner_exit_speed(year, gp, session, driver_b, lap_b, corner)

        return {
            "entry_delta": entry_a - entry_b,
            "apex_delta": apex_a - apex_b,
            "exit_delta": exit_a - exit_b
        }

    # 89
    def dirty_air_loss_estimation(self, year, gp, session, driver, lap):

        tel = self.get_telemetry(year, gp, session, driver, lap)

        throttle = tel["Throttle"]
        speed = tel["Speed"]

        efficiency = np.corrcoef(throttle, speed)[0][1]

        loss = 1 - efficiency

        return {
            "dirty_air_loss_index": float(loss)
        }

    # 90
    def downforce_estimation(self, year, gp, session, driver, lap):

        tel = self.get_telemetry(year, gp, session, driver, lap)

        speed = tel["Speed"]
        gear = tel["nGear"]

        stability = np.std(speed) / np.mean(gear)

        downforce_index = 1 / stability if stability != 0 else 0

        return {
            "downforce_index": float(downforce_index)
        }

    # 91
    def energy_deployment_pattern(self, year, gp, session, driver, lap):

        tel = self.get_telemetry(year, gp, session, driver, lap)

        speed = tel["Speed"]

        accel = np.gradient(speed)

        bursts = accel[accel > np.percentile(accel, 95)]

        return {
            "deployment_events": int(len(bursts)),
            "avg_acceleration": float(np.mean(accel))
        }
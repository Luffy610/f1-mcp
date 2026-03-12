"""E2E tests for telemetry tools (Tools 42-56)."""

import pytest
from services.telemetry_service import TelemetryService
from tests.conftest import assert_json_serializable

service = TelemetryService()


class TestTelemetryTools:

    def test_get_lap_telemetry(self, test_params):
        result = service.get_lap_telemetry(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_a"], test_params["lap_a"])
        assert_json_serializable(result, "get_lap_telemetry")
        assert result is not None
        assert "Speed" in result
        assert "Distance" in result

    def test_get_speed_trace(self, test_params):
        result = service.get_speed_trace(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_a"], test_params["lap_a"])
        assert_json_serializable(result, "get_speed_trace")
        assert isinstance(result, list)
        assert len(result) > 0

    def test_get_throttle_trace(self, test_params):
        result = service.get_throttle_trace(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_a"], test_params["lap_a"])
        assert_json_serializable(result, "get_throttle_trace")
        assert isinstance(result, list)

    def test_get_brake_trace(self, test_params):
        result = service.get_brake_trace(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_a"], test_params["lap_a"])
        assert_json_serializable(result, "get_brake_trace")
        assert isinstance(result, list)

    def test_get_gear_trace(self, test_params):
        result = service.get_gear_trace(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_a"], test_params["lap_a"])
        assert_json_serializable(result, "get_gear_trace")
        assert isinstance(result, list)

    def test_get_rpm_trace(self, test_params):
        result = service.get_rpm_trace(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_a"], test_params["lap_a"])
        assert_json_serializable(result, "get_rpm_trace")

    def test_get_drs_usage(self, test_params):
        result = service.get_drs_usage(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_a"], test_params["lap_a"])
        assert_json_serializable(result, "get_drs_usage")

    def test_get_distance_telemetry(self, test_params):
        result = service.get_distance_telemetry(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_a"], test_params["lap_a"])
        assert_json_serializable(result, "get_distance_telemetry")
        assert isinstance(result, list)

    def test_get_telemetry_segment(self, test_params):
        result = service.get_telemetry_segment(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_a"], test_params["lap_a"], 500, 1000)
        assert_json_serializable(result, "get_telemetry_segment")

    def test_get_corner_telemetry(self, test_params):
        result = service.get_corner_telemetry(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_a"], test_params["lap_a"], test_params["corner"])
        assert_json_serializable(result, "get_corner_telemetry")

    def test_compare_lap_telemetry(self, test_params):
        result = service.compare_lap_telemetry(
            test_params["year"], test_params["gp"], test_params["session"],
            test_params["driver_a"], test_params["lap_a"],
            test_params["driver_b"], test_params["lap_b"]
        )
        assert_json_serializable(result, "compare_lap_telemetry")
        assert "driver_a_speed" in result
        assert "driver_b_speed" in result

    def test_find_max_speed(self, test_params):
        result = service.find_max_speed(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_a"], test_params["lap_a"])
        assert_json_serializable(result, "find_max_speed")
        assert isinstance(result, float)

    def test_find_min_speed_corner(self, test_params):
        result = service.find_min_speed_corner(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_a"], test_params["lap_a"])
        assert_json_serializable(result, "find_min_speed_corner")
        assert "speed" in result
        assert "distance" in result

    def test_throttle_application_analysis(self, test_params):
        result = service.throttle_application_analysis(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_a"], test_params["lap_a"])
        assert_json_serializable(result, "throttle_application_analysis")

    def test_braking_point_analysis(self, test_params):
        result = service.braking_point_analysis(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_a"], test_params["lap_a"])
        assert_json_serializable(result, "braking_point_analysis")
        assert "brake_events" in result

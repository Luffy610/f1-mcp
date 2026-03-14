"""E2E tests for telemetry intelligence tools (Tools 85-91)."""

import pytest
from f1_mcp.services.telemetry_intelligence_service import TelemetryIntelligenceService
from tests.conftest import assert_json_serializable

service = TelemetryIntelligenceService()


class TestTelemetryIntelligenceTools:

    def test_corner_entry_speed(self, test_params):
        result = service.corner_entry_speed(
            test_params["year"], test_params["gp"], test_params["session"],
            test_params["driver_a"], test_params["lap_a"], test_params["corner"]
        )
        assert_json_serializable(result, "corner_entry_speed")
        assert isinstance(result, float)

    def test_corner_apex_speed(self, test_params):
        result = service.corner_apex_speed(
            test_params["year"], test_params["gp"], test_params["session"],
            test_params["driver_a"], test_params["lap_a"], test_params["corner"]
        )
        assert_json_serializable(result, "corner_apex_speed")
        assert isinstance(result, float)

    def test_corner_exit_speed(self, test_params):
        result = service.corner_exit_speed(
            test_params["year"], test_params["gp"], test_params["session"],
            test_params["driver_a"], test_params["lap_a"], test_params["corner"]
        )
        assert_json_serializable(result, "corner_exit_speed")
        assert isinstance(result, float)

    def test_corner_speed_comparison(self, test_params):
        result = service.corner_speed_comparison(
            test_params["year"], test_params["gp"], test_params["session"],
            test_params["driver_a"], test_params["lap_a"],
            test_params["driver_b"], test_params["lap_b"],
            test_params["corner"]
        )
        assert_json_serializable(result, "corner_speed_comparison")
        assert "entry_delta" in result

    def test_dirty_air_loss_estimation(self, test_params):
        result = service.dirty_air_loss_estimation(
            test_params["year"], test_params["gp"], test_params["session"],
            test_params["driver_a"], test_params["lap_a"]
        )
        assert_json_serializable(result, "dirty_air_loss_estimation")
        assert "dirty_air_loss_index" in result

    def test_downforce_estimation(self, test_params):
        result = service.downforce_estimation(
            test_params["year"], test_params["gp"], test_params["session"],
            test_params["driver_a"], test_params["lap_a"]
        )
        assert_json_serializable(result, "downforce_estimation")
        assert "downforce_index" in result

    def test_energy_deployment_pattern(self, test_params):
        result = service.energy_deployment_pattern(
            test_params["year"], test_params["gp"], test_params["session"],
            test_params["driver_a"], test_params["lap_a"]
        )
        assert_json_serializable(result, "energy_deployment_pattern")
        assert "deployment_events" in result

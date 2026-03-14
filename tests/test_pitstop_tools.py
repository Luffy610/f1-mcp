"""E2E tests for pit stop tools (Tools 65-71)."""

import pytest
from f1_mcp.services.pitstop_service import PitStopService
from tests.conftest import assert_json_serializable

service = PitStopService()


class TestPitStopTools:

    def test_get_pit_stops(self, test_params):
        result = service.get_pit_stops(test_params["year"], test_params["gp"], test_params["session"])
        assert_json_serializable(result, "get_pit_stops")
        assert isinstance(result, list)
        assert len(result) > 0
        assert isinstance(result[0]["lap"], int)

    def test_get_pit_stop_time(self, test_params):
        result = service.get_pit_stop_time(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_a"])
        assert_json_serializable(result, "get_pit_stop_time")
        assert isinstance(result, list)

    def test_get_pit_lane_loss(self, test_params):
        result = service.get_pit_lane_loss(test_params["year"], test_params["gp"], test_params["session"])
        assert_json_serializable(result, "get_pit_lane_loss")

    def test_undercut_effectiveness(self, test_params):
        result = service.undercut_effectiveness(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_a"])
        assert_json_serializable(result, "undercut_effectiveness")

    def test_overcut_effectiveness(self, test_params):
        result = service.overcut_effectiveness(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_a"])
        assert_json_serializable(result, "overcut_effectiveness")

    def test_optimal_pit_window(self, test_params):
        result = service.optimal_pit_window(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_a"])
        assert_json_serializable(result, "optimal_pit_window")

    def test_pit_stop_summary(self, test_params):
        result = service.pit_stop_summary(test_params["year"], test_params["gp"], test_params["session"])
        assert_json_serializable(result, "pit_stop_summary")
        assert isinstance(result, dict)
        # Verify lap numbers are ints, not floats
        for driver, data in result.items():
            for lap in data["laps"]:
                assert isinstance(lap, int), f"Lap number should be int, got {type(lap)}"

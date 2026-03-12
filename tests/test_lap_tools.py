"""E2E tests for lap tools (Tools 23-33)."""

import pytest
from services.lap_service import LapService
from tests.conftest import assert_json_serializable

service = LapService()


class TestLapTools:

    def test_get_all_laps(self, test_params):
        result = service.get_all_laps(test_params["year"], test_params["gp"], test_params["session"])
        assert_json_serializable(result, "get_all_laps")
        assert isinstance(result, list)
        assert len(result) > 0

    def test_get_driver_laps(self, test_params):
        """This was a known failing tool — TypeError: 'float' cannot be interpreted as integer."""
        result = service.get_driver_laps(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_a"])
        assert_json_serializable(result, "get_driver_laps")
        assert isinstance(result, list)
        assert len(result) > 0
        # Verify LapNumber is int, not float
        for lap in result:
            if lap.get("LapNumber") is not None:
                assert isinstance(lap["LapNumber"], int), f"LapNumber should be int, got {type(lap['LapNumber'])}"

    def test_get_lap_time(self, test_params):
        result = service.get_lap_time(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_a"], test_params["lap_a"])
        assert_json_serializable(result, "get_lap_time")
        assert result is not None
        assert isinstance(result, str)

    def test_get_fastest_lap(self, test_params):
        result = service.get_fastest_lap(test_params["year"], test_params["gp"], test_params["session"])
        assert_json_serializable(result, "get_fastest_lap")
        assert result is not None
        assert "driver" in result
        assert "lap_number" in result
        assert isinstance(result["lap_number"], int)

    def test_get_lap_delta(self, test_params):
        result = service.get_lap_delta(
            test_params["year"], test_params["gp"], test_params["session"],
            test_params["driver_a"], test_params["driver_b"], 10
        )
        assert_json_serializable(result, "get_lap_delta")

    def test_get_lap_times_series(self, test_params):
        result = service.get_lap_times_series(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_a"])
        assert_json_serializable(result, "get_lap_times_series")
        assert isinstance(result, list)
        assert len(result) > 0
        assert "lap" in result[0]
        assert isinstance(result[0]["lap"], int)

    def test_get_clean_laps(self, test_params):
        """This was a known failing tool — same serialization error as get_driver_laps."""
        result = service.get_clean_laps(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_a"])
        assert_json_serializable(result, "get_clean_laps")
        assert isinstance(result, list)

    def test_get_deleted_laps(self, test_params):
        result = service.get_deleted_laps(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_a"])
        assert_json_serializable(result, "get_deleted_laps")
        assert isinstance(result, list)

    def test_get_lap_position(self, test_params):
        result = service.get_lap_position(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_a"], 10)
        assert_json_serializable(result, "get_lap_position")
        assert result is None or isinstance(result, int)

    def test_get_lap_leader(self, test_params):
        result = service.get_lap_leader(test_params["year"], test_params["gp"], test_params["session"], 10)
        assert_json_serializable(result, "get_lap_leader")
        assert result is None or isinstance(result, str)

    def test_get_lap_time_distribution(self, test_params):
        result = service.get_lap_time_distribution(test_params["year"], test_params["gp"], test_params["session"])
        assert_json_serializable(result, "get_lap_time_distribution")
        assert "min" in result
        assert "max" in result
        assert isinstance(result["min"], float)

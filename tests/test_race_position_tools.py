"""E2E tests for race position tools (Tools 72-78)."""

import pytest
from services.race_position_service import RacePositionService
from tests.conftest import assert_json_serializable

service = RacePositionService()


class TestRacePositionTools:

    def test_get_position_changes(self, test_params):
        result = service.get_position_changes(test_params["year"], test_params["gp"], test_params["session"])
        assert_json_serializable(result, "get_position_changes")
        assert isinstance(result, list)

    def test_get_race_lead_changes(self, test_params):
        result = service.get_race_lead_changes(test_params["year"], test_params["gp"], test_params["session"])
        assert_json_serializable(result, "get_race_lead_changes")
        assert isinstance(result, list)

    def test_get_overtakes(self, test_params):
        result = service.get_overtakes(test_params["year"], test_params["gp"], test_params["session"])
        assert_json_serializable(result, "get_overtakes")
        assert isinstance(result, list)

    def test_get_driver_race_progression(self, test_params):
        result = service.get_driver_race_progression(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_a"])
        assert_json_serializable(result, "get_driver_race_progression")
        assert isinstance(result, list)
        assert len(result) > 0
        assert isinstance(result[0]["position"], int)

    def test_get_gap_to_leader(self, test_params):
        result = service.get_gap_to_leader(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_b"])
        assert_json_serializable(result, "get_gap_to_leader")
        assert isinstance(result, list)

    def test_get_gap_between_drivers(self, test_params):
        result = service.get_gap_between_drivers(
            test_params["year"], test_params["gp"], test_params["session"],
            test_params["driver_a"], test_params["driver_b"]
        )
        assert_json_serializable(result, "get_gap_between_drivers")
        assert isinstance(result, list)

    def test_get_battle_detection(self, test_params):
        result = service.get_battle_detection(test_params["year"], test_params["gp"], test_params["session"])
        assert_json_serializable(result, "get_battle_detection")
        assert isinstance(result, list)

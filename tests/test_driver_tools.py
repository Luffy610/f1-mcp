"""E2E tests for driver tools (Tools 13-22)."""

import pytest
from services.driver_service import DriverService
from tests.conftest import assert_json_serializable

service = DriverService()


class TestDriverTools:

    def test_list_drivers(self, test_params):
        result = service.list_drivers(test_params["year"], test_params["gp"], test_params["session"])
        assert_json_serializable(result, "list_drivers")
        assert isinstance(result, list)
        assert len(result) > 0
        # s.drivers returns driver numbers; names are in the dict
        names = " ".join(str(d) for d in result)
        assert "Verstappen" in names or any("VER" in str(d.get("code", "")) or "1" in str(d.get("code", "")) for d in result)

    def test_get_driver_info(self, test_params):
        result = service.get_driver_info(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_a"])
        assert_json_serializable(result, "get_driver_info")
        assert isinstance(result, dict)

    def test_get_driver_team(self, test_params):
        result = service.get_driver_team(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_a"])
        assert_json_serializable(result, "get_driver_team")
        assert result["driver"] == test_params["driver_a"]
        assert result["team"] is not None

    def test_get_driver_number(self, test_params):
        result = service.get_driver_number(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_a"])
        assert_json_serializable(result, "get_driver_number")
        assert result["driver"] == test_params["driver_a"]

    def test_get_teammate(self, test_params):
        result = service.get_teammate(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_a"])
        assert_json_serializable(result, "get_teammate")
        assert result is not None
        assert "teammate" in result

    def test_get_driver_grid_position(self, test_params):
        result = service.get_driver_grid_position(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_a"])
        assert_json_serializable(result, "get_driver_grid_position")
        assert result is None or isinstance(result, int)

    def test_get_driver_finish_position(self, test_params):
        result = service.get_driver_finish_position(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_a"])
        assert_json_serializable(result, "get_driver_finish_position")
        assert result is None or isinstance(result, int)

    def test_get_driver_points(self, test_params):
        result = service.get_driver_points(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_a"])
        assert_json_serializable(result, "get_driver_points")
        assert result is None or isinstance(result, float)

    def test_get_driver_standings(self, test_params):
        result = service.get_driver_standings(test_params["year"])
        assert_json_serializable(result, "get_driver_standings")
        assert isinstance(result, list)

    def test_get_constructor_standings(self, test_params):
        result = service.get_constructor_standings(test_params["year"])
        assert_json_serializable(result, "get_constructor_standings")
        assert isinstance(result, list)

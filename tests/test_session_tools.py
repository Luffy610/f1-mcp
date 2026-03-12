"""E2E tests for session tools (Tools 1-12)."""

import pytest
from services.session_service import SessionService
from tests.conftest import assert_json_serializable

service = SessionService()


class TestSessionTools:

    def test_list_seasons(self):
        result = service.list_seasons()
        assert_json_serializable(result, "list_seasons")
        assert isinstance(result, list)
        assert 2023 in result

    def test_list_grand_prix(self, test_params):
        result = service.list_grand_prix(test_params["year"])
        assert_json_serializable(result, "list_grand_prix")
        assert isinstance(result, list)
        assert any("Bahrain" in gp for gp in result)

    def test_list_sessions(self, test_params):
        result = service.list_sessions(test_params["year"], test_params["gp"])
        assert_json_serializable(result, "list_sessions")
        assert isinstance(result, list)
        assert len(result) > 0

    def test_get_session_info(self, test_params):
        result = service.get_session_info(test_params["year"], test_params["gp"], test_params["session"])
        assert_json_serializable(result, "get_session_info")
        assert "event_name" in result
        assert "Bahrain" in result["event_name"]

    def test_get_circuit_info(self, test_params):
        result = service.get_circuit_info(test_params["year"], test_params["gp"], test_params["session"])
        assert_json_serializable(result, "get_circuit_info")
        assert "corners" in result
        assert isinstance(result["corners"], list)
        assert len(result["corners"]) > 0
        # marshal_lights should be a list of dicts, not a raw DataFrame string
        if result.get("marshal_lights") is not None:
            assert isinstance(result["marshal_lights"], list)

    def test_get_track_length(self, test_params):
        result = service.get_track_length(test_params["year"], test_params["gp"], test_params["session"])
        assert_json_serializable(result, "get_track_length")

    def test_get_track_layout(self, test_params):
        result = service.get_track_layout(test_params["year"], test_params["gp"], test_params["session"])
        assert_json_serializable(result, "get_track_layout")
        assert isinstance(result, list)

    def test_get_session_weather(self, test_params):
        result = service.get_session_weather(test_params["year"], test_params["gp"], test_params["session"])
        assert_json_serializable(result, "get_session_weather")
        assert isinstance(result, list)

    def test_get_session_start_time(self, test_params):
        result = service.get_session_start_time(test_params["year"], test_params["gp"], test_params["session"])
        assert_json_serializable(result, "get_session_start_time")
        assert isinstance(result, str)

    def test_get_session_flag_events(self, test_params):
        result = service.get_session_flag_events(test_params["year"], test_params["gp"], test_params["session"])
        assert_json_serializable(result, "get_session_flag_events")
        assert isinstance(result, list)

    def test_get_track_status_changes(self, test_params):
        result = service.get_track_status_changes(test_params["year"], test_params["gp"], test_params["session"])
        assert_json_serializable(result, "get_track_status_changes")
        assert isinstance(result, list)

    def test_get_safety_car_periods(self, test_params):
        result = service.get_safety_car_periods(test_params["year"], test_params["gp"], test_params["session"])
        assert_json_serializable(result, "get_safety_car_periods")
        assert isinstance(result, list)

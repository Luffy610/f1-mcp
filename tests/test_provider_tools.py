"""E2E tests for provider tools (Tools 115-118)."""

import pytest
from f1_mcp.services.provider_service import ProviderService
from tests.conftest import assert_json_serializable

service = ProviderService()


class TestProviderTools:

    def test_merge_fastf1_and_ergast_results(self, test_params):
        result = service.merge_fastf1_and_ergast_results(test_params["year"], test_params["gp"], test_params["session"])
        assert_json_serializable(result, "merge_fastf1_and_ergast_results")
        assert isinstance(result, list)

    def test_validate_session_data(self, test_params):
        result = service.validate_session_data(test_params["year"], test_params["gp"], test_params["session"])
        assert_json_serializable(result, "validate_session_data")
        assert "laps_loaded" in result

    def test_fill_missing_telemetry(self, test_params):
        result = service.fill_missing_telemetry(
            test_params["year"], test_params["gp"], test_params["session"],
            test_params["driver_a"], test_params["lap_a"]
        )
        assert_json_serializable(result, "fill_missing_telemetry")

    def test_provider_health_check(self):
        result = service.provider_health_check()
        assert_json_serializable(result, "provider_health_check")
        assert "session_cache" in result

"""E2E tests for sector tools (Tools 34-41)."""

import pytest
from services.sector_service import SectorService
from tests.conftest import assert_json_serializable

service = SectorService()


class TestSectorTools:

    def test_get_sector_times(self, test_params):
        result = service.get_sector_times(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_a"], test_params["lap_a"])
        assert_json_serializable(result, "get_sector_times")
        assert result is not None

    def test_get_sector_delta(self, test_params):
        result = service.get_sector_delta(
            test_params["year"], test_params["gp"], test_params["session"],
            test_params["driver_a"], test_params["driver_b"], 10
        )
        assert_json_serializable(result, "get_sector_delta")

    def test_get_best_sector_times(self, test_params):
        result = service.get_best_sector_times(test_params["year"], test_params["gp"], test_params["session"])
        assert_json_serializable(result, "get_best_sector_times")
        assert isinstance(result, dict)

    def test_get_driver_best_sectors(self, test_params):
        result = service.get_driver_best_sectors(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_a"])
        assert_json_serializable(result, "get_driver_best_sectors")
        assert result is not None

    def test_sector_delta_vs_teammate(self, test_params):
        result = service.sector_delta_vs_teammate(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_a"])
        assert_json_serializable(result, "sector_delta_vs_teammate")

    def test_sector_performance_summary(self, test_params):
        result = service.sector_performance_summary(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_a"])
        assert_json_serializable(result, "sector_performance_summary")
        assert isinstance(result, dict)

    def test_sector_consistency(self, test_params):
        result = service.sector_consistency(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_a"])
        assert_json_serializable(result, "sector_consistency")
        assert isinstance(result, dict)

    def test_sector_improvement_over_time(self, test_params):
        result = service.sector_improvement_over_time(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_a"])
        assert_json_serializable(result, "sector_improvement_over_time")
        assert isinstance(result, dict)

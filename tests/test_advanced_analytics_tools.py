"""E2E tests for advanced analytics tools (Tools 92-98)."""

import pytest
from services.advanced_analytics_service import AdvancedAnalyticsService
from tests.conftest import assert_json_serializable

service = AdvancedAnalyticsService()


class TestAdvancedAnalyticsTools:

    def test_driver_consistency_score(self, test_params):
        result = service.driver_consistency_score(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_a"])
        assert_json_serializable(result, "driver_consistency_score")
        assert result is not None
        assert "consistency_score" in result

    def test_driver_aggression_index(self, test_params):
        result = service.driver_aggression_index(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_a"])
        assert_json_serializable(result, "driver_aggression_index")

    def test_driver_risk_index(self, test_params):
        result = service.driver_risk_index(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_a"])
        assert_json_serializable(result, "driver_risk_index")

    def test_qualifying_improvement_analysis(self, test_params):
        result = service.qualifying_improvement_analysis(test_params["year"], test_params["gp"], test_params["driver_a"])
        assert_json_serializable(result, "qualifying_improvement_analysis")

    def test_lap_time_variance(self, test_params):
        result = service.lap_time_variance(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_a"])
        assert_json_serializable(result, "lap_time_variance")
        assert result is not None
        assert "lap_time_variance" in result

    def test_performance_trend(self, test_params):
        result = service.performance_trend(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_a"])
        assert_json_serializable(result, "performance_trend")
        assert result is not None
        assert "trend" in result

    def test_driver_style_clustering(self, test_params):
        result = service.driver_style_clustering(test_params["year"], test_params["gp"], test_params["session"])
        assert_json_serializable(result, "driver_style_clustering")
        assert result is not None
        assert isinstance(result, list)

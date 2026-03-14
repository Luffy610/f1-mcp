"""E2E tests for strategy intelligence tools (Tools 79-84)."""

import pytest
from f1_mcp.services.strategy_intelligence_service import StrategyIntelligenceService
from tests.conftest import assert_json_serializable

service = StrategyIntelligenceService()


class TestStrategyIntelligenceTools:

    def test_predict_undercut_success(self, test_params):
        result = service.predict_undercut_success(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_a"])
        assert_json_serializable(result, "predict_undercut_success")

    def test_predict_overcut_success(self, test_params):
        result = service.predict_overcut_success(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_a"])
        assert_json_serializable(result, "predict_overcut_success")

    def test_race_strategy_simulation(self, test_params):
        result = service.race_strategy_simulation(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_a"])
        assert_json_serializable(result, "race_strategy_simulation")
        assert result["driver"] == test_params["driver_a"]

    def test_two_stop_vs_one_stop_simulation(self, test_params):
        result = service.two_stop_vs_one_stop_simulation(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_a"])
        assert_json_serializable(result, "two_stop_vs_one_stop_simulation")
        assert "recommended_strategy" in result

    def test_predict_optimal_strategy(self, test_params):
        result = service.predict_optimal_strategy(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_a"])
        assert_json_serializable(result, "predict_optimal_strategy")
        assert "recommended_strategy" in result

    def test_track_position_importance(self, test_params):
        result = service.track_position_importance(test_params["year"], test_params["gp"], test_params["session"])
        assert_json_serializable(result, "track_position_importance")
        assert "importance_level" in result

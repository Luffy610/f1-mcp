"""E2E tests for strategy tools (Tools 57-64)."""

import pytest
from services.strategy_service import StrategyService
from tests.conftest import assert_json_serializable

service = StrategyService()


class TestStrategyTools:

    def test_get_tyre_strategy(self, test_params):
        result = service.get_tyre_strategy(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_a"])
        assert_json_serializable(result, "get_tyre_strategy")
        assert isinstance(result, list)
        assert len(result) > 0
        assert "compound" in result[0]
        assert isinstance(result[0]["stint"], int)

    def test_get_stints(self, test_params):
        result = service.get_stints(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_a"])
        assert_json_serializable(result, "get_stints")
        assert isinstance(result, list)

    def test_get_tyre_compound_usage(self, test_params):
        result = service.get_tyre_compound_usage(test_params["year"], test_params["gp"], test_params["session"])
        assert_json_serializable(result, "get_tyre_compound_usage")
        assert isinstance(result, dict)

    def test_get_average_stint_length(self, test_params):
        result = service.get_average_stint_length(test_params["year"], test_params["gp"], test_params["session"])
        assert_json_serializable(result, "get_average_stint_length")
        assert isinstance(result, float)

    def test_get_tyre_degradation_rate(self, test_params):
        result = service.get_tyre_degradation_rate(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_a"])
        assert_json_serializable(result, "get_tyre_degradation_rate")
        assert isinstance(result, dict)

    def test_predict_tyre_cliff(self, test_params):
        result = service.predict_tyre_cliff(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_a"])
        assert_json_serializable(result, "predict_tyre_cliff")
        assert isinstance(result, dict)

    def test_compare_tyre_performance(self, test_params):
        result = service.compare_tyre_performance(test_params["year"], test_params["gp"], test_params["session"])
        assert_json_serializable(result, "compare_tyre_performance")
        assert isinstance(result, dict)

    def test_tyre_strategy_comparison(self, test_params):
        result = service.tyre_strategy_comparison(
            test_params["year"], test_params["gp"], test_params["session"],
            test_params["driver_a"], test_params["driver_b"]
        )
        assert_json_serializable(result, "tyre_strategy_comparison")
        assert result["driver_a"] == test_params["driver_a"]

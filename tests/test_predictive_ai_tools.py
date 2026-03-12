"""E2E tests for predictive AI tools (Tools 99-108)."""

import pytest
from services.predictive_ai_service import PredictiveAIService
from tests.conftest import assert_json_serializable

service = PredictiveAIService()


class TestPredictiveAITools:

    def test_predict_overtake_probability(self, test_params):
        result = service.predict_overtake_probability(
            test_params["year"], test_params["gp"], test_params["session"],
            test_params["driver_a"], test_params["driver_b"]
        )
        assert_json_serializable(result, "predict_overtake_probability")
        assert result is not None
        assert "overtake_probability" in result

    def test_predict_safety_car_probability(self, test_params):
        result = service.predict_safety_car_probability(test_params["year"], test_params["gp"], test_params["session"])
        assert_json_serializable(result, "predict_safety_car_probability")
        assert "safety_car_probability" in result

    def test_predict_virtual_safety_car_probability(self, test_params):
        result = service.predict_virtual_safety_car_probability(test_params["year"], test_params["gp"], test_params["session"])
        assert_json_serializable(result, "predict_virtual_safety_car_probability")

    def test_predict_race_winner(self, test_params):
        result = service.predict_race_winner(test_params["year"], test_params["gp"], test_params["session"])
        assert_json_serializable(result, "predict_race_winner")
        assert "predicted_winner" in result

    def test_predict_next_pit_stop(self, test_params):
        result = service.predict_next_pit_stop(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_a"])
        assert_json_serializable(result, "predict_next_pit_stop")

    def test_predict_battle_outcome(self, test_params):
        result = service.predict_battle_outcome(
            test_params["year"], test_params["gp"], test_params["session"],
            test_params["driver_a"], test_params["driver_b"]
        )
        assert_json_serializable(result, "predict_battle_outcome")
        assert "predicted_battle_winner" in result

    def test_predict_tyre_strategy(self, test_params):
        result = service.predict_tyre_strategy(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_a"])
        assert_json_serializable(result, "predict_tyre_strategy")
        assert "predicted_strategy" in result

    def test_predict_lap_time(self, test_params):
        result = service.predict_lap_time(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_a"])
        assert_json_serializable(result, "predict_lap_time")
        assert result is not None
        assert "predicted_lap_time_seconds" in result

    def test_predict_race_podium(self, test_params):
        result = service.predict_race_podium(test_params["year"], test_params["gp"], test_params["session"])
        assert_json_serializable(result, "predict_race_podium")
        assert "predicted_podium" in result
        assert len(result["predicted_podium"]) == 3

    def test_predict_driver_position_end_of_race(self, test_params):
        result = service.predict_driver_position_end_of_race(test_params["year"], test_params["gp"], test_params["session"], test_params["driver_a"])
        assert_json_serializable(result, "predict_driver_position_end_of_race")

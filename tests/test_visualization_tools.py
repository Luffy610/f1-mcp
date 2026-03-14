"""E2E tests for visualization tools (Tools 109-114)."""

import os
import pytest
from f1_mcp.services.visualization_service import VisualizationService
from tests.conftest import assert_json_serializable

service = VisualizationService()


class TestVisualizationTools:

    def test_generate_speed_map(self, test_params):
        result = service.generate_speed_map(
            test_params["year"], test_params["gp"], test_params["session"],
            test_params["driver_a"], test_params["lap_a"]
        )
        assert_json_serializable(result, "generate_speed_map")
        assert "plot_path" in result
        assert os.path.exists(result["plot_path"])

    def test_generate_track_dominance_map(self, test_params):
        result = service.generate_track_dominance_map(
            test_params["year"], test_params["gp"], test_params["session"],
            test_params["driver_a"], test_params["lap_a"],
            test_params["driver_b"], test_params["lap_b"]
        )
        assert_json_serializable(result, "generate_track_dominance_map")
        assert "plot_path" in result

    def test_generate_lap_delta_plot(self, test_params):
        """This was a known failing tool — dimension mismatch between telemetry arrays."""
        result = service.generate_lap_delta_plot(
            test_params["year"], test_params["gp"], test_params["session"],
            test_params["driver_a"], test_params["lap_a"],
            test_params["driver_b"], test_params["lap_b"]
        )
        assert_json_serializable(result, "generate_lap_delta_plot")
        assert "plot_path" in result
        assert os.path.exists(result["plot_path"])

    def test_generate_tyre_degradation_plot(self, test_params):
        result = service.generate_tyre_degradation_plot(
            test_params["year"], test_params["gp"], test_params["session"],
            test_params["driver_a"]
        )
        assert_json_serializable(result, "generate_tyre_degradation_plot")
        assert "plot_path" in result

    def test_generate_sector_performance_chart(self, test_params):
        result = service.generate_sector_performance_chart(
            test_params["year"], test_params["gp"], test_params["session"],
            test_params["driver_a"]
        )
        assert_json_serializable(result, "generate_sector_performance_chart")
        assert "plot_path" in result

    def test_generate_race_progression_chart(self, test_params):
        result = service.generate_race_progression_chart(
            test_params["year"], test_params["gp"], test_params["session"],
            test_params["driver_a"]
        )
        assert_json_serializable(result, "generate_race_progression_chart")
        assert "plot_path" in result

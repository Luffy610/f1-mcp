"""
Shared fixtures for E2E tests.

Uses 2023 Bahrain GP Race as the canonical test session — it's a well-known
dataset that exercises all tools (pit stops, overtakes, safety cars, etc.).
"""

import sys
import os
import json
import pytest

# Ensure project root is on path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from config import initialize_cache

initialize_cache()


# Canonical test parameters
TEST_YEAR = 2023
TEST_GP = "Bahrain"
TEST_SESSION = "R"
TEST_DRIVER_A = "VER"  # Verstappen
TEST_DRIVER_B = "PER"  # Perez
TEST_LAP_A = 44         # VER's fastest lap
TEST_LAP_B = 37         # PER's fastest lap
TEST_CORNER = 1


@pytest.fixture(scope="session")
def test_params():
    return {
        "year": TEST_YEAR,
        "gp": TEST_GP,
        "session": TEST_SESSION,
        "driver_a": TEST_DRIVER_A,
        "driver_b": TEST_DRIVER_B,
        "lap_a": TEST_LAP_A,
        "lap_b": TEST_LAP_B,
        "corner": TEST_CORNER,
    }


def assert_json_serializable(result, tool_name="unknown"):
    """Assert that a result can be serialized to JSON without errors."""
    try:
        json.dumps(result)
    except (TypeError, ValueError, OverflowError) as e:
        pytest.fail(f"Tool '{tool_name}' returned non-JSON-serializable result: {e}\nResult type: {type(result)}")

"""
Shared utilities for sanitizing FastF1 DataFrames before JSON serialization.

FastF1 DataFrames contain types that are not JSON-serializable:
- Timedelta columns (LapTime, Sector*Time, PitInTime, PitOutTime, Time)
- Float columns that should be ints (LapNumber, Position, Stint)
- NaT/NaN values that need to become None
"""

import pandas as pd
import numpy as np


# Columns that FastF1 stores as float but are logically integers
INT_COLUMNS = {"LapNumber", "Position", "Stint", "GridPosition", "DriverNumber",
               "Number", "ClassifiedPosition", "RoundNumber", "TyreLife"}

# Columns that are Timedelta and need string conversion
# Note: SpeedI1, SpeedI2, SpeedFL, SpeedST are float speed values, NOT timedeltas
TIMEDELTA_COLUMNS = {"LapTime", "Sector1Time", "Sector2Time", "Sector3Time",
                     "Sector1SessionTime", "Sector2SessionTime", "Sector3SessionTime",
                     "PitInTime", "PitOutTime", "Time", "Delta"}


def sanitize_value(val):
    """Convert a single value to a JSON-safe type."""
    if val is None:
        return None
    if isinstance(val, pd.Timedelta):
        return str(val)
    if isinstance(val, pd.Timestamp):
        return str(val)
    # Handle NaT (Not a Time) — check via pd.isna since NaT has no stable type
    try:
        if pd.isna(val):
            return None
    except (ValueError, TypeError):
        pass
    if isinstance(val, (np.integer,)):
        return int(val)
    if isinstance(val, (np.floating,)):
        if np.isnan(val):
            return None
        return float(val)
    if isinstance(val, (np.bool_,)):
        return bool(val)
    if isinstance(val, np.ndarray):
        return val.tolist()
    if isinstance(val, float) and np.isnan(val):
        return None
    return val


def sanitize_df(df):
    """
    Convert a FastF1 DataFrame to a list of JSON-safe dicts.

    Handles Timedelta→str, float→int for known columns, NaN→None.
    """
    if df is None or (hasattr(df, 'empty') and df.empty):
        return []

    result = df.copy()

    # Convert int-like float columns to nullable Int64
    for col in INT_COLUMNS:
        if col in result.columns:
            result[col] = pd.to_numeric(result[col], errors="coerce").astype("Int64")

    # Convert Timedelta columns to strings
    for col in result.columns:
        if col in TIMEDELTA_COLUMNS or pd.api.types.is_timedelta64_dtype(result[col]):
            result[col] = result[col].apply(lambda x: str(x) if pd.notna(x) else None)

    # Convert Timestamp columns
    for col in result.columns:
        if pd.api.types.is_datetime64_any_dtype(result[col]):
            result[col] = result[col].apply(lambda x: str(x) if pd.notna(x) else None)

    # Convert remaining float columns: NaN → None, numpy float → Python float
    for col in result.columns:
        if pd.api.types.is_float_dtype(result[col]):
            result[col] = result[col].apply(
                lambda x: None if pd.isna(x) else float(x)
            )

    records = result.to_dict(orient="records")

    # Final pass: sanitize any remaining non-JSON types
    sanitized = []
    for record in records:
        clean = {}
        for k, v in record.items():
            clean[k] = sanitize_value(v)
        sanitized.append(clean)

    return sanitized

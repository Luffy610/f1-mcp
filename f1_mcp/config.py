import os
import fastf1
from pathlib import Path

CACHE_DIR = Path(os.environ.get("F1_CACHE_DIR", os.path.join(os.path.expanduser("~"), ".f1-mcp", "cache")))

def initialize_cache():
    """Create the cache directory and enable FastF1 disk caching."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    fastf1.Cache.enable_cache(str(CACHE_DIR))
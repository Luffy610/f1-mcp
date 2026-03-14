"""Backwards-compatible entry point. Prefer: pip install -e . && f1-mcp"""
from f1_mcp.server import mcp

if __name__ == "__main__":
    mcp.run(transport="sse", host="0.0.0.0", port=8000)

FROM python:3.13-slim

WORKDIR /app

# Copy package files and install
COPY pyproject.toml README.md ./
COPY f1_mcp/ f1_mcp/
RUN pip install --no-cache-dir .

# Create directories for cache and plots
RUN mkdir -p cache plots

EXPOSE 8000

CMD ["python", "-c", "from f1_mcp.server import mcp; mcp.run(transport='sse', host='0.0.0.0', port=8000)"]

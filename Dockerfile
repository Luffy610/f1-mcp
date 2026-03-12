FROM python:3.13-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY config.py server.py ./
COPY connectors/ connectors/
COPY core/ core/
COPY models/ models/
COPY services/ services/
COPY tools/ tools/

# Create directories for cache and plots
RUN mkdir -p cache plots

EXPOSE 8000

CMD ["python", "server.py"]

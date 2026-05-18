FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir flask flask-cors

# Copy backend code (API needs it)
COPY backend ./backend

# Copy API code
COPY api ./api

# Set Python path
ENV PYTHONPATH=/app

WORKDIR /app

# Expose port
EXPOSE 5000

# Run API
CMD ["python", "-u", "api/app.py"]

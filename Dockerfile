FROM python:3.10-slim

WORKDIR /app

# Install only essential dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --compile -r requirements.txt

# Create db_files directory with proper permissions
RUN mkdir -p /app/db_files && chmod -R 777 /app/db_files

# Copy application code
COPY . .

# Set timezone as root
ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Create a non-root user and group
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Set permissions for /app and ensure db_files is writable
RUN chown -R appuser:appgroup /app && \
    chmod -R 755 /app && \
    chmod -R 777 /app/db_files

# Switch to non-root user
USER appuser

# Environment variables for performance optimization
ENV PYTHONUNBUFFERED=1 \
    NICEGUI_HOST=0.0.0.0 \
    NICEGUI_PORT=8080 \
    PYTHONMALLOC=malloc \
    PYTHONHASHSEED=random

EXPOSE 8080

# Clean up caches before running to reduce memory footprint
RUN find /app -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true \
    && find /app -name "*.pyc" -delete

CMD ["python", "app.py"]

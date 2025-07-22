FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create db_files directory with proper permissions
RUN mkdir -p /app/db_files && chmod 777 /app/db_files

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

ENV PYTHONUNBUFFERED=1 \
    NICEGUI_HOST=0.0.0.0 \
    NICEGUI_PORT=8080

EXPOSE 8080

CMD ["python", "app.py"]

FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set timezone as root
ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Create a non-root user and group
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Set permissions for /app
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

ENV PYTHONUNBUFFERED=1 \
    NICEGUI_HOST=0.0.0.0 \
    NICEGUI_PORT=8080

EXPOSE 8080

CMD ["uvicorn", "index:app", "--host", "0.0.0.0", "--port", "8080"]

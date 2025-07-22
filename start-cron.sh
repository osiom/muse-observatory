#!/bin/sh
# Activate venv
. /venv/bin/activate

# Setup cron job
mkdir -p /etc/crontabs
echo "1 0 * * * /venv/bin/python /app/generate_fact.py && docker restart muse-observatory-app" > /etc/crontabs/root

# Show crontab for debug
cat /etc/crontabs/root

# Run cron in foreground with verbose logs
crond -f -l 8

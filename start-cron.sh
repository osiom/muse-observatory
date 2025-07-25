#!/bin/sh
# Just run cron in foreground — crontab is already set
crond -f -l 8

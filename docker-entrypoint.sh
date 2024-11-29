#!/bin/bash
set -e

# Wait for Redis to be ready
until python -c "import redis; redis.Redis(host='redis', port=6379).ping()" 2>/dev/null; do
  echo "Waiting for Redis to be ready..."
  sleep 1
done

# Initialize the database
python -c "from app.core.database import init_db; init_db()"

# Execute the command (either celery worker or beat)
exec "$@"
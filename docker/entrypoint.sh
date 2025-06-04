#!/bin/bash
# Entrypoint script for Jobs Watcher application
# Runs database migrations before starting the application

set -e  # Exit on any error

echo "=== Jobs Watcher Container Starting ==="

# Wait for database to be ready (optional but recommended)
echo "Waiting for database to be ready..."
until nc -z ${POSTGRES_HOST:-postgres} ${POSTGRES_PORT:-5432}; do
    echo "Database not ready, waiting..."
    sleep 2
done
echo "Database is ready!"

# Run database migrations
echo "=== Running database migrations ==="

# Run migrations with proper error handling
if uv run flask db upgrade; then
    echo "Database migrations completed successfully"
else
    echo "Database migrations failed, but continuing..."
    echo "Note: This might be expected on first run if migrations haven't been initialized"
fi

# Start the main application
echo "=== Starting Jobs Watcher Application ==="
exec uv run ./src/app.py

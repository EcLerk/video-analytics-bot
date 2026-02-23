#!/bin/bash

set -e

# Apply migrations
alembic upgrade head

# Start CMD
exec "$@"
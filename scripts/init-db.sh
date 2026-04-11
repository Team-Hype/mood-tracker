#!/bin/bash
# This script runs on the database container startup

set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    -- Custom SQL here
EOSQL

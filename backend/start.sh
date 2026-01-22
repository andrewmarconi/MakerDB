#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.." || exit 1

.venv/bin/python \
    -m uvicorn makerdb.asgi:application \
    --app-dir backend

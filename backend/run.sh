#!/usr/bin/env bash
DB_DRIVER=sqlite uvicorn app:app --reload --host 0.0.0.0 --port 8000
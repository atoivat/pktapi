#!/bin/bash
python -m core.migrations
python populate.py
uvicorn app.main:app --host 0.0.0.0 --port 80
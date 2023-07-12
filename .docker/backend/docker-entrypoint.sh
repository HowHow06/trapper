#!/bin/bash
poetry run alembic upgrade head
exec poetry run gunicorn -w 2 -k uvicorn.workers.UvicornWorker app.main:app -b 0.0.0.0:8000
# poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000

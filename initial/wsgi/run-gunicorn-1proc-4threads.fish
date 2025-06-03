#!/usr/bin/env fish

gunicorn --bind 127.0.0.1:5010 \
    # num procesess:
    --workers 1 \
    # num threads (per process);
    --threads 4 \
    app:app

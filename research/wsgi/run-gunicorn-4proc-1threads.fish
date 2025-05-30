#!/usr/bin/env fish

gunicorn --bind 127.0.0.1:5010 \
    # num procesess:
    --workers 4 \
    # num threads (per process);
    --threads 1 \
    app:app

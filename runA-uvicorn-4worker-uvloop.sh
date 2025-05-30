#!/usr/bin/env bash

uvicorn \
    --workers 4 \
    --loop uvloop \
    --no-access-log \
    --port 9010 \
    main:app

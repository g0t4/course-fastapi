#!/usr/bin/env bash

uvicorn \
    --workers 2 \
    --loop uvloop \
    --no-access-log \
    --port 9010 \
    main:app

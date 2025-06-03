#!/usr/bin/env bash

# defaults:
#   --workers 1
#   --loop uvloop

uvicorn \
    --workers 1 \
    --loop uvloop \
    --no-access-log \
    --port 9010 \
    main:app

#!/usr/bin/env fish

# usage:
#  watch --color UVICORN_PORT=8000 ./example-curl-timing.fish

curl -fsSL -w @curl_timing_yaml "http://127.0.0.1:$UVICORN_PORT" \
    | yq --colors

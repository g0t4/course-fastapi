#!/usr/bin/env fish

curl -fsSL -w @curl_all_json "http://127.0.0.1:$UVICORN_PORT" | jq --color-output

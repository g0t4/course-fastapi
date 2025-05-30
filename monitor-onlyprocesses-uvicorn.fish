#!/usr/bin/env fish

# drop -M, so had to set format with -o to get columns I wanted back (including CPU usage)

watch --color --no-wrap --no-title \
    "fish -c 'grc --colour=on ps -o pid,tty,%cpu,command -p (echo (pgrep -if \".venv/bin/uvicorn\") (pgrep -P (pgrep -if \".venv/bin/uvicorn\") ) )'"

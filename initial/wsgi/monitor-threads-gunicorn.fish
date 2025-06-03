#!/usr/bin/env fish

# run fish -c to re-execute entire command each time, to get new PIDs each time
watch --color --no-wrap --no-title \
    "fish -c 'grc --colour=on ps -M -p (pgrep -if \".venv/bin/gunicorn\")'"

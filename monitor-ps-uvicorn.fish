#!/usr/bin/env fish

watch --color --no-wrap --no-title \
    "fish -c 'grc --colour=on ps -M -p (echo (pgrep -if \".venv/bin/uvicorn\") (pgrep -P (pgrep -if \".venv/bin/uvicorn\") ) )'"

# only need second `pgrep -P (...)` when using workers > 1
#   b/c it switches to multiprocessing.spawn for workers 
#   and pgrep .venv/bin/uvicorn doesn't match those processes

# BTW procs command is an alternative to get same info, however it had a bug when I was preparing course materials.

## FastAPI - Async vs Sync

| Workers |  Async        |   Sync        | Ratio (Async/Sync) |
|---------|---------------|---------------|--------------------|
|    1    |  25,750       |  12,374       | 2.08               |
|    2    |  47,911 (93%) |  22,455 (91%) | 2.13               |
|    4    |  90,966 (88%) |  34,680 (70%) | 2.62               |

## gunicorn + Flask (WSGI)

| workers | threads |  RPS  |
|---------|---------|-------|
|    1    |    1    | 2,392 |
|    4    |    1    | 6,290 |
|    1    |    4    | 2,185 |



## psql

```sh

source ./pgcli-psql-env-vars.sh

\l # list database
\d # list tables
\c postgres # connect to a database

```


## using the postgres container

```sh
docker-compose up -d

# cleanup, including named data volumes
docker compose down --remove-orphans --volumes
```

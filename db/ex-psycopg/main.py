from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from psycopg2.pool import ThreadedConnectionPool
import uuid

DATABASE_URL = "postgresql://postgres:postgres@localhost/postgres"

def recreate_table(pool: ThreadedConnectionPool):
    with pool.getconn() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                DROP TABLE IF EXISTS messages; 
                CREATE TABLE messages (id UUID PRIMARY KEY, content TEXT, sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
            """)

@asynccontextmanager
async def app_lifespan(app_: FastAPI):
    # https://www.starlette.io/lifespan/
    print("lifespan STARTUP")
    pool = ThreadedConnectionPool(minconn=5, maxconn=20, dsn=DATABASE_URL)
    recreate_table(pool)

    yield {"pool": pool}

    print("lifespan SHUTDOWN")
    pool.closeall()

app = FastAPI(lifespan=app_lifespan)

@app.get("/")
def default():
    return "psycopg2 example - use /message to test performance"

# GET here to contrast with POST later on
# curl -i localhost:8000/message?content=foothebar
@app.get("/message")
async def message(content: str, request: Request):
    id = uuid.uuid4()

    # example of not using context manager for connection, this is why CM is useful
    pool: ThreadedConnectionPool = request.state.pool
    connection = None
    try:
        connection = pool.getconn()
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO messages (id, content) VALUES (%s, %s) ", (str(id), content))

        connection.commit()
    finally:
        if connection:
            pool.putconn(connection)

    return {
        "id": id,
        "message": content,
    }

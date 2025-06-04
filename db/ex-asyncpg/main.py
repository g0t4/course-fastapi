from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
import asyncpg
import uuid

DATABASE_URL = "postgresql://postgres:postgres@localhost/postgres"

async def recreate_table(pool: asyncpg.Pool):
    async with pool.acquire() as connection:
        await connection.execute("""
            DROP TABLE IF EXISTS messages;
            CREATE TABLE messages (id UUID PRIMARY KEY, content TEXT, sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
        """)

@asynccontextmanager
async def app_lifespan(app_: FastAPI):
    print("lifespan STARTUP")
    async with asyncpg.create_pool(DATABASE_URL, min_size=5, max_size=20) as pool:
        await recreate_table(pool)

        yield {"pool": pool}

    print("lifespan SHUTDOWN")

app = FastAPI(lifespan=app_lifespan)

@app.get("/")
def default():
    return "asyncpg example - use /message to test performance"

# curl -i localhost:8000/message?content=foothebar
@app.get("/message")
async def message(content: str, request: Request):
    id = uuid.uuid4()

    pool: asyncpg.Pool = request.state.pool
    async with pool.acquire() as connection:
        await connection.execute(
            "INSERT INTO messages (id, content) VALUES ($1, $2) ",
            id,
            content,
        )

    return {
        "id": id,
        "message": content,
    }

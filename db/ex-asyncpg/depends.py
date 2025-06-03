from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import Body, Depends, FastAPI, Request
from pydantic import BaseModel, Field
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
    return "asyncpg depends example - use /message to test performance"

async def get_connection(request: Request):
    # FYI careful w/ print when measuing performance
    # I added it here to observe order of operations
    print(f"start get_connection")
    pool: asyncpg.Pool = request.state.pool
    async with pool.acquire() as connection:
        async with connection.transaction():
            yield connection
    print(f"finish get_connection")

class MessageModel(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    content: str

# submit content in body of request:
# http localhost:8000/message content=foothebar
# http -v localhost:8000/message content=foothebar
#    add -v to see the body the http(ie) command sends
@app.post("/message")
async def message(
    # content: Annotated[str, Body], # alternative
    message: MessageModel,
    connection: Annotated[asyncpg.Connection, Depends(get_connection)],
):
    # print(f"app state: {vars(request.state)}")

    print(f"before insert")
    await connection.execute(
        "INSERT INTO messages (id, content) VALUES ($1, $2) ",
        message.id,
        message.content,
    )
    print("after insert")

    return message

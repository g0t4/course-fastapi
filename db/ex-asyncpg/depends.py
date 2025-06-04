from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import Depends, FastAPI, Request
from pydantic import BaseModel, Field
import asyncpg
import uuid

DATABASE_URL = "postgresql://postgres:postgres@localhost/postgres"

async def recreate_table(pool: asyncpg.Pool) -> None:
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
async def default():
    return "asyncpg depends example - use /message to test performance"





async def get_pool(request: Request) -> asyncpg.Pool:
    return request.state.pool



# make annotated types (dependencies) reusable
Pool = Annotated[asyncpg.Pool, Depends(get_pool)]

async def with_connection(pool: Pool):
    # FYI careful w/ print when measuing performance
    # I added it here to observe order of operations
    print(f"start with_connection")
    async with pool.acquire() as connection:
        async with connection.transaction():
            yield connection
    print(f"finish with_connection")




class MessageModel(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    content: str




# submit content in body of request:
# http -v localhost:8000/message content=foothebar
@app.post("/message")
async def message(
    message: MessageModel,
    connection: Annotated[asyncpg.Connection, Depends(with_connection)],
):

    print(f"before insert")
    await connection.execute(
        "INSERT INTO messages (id, content) VALUES ($1, $2) ",
        message.id,
        message.content,
    )
    print("after insert")

    return message

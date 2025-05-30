from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello There Two"}


# async vs sync

@app.get("/fastapi")
async def hello_async():
    return "Hello FastAPI ASYNC"

@app.get("/fastapi_sync")
def hello_sync():
    return "Hello FastAPI SYNC"

from typing import Awaitable, Callable
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import FileResponse, HTMLResponse

app = FastAPI()

@app.middleware("http")
async def logger(request: Request, next: Callable[[Request], Awaitable[Response]]):
    print(f"logger start {request.url}")
    response: Response = await next(request)
    print("logger end")
    response.headers["FOO"] = "BAR"
    return response










prefix = "/usr/share/dict"
files = {
    "web2a": f"{prefix}/web2a",
    "web2": f"{prefix}/web2",
    "words": f"{prefix}/words",
    "propernames": f"{prefix}/propernames",
    "README": f"{prefix}/README",
    "connectives": f"{prefix}/connectives",
}

@app.get("/")
async def root():
    print("root start")
    html = "<html><body><h1>Welcome to the File Server!</h1>"
    for key in files.keys():
        html += f"<br><a href='/files/{key}'>{key}</a>"
    html += "</body></html>"
    print("root end")
    return HTMLResponse(content=html)

@app.get("/files/{name}")
async def get_file(name: str):
    file = files.get(name)
    if file is None:
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file)

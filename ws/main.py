from fastapi import FastAPI, WebSocket, WebSocketDisconnect, WebSocketException

app = FastAPI()


@app.websocket("/")
async def ws1(ws: WebSocket):
    await ws.accept()
    await ws.send_text("welcome")

    async for msg in ws.iter_text():
        await ws.send_text(f"echo: {msg}")
        if msg == ":quit":
            break

    await ws.close()
    print("done")






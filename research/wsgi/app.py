from flask import Flask

app = Flask(__name__)

@app.get("/hello_flask")
def hello():
    return "Hello flask"

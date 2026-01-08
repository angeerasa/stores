from fastapi import FastAPI
from routes import api

app = FastAPI()

app.include_router(api.api_router, prefix="/api")

@app.get("/")
def home():
    return "hello world"
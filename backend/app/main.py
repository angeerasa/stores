from fastapi import FastAPI
from app.routes import api
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # 👈 allow all domains
    allow_credentials=True,
    allow_methods=["*"],      # 👈 allow all HTTP methods
    allow_headers=["*"],      # 👈 allow all headers
)

app.include_router(api.api_router, prefix="/api")

@app.get("/")
def home():
    return "hello world"
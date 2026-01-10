from fastapi import Depends, FastAPI, HTTPException, Request, status
from app.routes import api
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from app.utils.Constants import BASE_URL, PUBLIC_ROUTES
from app.utils.pyjwt import verify_access_token

app = FastAPI()


app.include_router(api.api_router, prefix="/api")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

@app.middleware("http")
async def verify_auth_token(request: Request, call_next):
    #exceptions to middleware auth
    if(request.url.path in PUBLIC_ROUTES):
        res = await call_next(request);
        return res

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header"
        )

    token = auth_header.split(" ")[1]
    user = verify_access_token(token)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    res = await call_next(request);
    return res

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # 👈 allow all domains
    allow_credentials=True,
    allow_methods=["*"],      # 👈 allow all HTTP methods
    allow_headers=["*"],      # 👈 allow all headers
)


@app.get("/")
def home():
    return "hello world"

@app.get("/auth")
async def readToken(token:str = Depends(oauth2_scheme)):
    return {"token":token}
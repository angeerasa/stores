from typing import Dict
from datetime import datetime, timedelta
import jwt
from dotenv import load_dotenv
import os
from jwt import PyJWTError

load_dotenv()

JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
JWT_ALGORITHM = os.environ["JWT_ALGORITHM"]
JWT_EXPIRE_TIMEDELTA_MINUTES = os.environ["JWT_EXPIRE_TIMEDELTA_MINUTES"]

def create_access_token(data: dict):
    to_encode = data.copy()
    expire_time = datetime.now() + timedelta(minutes=int(JWT_EXPIRE_TIMEDELTA_MINUTES))
    to_encode.update({"exp": expire_time.timestamp()})
    access_token = jwt.encode(to_encode, JWT_SECRET_KEY, JWT_ALGORITHM)
    print(access_token)
    return {
        "access_token": access_token
    }

def verify_access_token(token: str):
    try:
        user = jwt.decode(token, JWT_SECRET_KEY, [JWT_ALGORITHM])
        return user
    except PyJWTError as jwtError:
        return None
    except Exception as error:
        return None
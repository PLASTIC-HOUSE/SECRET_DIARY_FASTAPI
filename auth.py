import os
from datetime import datetime, timedelta

from fastapi import HTTPException
from jwt import encode, decode, DecodeError

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = 'HS256'


def create_token(user_id: int):
    exp = datetime.utcnow() + timedelta(minutes=60)
    encoded_jwt = encode({"exp": exp, "sub": user_id}, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_id(token: str):
    try:
        return decode(token, SECRET_KEY, algorithms=[ALGORITHM])['sub']
    except DecodeError:
        raise HTTPException(status_code=401, detail="Invalid Token")

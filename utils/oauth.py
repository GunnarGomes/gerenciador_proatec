import requests
from fastapi import HTTPException
from jose import jwt
import os

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

def verify_google_token(token: str):
    """Verifica token JWT do Google"""
    url = f"https://oauth2.googleapis.com/tokeninfo?id_token={token}"
    resp = requests.get(url)
    if resp.status_code != 200:
        raise HTTPException(status_code=400, detail="Token inválido")
    data = resp.json()
    if data.get("aud") != GOOGLE_CLIENT_ID:
        raise HTTPException(status_code=400, detail="Token não pertence a este app")
    return data

def create_jwt_token(payload: dict):
    """Cria token JWT local"""
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

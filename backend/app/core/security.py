from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "fallback-inseguro-troque-no-env")
ALGORITHM  = "HS256"
EXPIRACAO_HORAS = 8

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_senha(senha: str) -> str:
    """Gera o hash bcrypt de uma senha."""
    return pwd_context.hash(senha)


def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    """Compara a senha digitada com o hash armazenado no banco."""
    return pwd_context.verify(senha_plana, senha_hash)


def criar_token(dados: dict) -> str:
    """Gera um JWT com os dados do usuário e validade de 8h."""
    payload = dados.copy()
    payload["exp"] = datetime.utcnow() + timedelta(hours=EXPIRACAO_HORAS)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decodificar_token(token: str) -> Optional[dict]:
    """Decodifica e valida um JWT. Retorna None se inválido."""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
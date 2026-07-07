from datetime import datetime, timedelta
from jose import jwt
import bcrypt
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "fallback-inseguro-troque-no-env")
ALGORITHM  = "HS256"
EXPIRACAO_HORAS = 8


def hash_senha(senha: str) -> str:
    """Gera o hash bcrypt de uma senha."""
    senha_bytes = senha.encode("utf-8")[:72]
    return bcrypt.hashpw(senha_bytes, bcrypt.gensalt()).decode("utf-8")


def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    """Compara a senha digitada com o hash armazenado no banco."""
    try:
        senha_bytes = senha_plana.encode("utf-8")[:72]
        hash_bytes = senha_hash.encode("utf-8")
        return bcrypt.checkpw(senha_bytes, hash_bytes)
    except Exception:
        return False


def criar_token(dados: dict) -> str:
    """Gera um JWT com os dados do usuário e validade de 8h."""
    payload = dados.copy()
    payload["exp"] = datetime.utcnow() + timedelta(hours=EXPIRACAO_HORAS)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
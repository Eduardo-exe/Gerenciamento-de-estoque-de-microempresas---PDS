from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verificar_senha, criar_token
from app.models.usuario import Usuario
from app.schemas.schemas_auth import LoginRequest, LoginResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login(dados: LoginRequest, db: Session = Depends(get_db)):
    # Busca o usuário pelo login
    usuario = db.query(Usuario).filter(Usuario.login == dados.login).first()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
        )

    if not verificar_senha(dados.senha, usuario.senha):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
        )

    # Gera o token com os dados do usuário
    token = criar_token({
        "sub":  usuario.login,
        "id":   usuario.id,
        "tipo": usuario.tipo,
    })

    return LoginResponse(
        access_token=token,
        tipo=usuario.tipo,
        nome=usuario.nome,
    )
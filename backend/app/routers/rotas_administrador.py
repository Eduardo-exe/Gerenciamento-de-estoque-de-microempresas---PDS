from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.administrador import PermissaoSchema, AlterarNivelSchema
from app.services.administrador import (
    listar_usuarios,
    dar_permissao,
    remover_permissao,
    alterar_nivel
)

router = APIRouter()


@router.get("/usuarios")
def get_usuarios(db: Session = Depends(get_db)):
    return listar_usuarios(db)


@router.post("/permissao/dar")
def post_dar_permissao(dados: PermissaoSchema, db: Session = Depends(get_db)):
    return dar_permissao(db, dados.usuario_id, dados.nivel)


@router.post("/permissao/remover")
def post_remover_permissao(dados: PermissaoSchema, db: Session = Depends(get_db)):
    return remover_permissao(db, dados.usuario_id)


@router.put("/permissao/nivel")
def put_alterar_nivel(dados: AlterarNivelSchema, db: Session = Depends(get_db)):
    return alterar_nivel(db, dados.usuario_id, dados.nivel)
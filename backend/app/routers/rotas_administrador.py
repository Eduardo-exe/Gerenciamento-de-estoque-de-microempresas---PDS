from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.administrador import (
    CriarUsuarioSchema,
    AlterarTipoSchema,
    DeletarUsuarioSchema,
)
from app.services.administrador import (
    listar_usuarios,
    criar_usuario,
    alterar_tipo,
    deletar_usuario,
)

router = APIRouter()


@router.get("/usuarios")
def get_usuarios(db: Session = Depends(get_db)):
    return listar_usuarios(db)


@router.post("/usuarios")
def post_criar_usuario(dados: CriarUsuarioSchema, db: Session = Depends(get_db)):
    return criar_usuario(db, dados.nome, dados.login, dados.senha, dados.tipo)


@router.put("/usuarios/tipo")
def put_alterar_tipo(dados: AlterarTipoSchema, db: Session = Depends(get_db)):
    return alterar_tipo(db, dados.usuario_id, dados.tipo)


@router.delete("/usuarios")
def delete_deletar_usuario(dados: DeletarUsuarioSchema, db: Session = Depends(get_db)):
    return deletar_usuario(db, dados.usuario_id)
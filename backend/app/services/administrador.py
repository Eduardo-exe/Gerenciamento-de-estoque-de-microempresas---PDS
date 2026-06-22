from sqlalchemy.orm import Session
from app.models.usuario import Usuario


def listar_usuarios(db: Session):
    usuarios = db.query(Usuario).all()
    return [{"id": u.id, "nome": u.nome, "nivel": u.nivel} for u in usuarios]


def dar_permissao(db: Session, usuario_id: int, nivel: str):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        return {"erro": "Usuário não encontrado"}

    usuario.nivel = nivel
    db.commit()
    db.refresh(usuario)

    return {"mensagem": "Permissão concedida", "usuario": {"id": usuario.id, "nome": usuario.nome, "nivel": usuario.nivel}}


def remover_permissao(db: Session, usuario_id: int):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        return {"erro": "Usuário não encontrado"}

    usuario.nivel = "sem_permissao"
    db.commit()
    db.refresh(usuario)

    return {"mensagem": "Permissão removida", "usuario": {"id": usuario.id, "nome": usuario.nome, "nivel": usuario.nivel}}


def alterar_nivel(db: Session, usuario_id: int, nivel: str):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        return {"erro": "Usuário não encontrado"}

    usuario.nivel = nivel
    db.commit()
    db.refresh(usuario)

    return {"mensagem": "Nível alterado", "usuario": {"id": usuario.id, "nome": usuario.nome, "nivel": usuario.nivel}}
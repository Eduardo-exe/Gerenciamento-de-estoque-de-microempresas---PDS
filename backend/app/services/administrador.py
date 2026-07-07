from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.core.security import hash_senha


def listar_usuarios(db: Session):
    usuarios = db.query(Usuario).all()
    return [{"id": u.id, "nome": u.nome, "login": u.login, "tipo": u.tipo, "ativo": getattr(u, "ativo", True)} for u in usuarios]


def criar_usuario(db: Session, nome: str, login: str, senha: str, tipo: str):
    existe = db.query(Usuario).filter(Usuario.login == login).first()
    if existe:
        return {"erro": "Login já cadastrado"}

    novo = Usuario(
        nome=nome,
        login=login,
        senha=hash_senha(senha),
        tipo=tipo,
        ativo=True,
    )
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return {"mensagem": "Usuário criado com sucesso", "usuario": {"id": novo.id, "nome": novo.nome, "login": novo.login, "tipo": novo.tipo}}


def alterar_tipo(db: Session, usuario_id: int, tipo: str):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        return {"erro": "Usuário não encontrado"}

    usuario.tipo = tipo
    db.commit()
    db.refresh(usuario)
    return {"mensagem": "Cargo atualizado", "usuario": {"id": usuario.id, "nome": usuario.nome, "tipo": usuario.tipo}}


def deletar_usuario(db: Session, usuario_id: int):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        return {"erro": "Usuário não encontrado"}

    db.delete(usuario)
    db.commit()
    return {"mensagem": "Usuário removido"}
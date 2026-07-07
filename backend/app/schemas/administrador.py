from pydantic import BaseModel


class CriarUsuarioSchema(BaseModel):
    nome: str
    login: str
    senha: str
    tipo: str


class AlterarTipoSchema(BaseModel):
    usuario_id: int
    tipo: str


class DeletarUsuarioSchema(BaseModel):
    usuario_id: int
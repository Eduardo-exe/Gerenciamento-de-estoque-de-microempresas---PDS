from pydantic import BaseModel

class PermissaoSchema(BaseModel):
    usuario_id: int
    nivel: str

class AlterarNivelSchema(BaseModel):
    usuario_id: int
    nivel: str
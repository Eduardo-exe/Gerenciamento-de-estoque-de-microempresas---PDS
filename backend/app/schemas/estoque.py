from pydantic import BaseModel


class MovimentacaoEstoque(BaseModel):
    codigo: int
    nome: str
    quantidade: int
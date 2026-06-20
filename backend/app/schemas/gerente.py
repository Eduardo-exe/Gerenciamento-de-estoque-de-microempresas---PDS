from pydantic import BaseModel

class ProdutoSchema(BaseModel):
    codigo: int
    nome: str
    quantidade: int

class ProdutoDeleteSchema(BaseModel):
    codigo: int

class FornecedorSchema(BaseModel):
    cnpj: str
    nome: str
    telefone: str

class FornecedorDeleteSchema(BaseModel):
    cnpj: str
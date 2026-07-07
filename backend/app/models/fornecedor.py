from sqlalchemy import Column, String
from app.core.database import Base

class Fornecedor(Base):
    __tablename__ = "fornecedor"

    cnpj     = Column(String(18), primary_key=True)
    nome     = Column(String(100), nullable=False)
    telefone = Column(String(20), nullable=False)
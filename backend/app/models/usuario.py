from sqlalchemy import Column, Integer, String, Boolean
from app.core.database import Base

class Usuario(Base):
    __tablename__ = "usuario"

    id    = Column(Integer, primary_key=True, index=True)
    nome  = Column(String(100), nullable=False)
    login = Column(String(50), unique=True, nullable=False)
    senha = Column(String(255), nullable=False)
    tipo  = Column(String(20), nullable=False) # Estoquista, gerente ou administrador.
    ativo = Column(Boolean, default=True, nullable=False)
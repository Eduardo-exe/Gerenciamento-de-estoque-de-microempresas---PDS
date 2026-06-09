from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Produto(Base):
    __tablename__ = "produto"

    codigo = Column(Integer, primary_key=True, index=True)
    nome   = Column(String(100), nullable=False)
from sqlalchemy import Column, Integer
from app.core.database import Base

class Estoque(Base):
    __tablename__ = "estoque"

    id = Column(Integer, primary_key=True, index=True)
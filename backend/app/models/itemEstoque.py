from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class ItemEstoque(Base):
    __tablename__ = "item_estoque"

    id             = Column(Integer, primary_key=True, index=True)
    estoque_id     = Column(Integer, ForeignKey("estoque.id"), nullable=False)
    produto_codigo = Column(Integer, ForeignKey("produto.codigo"), nullable=False)
    quantidade     = Column(Integer, nullable=False, default=0)

    produto = relationship("Produto")
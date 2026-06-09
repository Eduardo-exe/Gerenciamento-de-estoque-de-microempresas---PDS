from fastapi import FastAPI
from app.core.database import Base, engine

from app.routers.rotas_estoque import router as rotas_estoque

import app.models.usuario
import app.models.fornecedor
import app.models.produto
import app.models.estoque
import app.models.itemEstoque

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(rotas_estoque)

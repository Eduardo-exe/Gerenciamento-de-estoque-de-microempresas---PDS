from fastapi import FastAPI
from app.core.database import Base, engine

from app.routers.rotas_estoque import router as rotas_estoque
from app.routers.rotas_gerente import router as rotas_gerente
from app.routers.rotas_administrador import router as rotas_admin

import app.models.usuario
import app.models.fornecedor
import app.models.produto
import app.models.estoque
import app.models.itemEstoque

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Estoquista
app.include_router(rotas_estoque, prefix="/estoquista", tags=["Estoquista"])

# Gerente - suas rotas + herda Estoquista
app.include_router(rotas_gerente, prefix="/gerente", tags=["Gerente"])
app.include_router(rotas_estoque, prefix="/gerente", tags=["Gerente"])

# Administrador - suas rotas + herda Gerente + herda Estoquista
app.include_router(rotas_admin, prefix="/admin", tags=["Administrador"])
app.include_router(rotas_gerente, prefix="/admin", tags=["Administrador"])
app.include_router(rotas_estoque, prefix="/admin", tags=["Administrador"])
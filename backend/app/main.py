from fastapi import FastAPI

from routers.rotas_estoque import router as rotas_estoque

app = FastAPI()

app.include_router(rotas_estoque)
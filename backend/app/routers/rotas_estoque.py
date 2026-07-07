from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.estoque import MovimentacaoEstoque
from app.services.estoquista import (
    consultar_estoque,
    registrar_entrada,
    registrar_saida
)

router = APIRouter()


@router.get("/estoque")
def get_estoque(db: Session = Depends(get_db)):
    return consultar_estoque(db)


@router.post("/estoque/entrada")
def post_entrada(dados: MovimentacaoEstoque, db: Session = Depends(get_db)):
    return registrar_entrada(db, dados.codigo, dados.nome, dados.quantidade)


@router.post("/estoque/saida")
def post_saida(dados: MovimentacaoEstoque, db: Session = Depends(get_db)):
    return registrar_saida(db, dados.codigo, dados.nome, dados.quantidade)
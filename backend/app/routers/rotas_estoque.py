from fastapi import APIRouter

from services.estoquista import (
    consultar_estoque,
    registrar_entrada,
    registrar_saida
)

router = APIRouter()


@router.get("/estoque")
def estoque():

    return consultar_estoque()


@router.post("/entrada")
def entrada(codigo: int, quantidade: int):

    return registrar_entrada(codigo, quantidade)


@router.post("/saida")
def saida(codigo: int, quantidade: int):

    return registrar_saida(codigo, quantidade)
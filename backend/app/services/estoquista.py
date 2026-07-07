from sqlalchemy.orm import Session
from app.models.produto import Produto
from app.models.itemEstoque import ItemEstoque


def consultar_estoque(db: Session):
    itens = db.query(ItemEstoque).join(Produto).all()

    resultado = []
    for item in itens:
        resultado.append({
            "codigo": item.produto.codigo,
            "nome": item.produto.nome,
            "quantidade": item.quantidade
        })

    return resultado


def registrar_entrada(db: Session, codigo: int, nome: str, quantidade: int):
    item = (
        db.query(ItemEstoque)
        .join(Produto)
        .filter(Produto.codigo == codigo)
        .first()
    )

    if not item:
        return {"erro": "Produto não encontrado"}

    if item.produto.nome != nome:
        return {"erro": "Nome do produto não corresponde ao código informado"}

    item.quantidade += quantidade
    db.commit()
    db.refresh(item)

    return {
        "mensagem": "Entrada registrada",
        "produto": {
            "codigo": item.produto.codigo,
            "nome": item.produto.nome,
            "quantidade": item.quantidade
        }
    }


def registrar_saida(db: Session, codigo: int, nome: str, quantidade: int):
    item = (
        db.query(ItemEstoque)
        .join(Produto)
        .filter(Produto.codigo == codigo)
        .first()
    )

    if not item:
        return {"erro": "Produto não encontrado"}

    if item.produto.nome != nome:
        return {"erro": "Nome do produto não corresponde ao código informado"}

    if item.quantidade < quantidade:
        return {"erro": "Estoque insuficiente"}

    item.quantidade -= quantidade
    db.commit()
    db.refresh(item)

    return {
        "mensagem": "Saída registrada",
        "produto": {
            "codigo": item.produto.codigo,
            "nome": item.produto.nome,
            "quantidade": item.quantidade
        }
    }
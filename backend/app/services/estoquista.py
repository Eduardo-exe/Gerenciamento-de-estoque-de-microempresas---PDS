produtos = [
    {"codigo": 1, "nome": "Teclado", "quantidade": 20},
    {"codigo": 2, "nome": "Mouse", "quantidade": 35},
    {"codigo": 3, "nome": "Monitor", "quantidade": 10}
]


def consultar_estoque():
    return produtos


def registrar_entrada(codigo, quantidade):

    for produto in produtos:

        if produto["codigo"] == codigo:

            produto["quantidade"] += quantidade

            return {
                "mensagem": "Entrada registrada",
                "produto": produto
            }

    return {"erro": "Produto não encontrado"}


def registrar_saida(codigo, quantidade):

    for produto in produtos:

        if produto["codigo"] == codigo:

            if produto["quantidade"] < quantidade:

                return {"erro": "Estoque insuficiente"}

            produto["quantidade"] -= quantidade

            return {
                "mensagem": "Saída registrada",
                "produto": produto
            }

    return {"erro": "Produto não encontrado"}
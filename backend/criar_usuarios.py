"""
Script para criar usuários de teste no banco de dados.
Execute UMA VEZ de dentro da pasta backend/:

    python criar_usuarios.py

Usuários criados:
    login: estoquista  | senha: estoque123  | tipo: estoquista
    login: gerente     | senha: gerente123  | tipo: gerente
    login: admin       | senha: admin123    | tipo: administrador
"""

import sys
import os

# Garante que o Python enxerga o pacote app/
sys.path.insert(0, os.path.dirname(__file__))

from app.core.database import SessionLocal, engine, Base
from app.core.security import hash_senha
from app.models.usuario import Usuario

# Importa todos os models para o create_all enxergar as tabelas
import app.models.usuario
import app.models.produto
import app.models.estoque
import app.models.itemEstoque
import app.models.fornecedor

USUARIOS = [
    {"nome": "João Estoquista", "login": "estoquista", "senha": "estoque123", "tipo": "estoquista"},
    {"nome": "Maria Gerente",   "login": "gerente",    "senha": "gerente123", "tipo": "gerente"},
    {"nome": "Carlos Admin",    "login": "admin",      "senha": "admin123",   "tipo": "administrador"},
]


def main():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        criados = 0
        for dados in USUARIOS:
            existe = db.query(Usuario).filter(Usuario.login == dados["login"]).first()
            if existe:
                print(f"  [já existe]  {dados['login']}")
                continue

            usuario = Usuario(
                nome=dados["nome"],
                login=dados["login"],
                senha=hash_senha(dados["senha"]),
                tipo=dados["tipo"],
            )
            db.add(usuario)
            criados += 1
            print(f"  [criado]     {dados['login']}  ({dados['tipo']})")

        db.commit()
        print(f"\n{criados} usuário(s) criado(s) com sucesso.")

    except Exception as e:
        db.rollback()
        print(f"\nErro: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
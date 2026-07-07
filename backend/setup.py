"""
G-Estoque — Script de configuração inicial do banco de dados.
Execute UMA VEZ de dentro da pasta backend/ após configurar o .env:

    python setup.py

O que esse script faz:
    1. Cria todas as tabelas no banco (se não existirem)
    2. Adiciona a coluna 'ativo' na tabela usuario (se não existir)
    3. Cria os usuários padrão do sistema
    4. Popula produtos, estoque e fornecedores com dados de exemplo
"""

import sys
import os

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.dirname(__file__))

from app.core.database import SessionLocal, engine, Base
from app.core.security import hash_senha

# Importa todos os models para o create_all enxergar as tabelas
import app.models.usuario
import app.models.produto
import app.models.estoque
import app.models.itemEstoque
import app.models.fornecedor

from app.models.usuario     import Usuario
from app.models.produto     import Produto
from app.models.estoque     import Estoque
from app.models.itemEstoque import ItemEstoque
from app.models.fornecedor  import Fornecedor

from sqlalchemy import text, inspect


# ── Dados de exemplo ──────────────────────────────────────────────────────────

USUARIOS = [
    {"nome": "João Estoquista", "login": "estoquista", "senha": "estoque123", "tipo": "estoquista"},
    {"nome": "Maria Gerente",   "login": "gerente",    "senha": "gerente123", "tipo": "gerente"},
    {"nome": "Carlos Admin",    "login": "admin",      "senha": "admin123",   "tipo": "administrador"},
]

PRODUTOS = [
    {"codigo": 1,  "nome": "Teclado USB"},
    {"codigo": 2,  "nome": "Mouse Óptico"},
    {"codigo": 3,  "nome": "Monitor 24\""},
    {"codigo": 4,  "nome": "Cabo de Rede Cat6"},
    {"codigo": 5,  "nome": "Papel A4 (Resma)"},
    {"codigo": 6,  "nome": "Caneta Esferográfica"},
    {"codigo": 7,  "nome": "Grampeador"},
    {"codigo": 8,  "nome": "Fita Adesiva"},
    {"codigo": 9,  "nome": "Pen Drive 32GB"},
    {"codigo": 10, "nome": "Cartucho de Tinta"},
]

# Quantidades: alguns com estoque baixo (≤10) para mostrar badge "Baixo"
QUANTIDADES = {
    1:  35,   # Normal
    2:  42,   # Normal
    3:  8,    # Baixo
    4:  60,   # Normal
    5:  25,   # Normal
    6:  5,    # Baixo
    7:  18,   # Normal
    8:  7,    # Baixo
    9:  30,   # Normal
    10: 4,    # Baixo
}

FORNECEDORES = [
    {"cnpj": "11.222.333/0001-44", "nome": "TechSupply Ltda",       "telefone": "(98) 3211-4567"},
    {"cnpj": "22.333.444/0001-55", "nome": "Papelaria Central",     "telefone": "(98) 3222-8901"},
    {"cnpj": "33.444.555/0001-66", "nome": "InfoParts Distribuidora","telefone": "(98) 3233-2345"},
]


# ── Funções de setup ──────────────────────────────────────────────────────────

def step(msg: str):
    print(f"\n  {msg}")

def ok(msg: str):
    print(f"    [OK]  {msg}")

def skip(msg: str):
    print(f"    [-]   {msg} (já existe, pulando)")


def criar_tabelas():
    step("Criando tabelas...")
    Base.metadata.create_all(bind=engine)
    ok("Tabelas criadas/verificadas com sucesso.")


def adicionar_coluna_ativo(db):
    step("Verificando coluna 'ativo' na tabela usuario...")
    inspector = inspect(engine)
    colunas = [c["name"] for c in inspector.get_columns("usuario")]

    if "ativo" not in colunas:
        db.execute(text("ALTER TABLE usuario ADD COLUMN ativo BOOLEAN NOT NULL DEFAULT TRUE"))
        db.commit()
        ok("Coluna 'ativo' adicionada.")
    else:
        skip("Coluna 'ativo'")


def criar_usuarios(db):
    step("Criando usuários padrão...")
    criados = 0
    for dados in USUARIOS:
        existe = db.query(Usuario).filter(Usuario.login == dados["login"]).first()
        if existe:
            skip(f"Usuário '{dados['login']}'")
            continue
        usuario = Usuario(
            nome=dados["nome"],
            login=dados["login"],
            senha=hash_senha(dados["senha"]),
            tipo=dados["tipo"],
            ativo=True,
        )
        db.add(usuario)
        criados += 1
        ok(f"Usuário '{dados['login']}' criado ({dados['tipo']})")
    db.commit()
    if criados == 0:
        print("    —  Todos os usuários já existiam.")


def popular_produtos(db):
    step("Populando produtos...")
    criados = 0
    for p in PRODUTOS:
        existe = db.query(Produto).filter(Produto.codigo == p["codigo"]).first()
        if existe:
            skip(f"Produto '{p['nome']}'")
            continue
        db.add(Produto(codigo=p["codigo"], nome=p["nome"]))
        criados += 1
        ok(f"Produto '{p['nome']}' adicionado.")
    db.commit()
    if criados == 0:
        print("    —  Todos os produtos já existiam.")


def popular_estoque(db):
    step("Configurando estoque...")

    estoque = db.query(Estoque).first()
    if not estoque:
        estoque = Estoque()
        db.add(estoque)
        db.commit()
        db.refresh(estoque)
        ok(f"Estoque principal criado (id={estoque.id}).")
    else:
        skip(f"Estoque principal (id={estoque.id})")

    criados = 0
    for codigo, quantidade in QUANTIDADES.items():
        produto = db.query(Produto).filter(Produto.codigo == codigo).first()
        if not produto:
            continue
        existe = db.query(ItemEstoque).filter(
            ItemEstoque.estoque_id == estoque.id,
            ItemEstoque.produto_codigo == codigo
        ).first()
        if existe:
            skip(f"Item '{produto.nome}' no estoque")
            continue
        db.add(ItemEstoque(
            estoque_id=estoque.id,
            produto_codigo=codigo,
            quantidade=quantidade,
        ))
        criados += 1
        ok(f"'{produto.nome}' → {quantidade} unidades")
    db.commit()
    if criados == 0:
        print("    —  Todos os itens de estoque já existiam.")


def popular_fornecedores(db):
    step("Populando fornecedores...")
    criados = 0
    for f in FORNECEDORES:
        existe = db.query(Fornecedor).filter(Fornecedor.cnpj == f["cnpj"]).first()
        if existe:
            skip(f"Fornecedor '{f['nome']}'")
            continue
        db.add(Fornecedor(cnpj=f["cnpj"], nome=f["nome"], telefone=f["telefone"]))
        criados += 1
        ok(f"Fornecedor '{f['nome']}' adicionado.")
    db.commit()
    if criados == 0:
        print("    —  Todos os fornecedores já existiam.")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("\n" + "=" * 50)
    print("  G-Estoque — Setup do banco de dados")
    print("=" * 50)

    criar_tabelas()
    db = SessionLocal()

    try:
        adicionar_coluna_ativo(db)
        criar_usuarios(db)
        popular_produtos(db)
        popular_estoque(db)
        popular_fornecedores(db)

        print("\n" + "=" * 50)
        print("  Setup concluído com sucesso!")
        print("=" * 50)
        print("""
  Usuários criados:
    login: estoquista  |  senha: estoque123
    login: gerente     |  senha: gerente123
    login: admin       |  senha: admin123

  Próximo passo:
    cd backend
    uvicorn app.main:app --reload
""")

    except Exception as e:
        db.rollback()
        print(f"\n  ERRO durante o setup: {e}")
        print("  Verifique se o banco está rodando e o .env está configurado.")
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
# Arquitetura: Backend (FastAPI)

O backend do **G-Estoque** é construído em Python utilizando **FastAPI**, estruturado de forma modular para garantir manutenibilidade, testabilidade e separação de lógica.

---

## 📂 Estrutura de Diretórios do Backend

```
backend/
├── app/
│   ├── main.py              # Ponto de entrada, configuração de CORS e roteadores
│   ├── core/
│   │   ├── database.py      # Configuração do motor SQLAlchemy e sessão get_db
│   │   └── security.py      # Funções de hashing Bcrypt e geração/validação JWT
│   ├── models/
│   │   ├── usuario.py       # Modelo ORM Usuario (com campo ativo)
│   │   ├── estoque.py       # Modelos ORM Estoque, ItemEstoque e Produto
│   │   └── gerente.py       # Modelo ORM Fornecedor
│   ├── schemas/
│   │   ├── schemas_auth.py  # Schemas Pydantic para Login (Request e Response)
│   │   ├── estoque.py       # Schemas Pydantic para movimentação de estoque
│   │   ├── gerente.py       # Schemas Pydantic de Produtos e Fornecedores
│   │   └── administrador.py # Schemas Pydantic para gestão de usuários
│   ├── services/
│   │   ├── estoque.py       # Lógica de negócio: validação de estoque e saldo
│   │   ├── gerente.py       # Lógica de negócio: cadastros e geração de PDF ReportLab
│   │   └── administrador.py # Lógica de negócio: CRUD e promoções de usuários
│   └── routers/
│       ├── routers_auth.py  # Rota de autenticação /auth/login
│       ├── rotas_estoque.py # Endpoints de consulta e movimentação do estoquista
│       ├── rotas_gerente.py # Endpoints gerenciais (produtos, fornecedores, PDF)
│       └── rotas_administrador.py # Endpoints de usuários (CRUD e permissões)
├── setup.py                 # Script de inicialização, migração e seed do SQLite
└── requirements.txt         # Dependências python do servidor
```

---

## 🔀 Sistema de Roteamento e Herança de Privilégios

Em vez de verificar permissões individualmente com `if/else` dentro de cada função gerencial, o **G-Estoque** implementa a herança de acessos na própria montagem dos roteadores no arquivo principal `app/main.py`:

```python
# 1. Rotas do Estoquista: montadas apenas no prefixo /estoquista
app.include_router(rotas_estoque.router, prefix="/estoquista", tags=["Estoquista"])

# 2. Rotas do Gerente: montadas em /gerente
# O Gerente herda as rotas de estoque, pois as rotas de estoque também são incluídas sob /gerente
app.include_router(rotas_estoque.router, prefix="/gerente", tags=["Estoque (Gerente)"])
app.include_router(rotas_gerente.router, prefix="/gerente", tags=["Gerente"])

# 3. Rotas do Administrador: montadas em /admin
# O Administrador herda tudo do gerente e do estoquista + suas rotas exclusivas
app.include_router(rotas_estoque.router, prefix="/admin", tags=["Estoque (Admin)"])
app.include_router(rotas_gerente.router, prefix="/admin", tags=["Gerente (Admin)"])
app.include_router(rotas_administrador.router, prefix="/admin", tags=["Administrador"])
```

Essa arquitetura garante que uma requisição disparada pelo frontend logado como `admin` para `/admin/relatorio/pdf` ou `/admin/estoque` acione exatamente os mesmos serviços validados sem duplicação de código.

---

## 🛡️ Segurança Criptográfica (`core/security.py`)

A segurança é estruturada sobre dois pilares:
1. **Hashing Bcrypt Nativo:** Para evitar problemas de compatibilidade e obsolescência com abstrações de terceiros, o sistema utiliza chamadas nativas ao módulo `bcrypt`. As senhas são truncadas em até 72 bytes com `senha.encode("utf-8")[:72]` para respeitar os limites do algoritmo Blowfish do Bcrypt antes de receberem o Salt gerado por `bcrypt.gensalt()`.
2. **JSON Web Tokens (JWT):** Na autenticação em `/auth/login`, se o login e senha forem validados, o servidor emite um token JWT assinado digitalmente usando o algoritmo `HS256` contendo o ID do usuário, seu login (`sub`), seu cargo (`tipo`) e um tempo de expiração (`exp`) de 8 horas.

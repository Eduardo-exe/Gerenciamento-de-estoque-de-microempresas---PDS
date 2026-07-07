# 📦 G-Estoque - Sistema de Gerenciamento de Estoque para Microempresas

Sistema desenvolvido para a disciplina de **Projeto e Desenvolvimento de Software (PDS)** com o objetivo de automatizar o gerenciamento de estoque de microempresas, permitindo o controle de produtos, fornecedores, movimentações de estoque e gerenciamento de usuários através de diferentes níveis de acesso.

O projeto foi desenvolvido seguindo princípios de **Engenharia de Software**, utilizando **UML** para modelagem, arquitetura em camadas e separação das responsabilidades entre Backend, Frontend e Banco de Dados.

---

# 👨‍💻 Desenvolvedores

- Eduardo Oliveira
- Gabriel Patrick
- Marcelo Almeida
- Thalita Amorim

---

# 📋 Funcionalidades

O sistema possui três perfis de usuários:

## 📦 Estoquista

- Realizar login
- Consultar estoque
- Registrar entrada de produtos
- Registrar saída de produtos

---

## 👨‍💼 Gerente

Herda todas as permissões do Estoquista e pode:

- Cadastrar produtos
- Atualizar produtos
- Remover produtos
- Cadastrar fornecedores
- Atualizar fornecedores
- Remover fornecedores
- Consultar CNPJ de fornecedores

---

## 👨‍💻 Administrador

Responsável pelo gerenciamento do sistema.

Pode:

- Gerenciar usuários
- Criar usuários
- Atualizar usuários
- Alterar permissões
- Alterar níveis de acesso
- Ativar ou desativar usuários

---

# 🏗 Arquitetura do Projeto

O projeto foi dividido em três grandes componentes.

```
Projeto
│
├── backend
│
├── frontend
│
├── Diagramas
│
└── documentação
```

---

## Backend

Desenvolvido em **Python** utilizando **FastAPI**.

Responsável por:

- API REST
- Autenticação
- Regras de negócio
- Persistência dos dados
- Controle de acesso
- Integração com banco de dados

Estrutura:

```
backend
│
├── app
│   ├── core
│   ├── models
│   ├── routers
│   ├── schemas
│   ├── services
│   └── main.py
│
├── setup.py
│
└── requirements.txt
```

---

## Frontend

Desenvolvido utilizando **Flet**.

Estrutura:

```
frontend
│
├── api
├── assets
├── views
├── state.py
└── app.py
```

---

## Banco de Dados

O projeto utiliza **SQLAlchemy** como ORM.

O banco é inicializado automaticamente através do script:

```
backend/setup.py
```

---

# 📐 Diagramas UML

A documentação do sistema foi construída utilizando UML.

Foram desenvolvidos:

- Diagrama de Casos de Uso
- Diagrama de Classes
- Diagramas de Atividades
- Diagramas de Sequência

Todos os diagramas encontram-se na pasta:

```
Diagramas/
```

---

# 📖 Casos de Uso

## Estoquista

- Fazer Login
- Consultar Estoque
- Registrar Entrada
- Registrar Saída

---

## Gerente

Além das funções do Estoquista:

- Cadastrar Produto
- Atualizar Produto
- Excluir Produto
- Cadastrar Fornecedor
- Atualizar Fornecedor
- Excluir Fornecedor
- Consultar CNPJ

---

## Administrador

- Criar Usuário
- Atualizar Usuário
- Alterar Permissões
- Gerenciar Níveis de Acesso

---

# 🏛 Arquitetura de Software

A arquitetura segue o padrão em camadas.

```
Frontend

↓

Routers

↓

Services

↓

Models

↓

Banco de Dados
```

Cada camada possui uma responsabilidade específica.

### Routers

Recebem as requisições HTTP.

### Services

Contêm toda regra de negócio.

### Models

Representam as entidades persistidas no banco.

### Schemas

Realizam validação dos dados de entrada e saída.

### Core

Configurações do sistema:

- Banco
- Segurança
- Autenticação

---

# 🔐 Regras de Negócio

## Login

O sistema valida:

- usuário
- senha
- usuário ativo

Caso inválido:

- acesso negado

---

## Produtos

Todo produto possui:

- código
- nome
- quantidade

O sistema impede:

- produtos duplicados
- códigos inválidos

---

## Estoque

Toda movimentação:

Entrada

↓

Atualiza quantidade

Saída

↓

Atualiza quantidade

Caso não exista saldo suficiente:

- operação cancelada

---

## Fornecedores

Cada fornecedor possui:

- Nome
- CNPJ
- Telefone

O CNPJ pode ser validado antes do cadastro.

---

# 🛠 Tecnologias Utilizadas

## Backend

- Python
- FastAPI
- SQLAlchemy
- Uvicorn

---

## Frontend

- Python
- Flet

---

## Banco de Dados

- SQLAlchemy
- SQLite

---

## Modelagem

- UML 2.5
- PlantUML
- StarUML

---

# 🚀 Como Executar o Projeto

## 1. Clonar o Repositório

```bash
git clone https://github.com/Eduardo-exe/Gerenciamento-de-estoque-de-microempresas---PDS.git

cd Gerenciamento-de-estoque-de-microempresas---PDS
```

---

## 2. Criar Ambiente Virtual

Na raiz do projeto:

```bash
python -m venv .venv
```

---

## 3. Ativar Ambiente Virtual

Windows

```bash
.venv\Scripts\activate
```

Linux

```bash
source .venv/bin/activate
```

---

## 4. Instalar Dependências do Backend

Entre na pasta:

```bash
cd backend
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

---

## 5. Inicializar o Banco

Ainda dentro da pasta backend:

```bash
python setup.py
```

Esse script cria automaticamente:

- tabelas
- usuários
- produtos
- estoque
- fornecedores

Caso o banco já exista, apenas verifica e atualiza a estrutura quando necessário.

---

## 6. Executar a API

Ainda dentro da pasta backend:

```bash
python -m uvicorn app.main:app --reload
```

A API ficará disponível em:

```
http://127.0.0.1:8000
```

Swagger:

```
http://127.0.0.1:8000/docs
```

ReDoc:

```
http://127.0.0.1:8000/redoc
```

---

## 7. Executar o Frontend

Abra um novo terminal.

Entre na pasta:

```bash
cd frontend
```

Execute:

```bash
python app.py
```

O aplicativo será iniciado automaticamente utilizando Flet.

---

# 👥 Usuários Padrão

Após executar o setup, o sistema cria automaticamente os seguintes usuários:

| Perfil | Login | Senha |
|---------|--------|--------|
| Administrador | admin | admin123 |
| Gerente | gerente | gerente123 |
| Estoquista | estoquista | estoque123 |

---

# 📚 Documentação

O projeto utiliza **MkDocs** com **Material for MkDocs**.

Instale:

```bash
pip install mkdocs-material
```

Na raiz do projeto execute:

```bash
mkdocs serve
```

A documentação ficará disponível em:

```
http://127.0.0.1:8000
```

Caso a API já esteja utilizando a porta 8000, execute:

```bash
mkdocs serve -a 127.0.0.1:8001
```

e acesse:

```
http://127.0.0.1:8001
```

---

# 📁 Estrutura do Projeto

```
Gerenciamento-de-estoque-de-microempresas---PDS
│
├── backend
│   ├── app
│   │   ├── core
│   │   ├── models
│   │   ├── routers
│   │   ├── schemas
│   │   ├── services
│   │   └── main.py
│   │
│   ├── setup.py
│   └── requirements.txt
│
├── frontend
│   ├── api
│   ├── assets
│   ├── views
│   ├── app.py
│   └── state.py
│
├── Diagramas
│
├── site
│
├── mkdocs.yml
│
└── README.md
```

---

# 📄 Licença

Projeto desenvolvido exclusivamente para fins acadêmicos na disciplina de Projeto e Desenvolvimento de Software (PDS).

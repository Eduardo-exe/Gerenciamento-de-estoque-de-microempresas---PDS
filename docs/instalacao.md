# Guia de Instalação Passo a Passo

Este guia descreve como configurar todo o ambiente do projeto **G-Estoque** a partir do código-fonte em um sistema operacional Windows.

---

## 📋 Pré-requisitos

Antes de começar, certifique-se de ter instalado em sua máquina:
- **Python 3.10 ou superior** (com a opção *Add Python to PATH* marcada na instalação).
- **Git** (para clonar ou gerenciar o repositório).

---

## ⚙️ 1. Clone e Ambiente Virtual

Abra um terminal (PowerShell ou Prompt de Comando) na pasta onde deseja rodar o projeto e execute os comandos abaixo:

```powershell
# 1. Entre na pasta raiz do repositório
cd Gerenciamento-de-estoque-de-microempresas---PDS

# 2. Crie o ambiente virtual Python (.venv)
python -m venv .venv

# 3. Ative o ambiente virtual (PowerShell)
.\.venv\Scripts\Activate.ps1
# (Ou no CMD: .\.venv\Scripts\activate.bat)
```

> [!TIP]
> Se o PowerShell exibir erro de política de execução de scripts, rode o comando:
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

---

## 📦 2. Instalação das Dependências

Com o ambiente virtual ativo (você verá `(.venv)` no início do terminal), instale as dependências listadas no arquivo `requirements.txt`:

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

Isso instalará automaticamente o **FastAPI**, **Uvicorn**, **SQLAlchemy**, **Flet Desktop**, **Bcrypt**, **ReportLab**, **PyJWT** e o **MkDocs Material**.

---

## 🗄️ 3. Setup e População do Banco de Dados

O backend possui um script automatizado (`setup.py`) que inicializa o banco SQLite, cria as tabelas relacionais necessárias e insere os dados iniciais padrão (3 usuários, 10 produtos de exemplo, acervo inicial e 3 fornecedores).

Execute a inicialização do banco:

```powershell
# 1. Entre no diretório do backend
cd backend

# 2. Rode o setup da aplicação
python setup.py
```

Você verá no terminal uma saída com sinais de confirmação `[OK]` indicando que as tabelas foram criadas e os usuários iniciais foram cadastrados com sucesso.

---

## 🚀 4. Executando o Servidor Backend (API)

O backend deve permanecer rodando em um terminal para responder às requisições da interface gráfica.

Ainda no terminal dentro da pasta `backend`, inicie o servidor **Uvicorn**:

```powershell
uvicorn app.main:app --reload --port 8000
```

> [!NOTE]
> O servidor estará rodando em `http://127.0.0.1:8000`. Você pode acessar a documentação interativa automática da API no seu navegador acessando **`http://127.0.0.1:8000/docs`** (Swagger UI).

---

## 🖥️ 5. Executando o Aplicativo Frontend (UI Desktop)

Abra **uma nova janela de terminal** (mantendo a primeira janela do backend aberta e rodando), ative o ambiente virtual nessa nova janela e inicie a interface do Flet:

```powershell
# 1. Ative o ambiente virtual no novo terminal
.\.venv\Scripts\Activate.ps1

# 2. Entre no diretório do frontend
cd frontend

# 3. Inicie o aplicativo Flet Desktop
python app.py
```

A janela nativa do **G-Estoque** será aberta exibindo a tela de Login!

---

## 🔑 Credenciais Padrão de Acesso

O script `setup.py` cria 3 perfis para você testar todas as camadas do sistema:

| Perfil | Login | Senha Padrão | Nível de Acesso |
| :--- | :--- | :--- | :--- |
| **Estoquista** | `estoquista` | `estoque123` | Movimentação de estoque e consultas. |
| **Gerente** | `gerente` | `gerente123` | Movimentação + Cadastro de Produtos/Fornecedores + Emissão de PDF. |
| **Administrador** | `admin` | `admin123` | Acesso total, incluindo o Painel de Gestão de Usuários. |

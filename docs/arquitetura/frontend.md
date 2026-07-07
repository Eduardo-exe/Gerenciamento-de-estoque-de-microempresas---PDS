# Arquitetura: Frontend (Flet Python Desktop)

O frontend do **G-Estoque** é construído na tecnologia nativa **Flet**, que compila código estruturado em Python para componentes nativos do motor gráfico Flutter, fornecendo uma experiência desktop fluida, moderna e sem necessidade de navegadores web ou HTML.

---

## 📂 Estrutura de Diretórios do Frontend

```
frontend/
├── app.py                   # Inicialização da janela Flet, controle de rotas e segregação SPA
├── state.py                 # Estado global da sessão (token, tipo, nome, login do usuário)
├── api/
│   ├── __init__.py
│   └── client.py            # Camada única de comunicação REST HTTP (requests) com o Backend
└── views/
    ├── __init__.py
    ├── login.py             # View SPA da tela de Autenticação inicial
    ├── estoquista.py        # View SPA do painel operacional (3 abas)
    ├── gerente.py           # View SPA do painel gerencial (5 abas)
    └── admin.py             # View SPA do painel supremo com gestão de usuários (8 abas)
```

---

## 🧭 Roteamento SPA e Travas de Segurança (`app.py`)

Em vez de recarregar janelas do sistema operacional, o Flet opera no modelo **Single Page Application (SPA)** gerenciando uma pilha de visualizações (`page.views`).

Quando a rota muda (evento `on_route_change`), o sistema executa verificações de segurança antes de renderizar a tela solicitada:

```python
def route_change(e):
    page.views.clear()
    
    # 1. Tela de Login sempre permitida para início de sessão
    if page.route == "/login":
        page.views.append(login_view(page))
    
    # 2. Verificação de Acesso: Estoquista só pode entrar em /estoquista
    elif page.route == "/estoquista":
        if get_state().get("tipo") in ("estoquista", "gerente", "admin"):
            page.views.append(estoquista_view(page))
        else:
            page.push_route("/login")
            
    # 3. Trava Gerencial: Estoquistas são bloqueados na rota de Gerente
    elif page.route == "/gerente":
        if get_state().get("tipo") in ("gerente", "admin"):
            page.views.append(gerente_view(page))
        else:
            page.push_route("/estoquista")
            
    # 4. Trava Suprema: Apenas administradores entram em /admin
    elif page.route == "/admin":
        if get_state().get("tipo") == "admin":
            page.views.append(admin_view(page))
        else:
            page.push_route("/login")
```

Essa barreira no frontend impede que usuários tentem forçar a entrada em telas não autorizadas pela URL interna do Flet.

---

## 💾 Gerenciamento de Estado (`state.py`)

O arquivo `state.py` exporta um dicionário global em memória (`_state`) que armazena as variáveis vitais do usuário ativo na sessão do Desktop:

```python
_state = {
    "token": None, # Armazena o JWT devolvido no login
    "tipo":  None, # Cargo do usuário ("estoquista", "gerente" ou "admin")
    "nome":  None, # Nome completo exibido nas saudações do cabeçalho
    "login": None  # Nome do login digitado (usado para prevenir autoexclusão no admin)
}
```

Quando um usuário clica em **Sair**, a função `clear_state()` zera imediatamente essas chaves e limpa o token armazenado na instância do `ApiClient`.

---

## 🌐 Camada de Cliente HTTP (`api/client.py`)

Para manter as Views (`views/*.py`) limpas e focadas apenas em componentes visuais (botões, tabelas, caixas de diálogo), toda requisição de rede ao backend é encapsulada nos métodos da classe `ApiClient`.

- **Headers Automáticos:** Ao fazer login, a resposta JWT é armazenada por `api.set_token(token)`. A partir desse momento, qualquer requisição (`api.registrar_entrada()`, `api.get_usuarios()`, etc.) invoca o método privado `_headers()`, que anexa `{"Authorization": f"Bearer {self._token}"}` à requisição.
- **Tratamento de Exceções:** Os métodos do cliente são encapsulados em blocos `try/except` que capturam `requests.exceptions.ConnectionError` e `Timeout`, devolvendo dicionários estruturados como `{"erro": "Servidor indisponível"}` para que a interface exiba alertas visuais em vermelho sem fechar ou quebrar a janela do usuário.

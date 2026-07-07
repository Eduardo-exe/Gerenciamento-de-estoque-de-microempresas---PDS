# Diagramas: Arquitetura de Classes

Este documento apresenta a modelagem estrutural do sistema através dos seus **Diagramas de Classe**.

---

## 🏛️ Diagrama Oficial de Classes

Abaixo está o diagrama de classes oficial do sistema, modelando as entidades, atributos e métodos principais da aplicação:

<object data="../assets/DIAGRAMA DE CLASSE.pdf" type="application/pdf" width="100%" height="800px">
  <p>Seu navegador não suporta a visualização de PDFs. <a href="../assets/DIAGRAMA%20DE%20CLASSE.pdf">Clique aqui para baixar o PDF do Diagrama de Classes.</a></p>
</object>

---

## Estrutura Complementar do Frontend (Flet)

No lado da apresentação desktop (`frontend/`), as responsabilidades foram organizadas para separar controle de sessão de renderização gráfica. Aqui está uma visualização complementar da arquitetura implementada:

```mermaid
classDiagram
    class ApiClient {
        -string _token
        -dict _headers()
        +set_token(token)
        +clear()
        +login(login, senha) Dict
        +get_estoque() List
    }

    class StateController {
        -dict _state
        +get_state() dict
        +set_state(key, val)
        +clear_state()
    }

    class AppRouter {
        +main(page: Page)
        +route_change(e)
    }

    class Views {
        <<enumeration>>
        +login_view(page) View
        +estoquista_view(page) View
        +gerente_view(page) View
        +admin_view(page) View
    }

    AppRouter --> Views : empilha e renderiza (SPA)
    AppRouter --> StateController : valida permissões
    Views --> ApiClient : envia requisições HTTP REST
    Views --> StateController : lê/atualiza token e cargo
```

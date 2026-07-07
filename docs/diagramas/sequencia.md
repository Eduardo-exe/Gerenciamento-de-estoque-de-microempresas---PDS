# Diagramas: Sequência

Este documento contém os **Diagramas de Sequência** detalhando as interações entre o usuário, a interface Flet, e a API FastAPI, focando nas operações de Estoquista, Gerente e Administrador.

---

## 1. Sequência: Estoquista (Movimentação de Estoque)

Este diagrama ilustra a comunicação cliente-servidor durante um registro de entrada de mercadorias.

<object data="../assets/DIGRAMA DE SEQUENCIA - ESTOQUISTA.pdf" type="application/pdf" width="100%" height="800px">
  <p>Seu navegador não suporta a visualização de PDFs. <a href="../assets/DIGRAMA%20DE%20SEQUENCIA%20-%20ESTOQUISTA.pdf">Baixar PDF</a></p>
</object>

**Fluxo em Mermaid:**
```mermaid
sequenceDiagram
    actor E as Estoquista
    participant UI as Flet UI (Frontend)
    participant API as FastAPI (Backend)
    participant DB as SQLite (Banco)

    E->>UI: Clica em "Registrar Entrada" (Cod: 10, Qtd: 5)
    UI->>API: POST /estoquista/entrada {cod: 10, qtd: 5} + JWT
    API->>API: Valida Token JWT (Cargo: Estoquista)
    API->>DB: SELECT * FROM ItemEstoque WHERE cod = 10
    DB-->>API: Retorna Item (Saldo Atual: 20)
    API->>DB: UPDATE ItemEstoque SET quantidade = 25
    DB-->>API: Confirmação de UPDATE
    API-->>UI: 200 OK {"msg": "Sucesso", "novo_saldo": 25}
    UI-->>E: Exibe Alerta Verde (Operação Concluída)
    UI->>UI: Atualiza tabela de estoque na tela
```

---

## 2. Sequência: Gerente (Gestão de Fornecedores)

Este fluxo demonstra a criação de um novo fornecedor pelo Gerente.

<object data="../assets/DIAGRAMA DE SEQUENCIA - GERENTE.pdf" type="application/pdf" width="100%" height="800px">
  <p>Seu navegador não suporta a visualização de PDFs. <a href="../assets/DIAGRAMA%20DE%20SEQUENCIA%20-%20GERENTE.pdf">Baixar PDF</a></p>
</object>

**Fluxo em Mermaid:**
```mermaid
sequenceDiagram
    actor G as Gerente
    participant UI as Flet UI (Frontend)
    participant API as FastAPI (Backend)
    participant DB as SQLite (Banco)

    G->>UI: Preenche CNPJ, Nome, Tel e clica "Salvar"
    UI->>UI: Valida formato do CNPJ (Regex)
    UI->>API: POST /gerente/fornecedor {cnpj, nome, tel} + JWT
    API->>API: Valida Token JWT (Cargo: Gerente/Admin)
    API->>DB: INSERT INTO Fornecedor (cnpj, nome, tel)
    DB-->>API: Confirmação de INSERT
    API-->>UI: 201 Created {"msg": "Fornecedor cadastrado"}
    UI-->>G: Exibe Alerta Verde
    UI->>API: GET /gerente/fornecedores
    API-->>UI: Retorna Lista Atualizada
    UI->>UI: Renderiza nova linha na Tabela
```

---

## 3. Sequência: Administrador (Controle de Usuários)

Este fluxo detalha a alteração de cargo de um funcionário.

**Fluxo em Mermaid:**
```mermaid
sequenceDiagram
    actor A as Administrador
    participant UI as Flet UI (Frontend)
    participant API as FastAPI (Backend)
    participant DB as SQLite (Banco)

    A->>UI: Clica em "Promover a Gerente" (ID: 5)
    UI->>API: PUT /admin/usuarios/5/tipo {tipo: "gerente"} + JWT
    API->>API: Valida Token JWT (Cargo: Admin)
    API->>DB: SELECT * FROM Usuario WHERE id = 5
    DB-->>API: Retorna Usuário Atual
    API->>DB: UPDATE Usuario SET tipo = 'gerente' WHERE id = 5
    DB-->>API: Confirmação de UPDATE
    API-->>UI: 200 OK {"msg": "Cargo atualizado"}
    UI-->>A: Exibe Alerta Verde
    UI->>API: GET /admin/usuarios
    API-->>UI: Retorna Lista Atualizada
    UI->>UI: Atualiza Tabela de Usuários na tela
```

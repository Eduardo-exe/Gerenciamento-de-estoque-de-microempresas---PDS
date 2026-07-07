# Manual de Uso: Perfil Estoquista

O perfil de **Estoquista** é o perfil fundamental e operacional da aplicação **G-Estoque**. Ele é focado na agilidade e precisão do dia a dia da empresa, permitindo consultar peças e registrar movimentações de entrada e saída no galpão.

---

## 🔐 Acesso ao Sistema

![Tela de Login](../assets/TelaEntrada.jpg)

Na tela inicial do aplicativo, insira suas credenciais:
- **Login Padrão:** `estoquista`
- **Senha Padrão:** `estoque123`

Após o clique no botão **Entrar**, o sistema efetuará a autenticação via token JWT e redirecionará automaticamente para o painel de operações do Estoquista.

---

## 📋 1. Consultar Estoque

![Dashboard do Sistema](../assets/TelaDashboard.jpg)

A primeira aba da interface é a de **Consultar Estoque**. Esta tela exibe em tempo real a listagem completa de todos os produtos cadastrados e armazenados no acervo da microempresa.

- **Atualização Automática:** Ao clicar na aba **Consultar Estoque**, o sistema requisita imediatamente ao backend a lista atualizada com as devidas quantidades em prateleira.
- **Informações Exibidas:**
  - **Código:** Identificador numérico único do produto (SKU/Código interno).
  - **Nome do Produto:** Descrição nominal da peça.
  - **Quantidade:** Saldo físico atualmente disponível para movimentação.

---

## 📥 2. Registrar Entrada de Produtos

A aba **Registrar Entrada** é utilizada quando chegam novas mercadorias de fornecedores ou devoluções, aumentando o saldo do item na prateleira.

### Passo a Passo para Entrada:
1. Clique no botão de navegação **Registrar Entrada** (ícone de seta verde para cima).
2. Preencha os campos obrigatórios:
   - **Código do Produto:** Digite o número identificador (ex: `101`).
   - **Nome do Produto:** Digite exatamente o nome cadastrado para aquela peça (ex: `Teclado USB`).
   - **Quantidade:** Informe quantas unidades estão entrando no estoque (ex: `15`).
3. Clique no botão azul **REGISTRAR ENTRADA**.

> [!IMPORTANT]
> **Trava de Segurança (Dupla Confirmação):** O backend do G-Estoque valida se o **Nome do Produto** informado corresponde rigorosamente ao código preenchido. Se houver divergência, a operação será bloqueada com mensagem de erro, impedindo que uma peça receba entrada no código de outra peça por engano de digitação.

---

## 📤 3. Registrar Saída de Produtos

A aba **Registrar Saida** é acionada ao expedir produtos para vendas, consumo interno ou transferências, reduzindo o saldo no banco de dados.

### Passo a Passo para Saída:
1. Clique no botão de navegação **Registrar Saida** (ícone de seta laranja para baixo).
2. Preencha os dados da movimentação:
   - **Código do Produto:** Digite o identificador da peça.
   - **Nome do Produto:** Digite a descrição da peça.
   - **Quantidade:** Informe quantas unidades estão sendo retiradas.
3. Clique no botão azul **REGISTRAR SAÍDA**.

> [!WARNING]
> **Validação de Saldo Insuficiente:** Além da verificação de compatibilidade do nome, o sistema verifica se há saldo em estoque suficiente para cobrir a saída solicitada. Caso você tente retirar uma quantidade superior ao saldo atual (ex: retirar 50 unidades de um item com saldo 20), o sistema negará a transação, retornando o alerta **"Estoque insuficiente"**.

---

## 🚪 Logout do Sistema

Para encerrar sua sessão com segurança no final de seu turno:
1. Localize o botão de saída **Sair** no canto inferior da barra de navegação lateral.
2. Ao clicar, o sistema invalida os dados locais de sessão (`clear_state()`), limpa os cabeçalhos do cliente HTTP e redireciona para a tela inicial de login.

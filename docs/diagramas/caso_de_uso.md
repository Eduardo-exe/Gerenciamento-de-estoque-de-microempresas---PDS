# Diagramas: Casos de Uso

Este documento apresenta o **Diagrama de Casos de Uso** oficial que modela o comportamento operacional e as interações de cada um dos três perfis de ator do sistema **G-Estoque**: Estoquista, Gerente e Administrador.

---

## 👥 Diagrama Oficial de Casos de Uso

Abaixo, você pode visualizar o diagrama oficial de Casos de Uso do projeto.

<object data="../assets/DigramaDeCasoDeUsoV2.pdf" type="application/pdf" width="100%" height="800px">
  <p>Seu navegador não suporta a visualização de PDFs. <a href="../assets/DigramaDeCasoDeUsoV2.pdf">Clique aqui para baixar o PDF do Diagrama de Casos de Uso.</a></p>
</object>

---

## Detalhamento dos Atores

- **Estoquista:**
  - Consultar Estoque em Tempo Real
  - Registrar Entrada de Itens
  - Registrar Saída de Itens

- **Gerente (Herda funções do Estoquista):**
  - Cadastrar, Editar e Excluir Produtos
  - Cadastrar, Editar e Excluir Fornecedores
  - Emitir Relatório Geral em PDF

- **Administrador (Herda funções do Gerente):**
  - Listar Todos os Usuários
  - Cadastrar Novo Usuário com Hash Bcrypt
  - Promover ou Rebaixar Cargo do Usuário
  - Excluir Conta de Colaborador

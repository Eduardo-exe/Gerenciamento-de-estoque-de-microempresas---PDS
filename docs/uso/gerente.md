# Manual de Uso: Perfil Gerente

O perfil de **Gerente** combina todas as capacidades operacionais do Estoquista com um poderoso conjunto de ferramentas de gestão cadastral e auditoria. É o perfil ideal para encarregados de loja, chefes de almoxarifado e coordenadores de compras.

---

## 🔐 Acesso ao Sistema

Faça login no aplicativo utilizando as credenciais gerenciais:
- **Login Padrão:** `gerente`
- **Senha Padrão:** `gerente123`

---

## 🔁 Herança Operacional: Estoque e Movimentações

O Gerente possui acesso integral às 3 abas iniciais operacionais, funcionando exatamente como o painel do Estoquista:
1. **Consultar Estoque:** Visão em tempo real de itens e quantidades.
2. **Registrar Entrada:** Inserção de saldo de mercadorias com validação de código e nome.
3. **Registrar Saída:** Baixa de estoque com validação de saldo disponível.

---

## 📦 Gestão de Produtos

Na seção gerencial do menu de navegação, a aba **Produtos** permite o controle absoluto do catálogo da empresa.

### 1. Cadastrar Novo Produto
1. Preencha o formulário superior na aba Produtos:
   - **Código:** Digite um número inteiro único que servirá como identificador.
   - **Nome:** Digite a descrição comercial do produto.
   - **Quantidade Inicial:** Digite o saldo inicial para a abertura do cadastro (padrão `0`).
2. Clique no botão verde **+ CADASTRAR**.
3. O produto aparecerá instantaneamente na tabela de itens cadastrados abaixo.

### 2. Editar ou Atualizar Produto
Para agilizar edições sem necessidade de redigitação manual de códigos:
1. Localize o produto na tabela inferior.
2. Clique no ícone de lápis azul (**Editar / Preencher form**) na coluna *Ações*.
3. Os dados do produto preencherão automaticamente o formulário de cadastro acima.
4. Altere o nome ou ajuste a quantidade e clique no botão azul **ATUALIZAR**.

### 3. Excluir Produto
1. Localize o item indesejado ou descontinuado na tabela.
2. Clique no ícone de lixeira vermelha (**Excluir**).
3. O sistema enviará a ordem de remoção e o produto desaparecerá da lista de estoque.

> [!CAUTION]
> **Atenção na Exclusão:** A remoção de um produto apaga permanentemente o seu histórico de estoque atrelado àquela peça.

---

## 🤝 Gestão de Fornecedores

A aba **Fornecedores** gerencia a base de parceiros comerciais da microempresa, garantindo confiabilidade nas compras e contatos rápidos.

### 1. Cadastrar Fornecedor
1. Preencha os campos na aba Fornecedores:
   - **CNPJ:** Digite o Cadastro Nacional de Pessoa Jurídica (apenas números ou formatado, ex: `12.345.678/0001-90`).
   - **Nome:** Razão social ou nome fantasia da empresa parceira.
   - **Telefone:** Telefone comercial ou celular de contato (ex: `(11) 98765-4321`).
2. Clique no botão verde **+ CADASTRAR**.

> [!IMPORTANT]
> **Validação Automática de CNPJ via Regex:** O sistema possui uma validação nativa autocontida via Expressão Regular (Regex) no formato `^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$`. O frontend bloqueia CNPJs fora desse padrão para manter a consistência do banco sem necessitar de consultas lentas a APIs externas de terceiros.

### 2. Editar e Excluir Fornecedores
Assim como na tela de produtos, a tabela de fornecedores conta com os botões rápidos de **Editar** (lápis) para re-injetar os dados no formulário e **Excluir** (lixeira) para remover parceiros desativados.

---

## 📄 Emissão de Relatório em PDF

O Gerente possui a autoridade de gerar documentos oficiais para balanço contábil ou conferência física de estoque.

1. Acesse a aba **Relatório** no menu lateral.
2. Clique no botão vermelho **BAIXAR RELATÓRIO PDF**.
3. O sistema fará a compilação instantânea dos dados no servidor via ReportLab e fará o download de um arquivo devidamente diagramado diretamente na sua pasta padrão de **Downloads** do sistema operacional.
4. O caminho absoluto do arquivo PDF gerado (ex: `C:\Users\SeuUsuario\Downloads\relatorio_estoque_20260706_221500.pdf`) será exibido em verde na tela de confirmação.

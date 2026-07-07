# Gerenciamento-de-estoque-de-microempresas---PDS

# Sistema de Gerenciamento de Estoque

Este projeto consiste em um Sistema de Gerenciamento de Estoque planejado e estruturado com base nos princípios de Engenharia de Software e modelagem UML (Unified Modeling Language). O sistema visa automatizar o fluxo de armazenamento, controle de mercadorias, relacionamento com fornecedores externos e administração de permissões de acesso.

---

## Desenvolvedores do Projeto

* Eduardo Oliveira
* Gabriel Patrick
* Marcelo Almeida
* Thalita Amorim

---

## Modelagem do Sistema

A arquitetura lógica do sistema foi projetada utilizando diagramas UML para alinhar as regras de negócio ao modelo de dados e comportamental da aplicação.

### 1. Diagrama de Casos de Uso
O escopo funcional do sistema é segmentado por níveis hierárquicos de atores, onde cada perfil herda ou estende responsabilidades específicas:

* Estoquista: Responsável pelo fluxo operacional básico do estoque.
    * Fazer login (com verificação de credenciais e tratamento de erro).
    * Registrar entrada e saída de mercadorias.
    * Consultar estoque.
* Gerente: Herda as funções do Estoquista e expande para a gestão cadastral.
    * Atender aos fluxos de atualizar, deletar e cadastrar produtos (com validação integrada de código do produto).
    * Cadastrar, atualizar e deletar fornecedores.
    * Consultar CNPJ de fornecedores (com tratamento para formatos incorretos ou dados inexistentes através de integração externa).
* Administrador: Atua de forma independente no controle de segurança do sistema.
    * Gerenciar acesso de usuários.
    * Validar IDs de usuários.
    * Conceder ou remover privilégios e níveis de acesso no sistema.

### 2. Diagrama de Classes (Arquitetura de Software)
O diagrama de classes adota um padrão baseado em Serviços, separando as entidades de domínio das regras de negócio.

* Camada de Usuários (Herança): A classe base Usuario (nome, id) é herdada por Estoquista, Gerente e Administrador, aplicando polimorfismo e herança estrutural.
* Camada de Domínio (Entidades):
    * Estoque: Controla o agrupamento dos itens (id, atualizarEstoque()).
    * ItemEstoque: Classe associativa que gerencia a quantidade física armazenada.
    * Produto: Contém os atributos fundamentais (codigo, nome) e comportamentos de autovalidação.
    * Fornecedor: Concentra as informações fiscais e de contato (CNPJ, nome, telefone).
* Camada de Serviços (Controladores de Regra de Negócio):
    * ServicoAcesso: Responsável pelas rotinas de segurança (darPermissao, removerPermissao, alterarNivel).
    * ServicoEstoque: Centraliza a lógica de movimentação física (entradaProduto, saidaProduto, consultarQuantidadeProduto).
    * ServicoProduto e ServicoFornecedor: Abstraem as operações de CRUD das entidades.
    * ServicoRelatorio: Responsável por consolidar dados analíticos do inventário.
* Integração Externa:
    * ApiReceitaFederal: Abstração de consumo de API REST externa para validação síncrona de dados cadastrais de fornecedores.

---

## Regras de Negócio e Validações Mapeadas

* Segurança de Acesso: Tentativas de login inválidas acionam o fluxo alternativo "Mostrar erro de login". O Administrador pode revogar ou alterar níveis dinamicamente via ServicoAcesso.
* Consistência de Dados de Produtos: Toda operação de produto exige a execução prévia do método validarCodigo() ou validar Codigo produto. Caso o código seja inexistente ou o formato seja inválido, o sistema impede a persistência.
* Validação Fiscal de Fornecedores: O cadastro de um novo fornecedor dispara uma chamada para a ApiReceitaFederal. O sistema trata exceções para formatos incorretos de CNPJ, empresas fantasmas ou registros recém-criados antes de concluir o vínculo.

---

## Tecnologias Aplicadas

* Linguagem de Programação (Backend): Python
* Banco de Dados: PostgreSQL
* Ferramenta de Modelagem: StarUML
* Linguagem de Modelagem: UML 2.5 (Casos de Uso e Classes)

---

## 📚 Como Rodar a Documentação Localmente

Este projeto utiliza o **MkDocs** com o tema **Material for MkDocs** para gerar uma documentação estática bonita e fácil de navegar. Siga os passos abaixo para visualizá-la no seu navegador:

1. **Ative seu ambiente virtual (se aplicável):**
   ```bash
   # Windows
   .venv\Scripts\activate
   ```

2. **Instale as dependências da documentação:**
   Certifique-se de que o `mkdocs-material` está instalado no seu ambiente.
   ```bash
   pip install mkdocs-material
   ```

3. **Inicie o servidor local do MkDocs:**
   Na raiz do projeto (onde está o arquivo `mkdocs.yml`), execute:
   ```bash
   mkdocs serve
   ```

4. **Acesse no navegador:**
   O terminal exibirá um endereço local, geralmente `http://127.0.0.1:8000/`. Abra esse link no seu navegador para ver a documentação interativa com todos os diagramas e imagens.
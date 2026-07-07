# Manual de Uso: Perfil Administrador

O perfil de **Administrador** é o nível máximo de privilégio na hierarquia do **G-Estoque**. Ele é voltado para os proprietários da empresa e administradores de TI, combinando todas as ferramentas de estoque e cadastros com um exclusivo **Painel de Gestão de Usuários**.

---

## 🔐 Acesso ao Sistema

Efetue login com as credenciais de administrador supremo:
- **Login Padrão:** `admin`
- **Senha Padrão:** `admin123`

---

## 👑 Herança Total de Capacidades

O Administrador possui um painel completo com **8 abas de navegação**, absorvendo todas as funções dos perfis inferiores:
- **Operação de Estoque (Estoquista):** Consultar Estoque, Registrar Entrada, Registrar Saída.
- **Gestão de Acervo e Parceiros (Gerente):** Produtos, Fornecedores e Emissão de Relatório PDF (operando de forma transparente sob o prefixo `/admin/relatorio/pdf`).

---

## 👥 Painel Exclusivo: Gestão de Usuários

![Tela de Gestão de Usuários](../assets/TelaUsuario.jpg)

A aba **Usuários** (com ícone de escudo/admin) é o centro de controle de segurança do sistema, onde você define quem pode entrar no aplicativo e quais cargos essas pessoas terão.

### 1. Visualizar Usuários Cadastrados
A tabela inferior da aba Usuários exibe todos os operadores com acesso ao sistema, contendo:
- **ID:** Identificador interno único da conta.
- **Nome:** Nome completo do colaborador.
- **Login:** Nome de usuário utilizado no momento da autenticação.
- **Tipo (Cargo):** Perfil de privilégio atual (`estoquista`, `gerente` ou `admin`).
- **Status de Atividade:** Indicador de conta ativa no sistema.

### 2. Cadastrar Novo Usuário
Para dar acesso a um novo funcionário na microempresa:
1. No formulário superior de **Cadastrar Usuário**:
   - **Nome Completo:** Digite o nome do colaborador (ex: `Carlos Souza`).
   - **Login de Acesso:** Digite o nome de usuário (ex: `carlos.estoque`).
   - **Senha Incial:** Digite a senha provisória ou definitiva.
   - **Perfil / Cargo:** Selecione no menu suspenso o nível de acesso que ele terá (`estoquista`, `gerente` ou `admin`).
2. Clique no botão verde **+ CADASTRAR USUÁRIO**.
3. O servidor encriptará a senha via Bcrypt com Salt e registrará o colaborador instantaneamente.

### 3. Alterar Cargo / Rebaixar ou Promover
Se um funcionário for promovido (ex: de Estoquista para Gerente) ou precisar alterar suas permissões:
1. Localize a conta do colaborador na tabela inferior.
2. Na coluna *Ações*, utilize o menu suspenso (Dropdown) para selecionar o novo cargo desejado.
3. Ao alterar a opção no dropdown, o sistema dispara um comando `PUT` em tempo real para o backend, atualizando as permissões daquela conta imediatamente sem necessidade de recarregar a tela.

### 4. Excluir Conta de Usuário
Para desligar colaboradores ou remover contas de teste:
1. Localize a conta na tabela.
2. Clique no ícone de lixeira vermelha na coluna *Ações*.
3. Confirme a remoção e o acesso do usuário será revogado em definitivo.

> [!WARNING]
> **Proteção Anti-Autoexclusão:** Como medida fundamental de segurança, o sistema impede que um Administrador exclua a própria conta enquanto estiver logado com ela (`usuario.login == _state["login"]`). Ao tentar clicar na lixeira da sua própria linha, o sistema emitirá o alerta **"Não é possível excluir o usuário logado atualmente"**, evitando o bloqueio acidental do último administrador do sistema.

# Visão Geral do Projeto

Bem-vindo à documentação oficial do **G-Estoque**, o **Sistema de Gerenciamento de Estoque para Microempresas**.

O **G-Estoque** é uma aplicação desktop moderna projetada para simplificar, acelerar e segregar com segurança o controle operacional e gerencial do estoque de microempresas. Desenvolvido com uma arquitetura limpa em camadas, o sistema garante alta performance, usabilidade fluida e controle de acessos granular.

---

## 🚀 Principais Recursos

- **📦 Controle em Tempo Real:** Registro instantâneo de entrada e saída de produtos, com validação de cruzamento entre código e nome da peça para evitar baixas ou incrementos incorretos.
- **👥 Controle de Acesso por Perfil (RBAC):** Separação de rotas, telas e permissões baseada no cargo do usuário logado:
    - **Estoquista:** Focado em movimentação e consulta de estoque.
    - **Gerente:** Herda funções de movimentação e adiciona gestão completa de cadastros (Produtos e Fornecedores) e emissão de relatórios.
    - **Administrador:** Herda todas as funções gerenciais e adiciona o controle total sobre a gestão de usuários e contas do sistema.
- **🔐 Segurança Criptográfica:** Autenticação baseada em **JWT (JSON Web Tokens)** e armazenamento de senhas protegidas com hashing de nível militar (**Bcrypt**).
- **📄 Relatórios PDF Dinâmicos:** Emissão em tempo real de relatórios formatados contendo a situação atual de todo o acervo de estoque e a lista de fornecedores cadastrados, prontos para impressão ou auditoria.

---

## 🛠️ Stack Tecnológica

O sistema foi construído utilizando as melhores e mais modernas ferramentas do ecossistema Python:

| Camada | Tecnologia | Descrição |
| :--- | :--- | :--- |
| **Backend (API)** | [FastAPI](https://fastapi.tiangolo.com/) | Framework web de alta performance para construção de APIs RESTful com documentação interativa automática (Swagger/OpenAPI). |
| **Frontend (UI)** | [Flet](https://flet.dev/) | Framework Python que utiliza o motor do Flutter sob o capô, criando interfaces gráficas nativas e modernas para Desktop sem necessidade de HTML/CSS/JS. |
| **Banco de Dados** | SQLite + SQLAlchemy | Banco de dados relacional embutido de alta velocidade gerenciado por ORM para mapeamento limpo de entidades e modelos. |
| **Relatórios** | ReportLab | Biblioteca especializada na geração programática de arquivos PDF vetoriais de alta resolução. |
| **Segurança** | PyJWT & Bcrypt | Criptografia de tokens de sessão com validade de 8 horas e hashing salgado para proteção das senhas no banco. |

---

## 📚 Como Navegar pela Documentação

Utilize o menu lateral para explorar as seções do manual:

1. **[Instalação](instalacao.md):** Guia passo a passo para configurar o ambiente virtual, instalar dependências e inicializar o banco de dados e servidores.
2. **Como Usar:** Tutoriais práticos divididos por perfil de uso ([Estoquista](uso/estoquista.md), [Gerente](uso/gerente.md) e [Administrador](uso/administrador.md)).
3. **Arquitetura:** Detalhamento técnico da estrutura do [Backend](arquitetura/backend.md), [Frontend](arquitetura/frontend.md) e do [Banco de Dados](arquitetura/banco_de_dados.md).
4. **Diagramas:** Visualização gráfica dos [Casos de Uso](diagramas/caso_de_uso.md) e da [Arquitetura de Classes](diagramas/classe.md) em formato Mermaid.

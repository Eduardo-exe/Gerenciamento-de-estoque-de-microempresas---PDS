# Diagramas: Atividades

Este documento apresenta os **Diagramas de Atividades** referentes aos processos do sistema para os três níveis de acesso.

---

## Diagrama Oficial (PDF)

<object data="../assets/DIAGRAMA DE ATIVIDADE.pdf" type="application/pdf" width="100%" height="800px">
  <p>Seu navegador não suporta a visualização de PDFs. <a href="../assets/DIAGRAMA%20DE%20ATIVIDADE.pdf">Baixar PDF do Diagrama de Atividades</a></p>
</object>

---

## 1. Fluxo de Atividade: Estoquista (Movimentação de Peça)

```mermaid
flowchart TD
    Inicio([Início]) --> Login[Efetuar Login como Estoquista]
    Login --> Aba[Abrir aba Registrar Entrada ou Saída]
    Aba --> Preencher[Preencher Código, Nome e Quantidade]
    Preencher --> Enviar[Clicar no botão Registrar]
    
    Enviar --> ValidarNome{Nome bate com<br>o Código no banco?}
    ValidarNome -- Não --> ErroNome[/Exibir Erro: Peça não confere/] --> Preencher
    
    ValidarNome -- Sim --> TipoMov{É Saída?}
    TipoMov -- Sim --> ValidarSaldo{Saldo em estoque<br>é suficiente?}
    ValidarSaldo -- Não --> ErroSaldo[/Exibir Erro: Estoque insuficiente/] --> Preencher
    ValidarSaldo -- Sim --> Baixa[Executar Baixa no Saldo]
    TipoMov -- Não (Entrada) --> Soma[Incrementar Saldo em Prateleira]
    
    Baixa --> Sucesso[/Exibir Mensagem de Sucesso verde/]
    Soma --> Sucesso
    Sucesso --> Fim([Fim])
```

---

## 2. Fluxo de Atividade: Gerente (Gestão de Fornecedor)

```mermaid
flowchart TD
    Inicio([Início]) --> Login[Efetuar Login como Gerente]
    Login --> Aba[Acessar aba Fornecedores]
    Aba --> Acao{Qual a ação desejada?}
    
    Acao -- Novo Cadastro --> Preencher[Preencher CNPJ, Nome e Telefone]
    Preencher --> ValidarRegex{CNPJ é válido no<br>formato XX.XXX.XXX/XXXX-XX?}
    ValidarRegex -- Não --> ErroRegex[/Alerta vermelho: CNPJ inválido/] --> Preencher
    ValidarRegex -- Sim --> Salvar[Enviar POST para /gerente/fornecedor]
    
    Acao -- Editar --> ClicarLapis[Clicar no Lápis da Tabela]
    ClicarLapis --> FormPreenchido[Formulário carrega dados automaticamente]
    FormPreenchido --> Alterar[Modificar Nome ou Telefone]
    Alterar --> SalvarEdicao[Enviar PUT para /gerente/fornecedor]
    
    Salvar --> AtualizarTabela[Tabela atualizada em tela]
    SalvarEdicao --> AtualizarTabela
    AtualizarTabela --> Fim([Fim])
```

---

## 3. Fluxo de Atividade: Administrador (Exclusão Segura de Usuário)

```mermaid
flowchart TD
    Inicio([Início]) --> Login[Efetuar Login como Admin]
    Login --> Aba[Acessar aba Usuários no Painel]
    Aba --> Selecionar[Localizar usuário na Tabela]
    Selecionar --> ClicarLixeira[Clicar no botão Excluir]
    
    ClicarLixeira --> CheckLogado{A conta selecionada é<br>o próprio usuário logado?}
    CheckLogado -- Sim --> AlertaBloqueio[/Alerta vermelho:<br>Não é possível excluir o usuário logado!/]
    AlertaBloqueio --> Cancelar([Operação Cancelada])
    
    CheckLogado -- Não --> EnviarDelete[Disparar DELETE para /admin/usuarios]
    EnviarDelete --> RemoverBanco[Backend remove o registro]
    RemoverBanco --> Sucesso[/Lista recarregada: Colaborador removido/] --> Fim([Fim])
```

## Context

Projeto novo, sem código existente. Ver proposal.md para motivação (teste do fluxo OpenSpec + cadastro básico de clientes). Stack definida pelo usuário: Flask.

## Goals / Non-Goals

**Goals:**
- Definir uma estrutura simples de aplicação Flask para expor o CRUD de clientes descrito em `specs/cliente/spec.md`.
- Escolher um mecanismo de armazenamento simples, adequado ao caráter de teste do change.

**Non-Goals:**
- Autenticação/autorização de acesso à API.
- Paginação, filtros ou ordenação avançada na listagem.
- Múltiplos endereços/contatos por cliente ou validação de documentos (CPF/CNPJ).

## Decisions

### Armazenamento: SQLite via SQLAlchemy
Usar SQLite (arquivo local) com Flask-SQLAlchemy para persistência dos clientes.
- **Alternativa considerada**: armazenamento em memória (lista/dict em processo). Rejeitada porque os dados se perderiam a cada restart, dificultando testar o CRUD de ponta a ponta.
- **Alternativa considerada**: Postgres/outro banco externo. Rejeitado por adicionar complexidade de infraestrutura desnecessária para um teste de fluxo.

### Estrutura da aplicação: single-file Flask app
Uma única aplicação Flask (`app.py`) com um Blueprint ou rotas diretas para `/clientes`, usando o padrão de fábrica de app (`create_app`) para permitir testes automatizados isolados.
- **Alternativa considerada**: separar em múltiplos módulos (models/routes/services). Rejeitada por ora dado o escopo pequeno (3 campos, 5 endpoints); pode ser revisitado se o escopo crescer.

### Identificador do cliente
Usar `id` inteiro autoincremento como chave primária, retornado na criação e usado nos endpoints `GET/PUT/DELETE /clientes/<id>`.

### Formato de erro
Respostas de erro em JSON no formato `{"error": "<mensagem>"}`, com status HTTP apropriado (400 para dados inválidos, 404 para não encontrado, 409 para conflito de email duplicado).

## Risks / Trade-offs

- [SQLite não é adequado para produção com múltiplos processos concorrentes] → Aceitável pois este change é um teste de fluxo, não um sistema em produção.
- [Validação de formato de email/telefone é simplificada] → Mitigado ao restringir a validação a "não vazio" nesta primeira versão; validação mais rica fica como possível change futuro.

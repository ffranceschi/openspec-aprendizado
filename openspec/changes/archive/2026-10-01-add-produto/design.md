## Context

`app.py` concentra hoje o model `Cliente` e suas cinco rotas dentro de `create_app()`, com Flask + Flask-SQLAlchemy sobre SQLite. Os testes (`test_app.py`) usam `create_app('testing')` com SQLite em memória. O padrão de erros já estabelecido é: 400 para campos ausentes, 404 para não encontrado, 409 para conflito de unicidade, 201 na criação e 204 na remoção. Requisitos em `specs/produto/spec.md`; motivação em `proposal.md`.

## Goals / Non-Goals

**Goals:**
- Espelhar o formato da API de clientes em `/produtos`, de modo que quem consome uma entenda a outra.
- Garantir preço sem erro de ponto flutuante do request até o banco e de volta.

**Non-Goals:**
- Refatorar o código de clientes ou extrair camadas genéricas (CRUD base, serializers).
- Introduzir biblioteca de validação (marshmallow, pydantic) ou migrações (Alembic).

## Decisions

**1. Manter tudo em `app.py` (sem blueprints por enquanto)**
O model `Produto` e as rotas entram em `app.py`, ao lado de `Cliente`, seguindo o padrão atual.
- Alternativa: separar em `clientes.py` / `produtos.py` com blueprints. Melhor organização, mas mexe em código de clientes que não faz parte desta change. Fica como refactor futuro, se um terceiro recurso surgir.

**2. Preço como `Numeric(10, 2)` com `Decimal` no Python**
Coluna `db.Numeric(10, 2, asdecimal=True)`. O valor recebido é convertido com `Decimal(str(valor))` para não herdar o erro binário do float do JSON.
- Alternativa: `Float` — descartado por erro de arredondamento (requisito "Precisão preservada").
- Alternativa: inteiro em centavos — exato, mas muda a semântica para o consumidor da API (enviar 1990 para R$ 19,90). Descartado para manter o contrato intuitivo.
- Nota SQLite: não há tipo decimal nativo; o SQLAlchemy emite um aviso e armazena como REAL/NUMERIC. Com no máximo duas casas e conversão via `str`, o round-trip é estável para os valores do escopo. Ao migrar para Postgres, o tipo passa a ser exato nativamente.

**3. Formato do preço no JSON: número**
Entrada aceita número JSON (`19.9`, `19.90`, `0`). Também é aceito string numérica (`"19.90"`), porque `Decimal(str(...))` trata ambos. A saída é número JSON (`float(decimal)`), ex.: `19.9`.
- Alternativa: retornar string `"19.90"` (exata e com casas fixas). Mais correta para dinheiro, mas destoa do resto da API. Pode ser revisto se surgirem consumidores sensíveis a isso.

**4. Regras de validação de preço**
Inválido (400) se: não convertível para `Decimal`, `bool` (em Python `True` é `int`, deve ser recusado explicitamente), `NaN`/`Infinity`, menor que zero, ou com expoente < -2 (mais de duas casas decimais). A validação fica numa função auxiliar usada por POST e PUT.

**5. Unicidade de SKU no banco e na aplicação**
`sku` com `unique=True` na coluna (proteção final) e checagem prévia com `filter_by(sku=...)` para retornar 409 com mensagem clara, igual ao fluxo de email em clientes. No PUT, só checa se o SKU mudou.

**6. Mensagens de erro**
Mesmo formato `{'error': '...'}` e em inglês, como em clientes: `Missing required fields: nome, sku, preco`, `Invalid preco`, `SKU already exists`, `Produto not found`.

## Risks / Trade-offs

- [Aviso do SQLAlchemy sobre Decimal no SQLite] → Aceitável em estudo; documentado. Em produção, usar Postgres.
- [Corrida entre checagem de SKU e insert] → A constraint `unique` do banco impede duplicidade; um `IntegrityError` raro resultaria em 500. Aceitável no escopo; pode ser tratado com try/except em evolução futura.
- [Saída do preço como float pode exibir `19.9` em vez de `19.90`] → Valor numérico é o mesmo; formatação fica a cargo do cliente da API.
- [Remoção física] → Se pedidos forem introduzidos, será necessário rever para remoção lógica (ver proposal, fora de escopo).

## Migration Plan

Sem migração: `db.create_all()` cria a tabela `produtos` na próxima subida da aplicação; a tabela `clientes` não é alterada. Rollback = reverter o código; a tabela órfã pode ser removida manualmente se desejado.

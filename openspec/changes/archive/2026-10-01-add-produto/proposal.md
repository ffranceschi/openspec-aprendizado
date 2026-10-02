## Why

O sistema hoje só cadastra clientes. Para evoluir rumo a vendas/pedidos, é preciso primeiro ter um cadastro central de produtos, com identificação única (SKU) e preço confiável, seguindo o mesmo padrão de API já usado em clientes.

## What Changes

- Novo recurso REST `/produtos` com operações de criar, listar, consultar por id, atualizar e remover (mesmo formato de `/clientes`).
- Produto possui: `nome` (obrigatório), `sku` (obrigatório, único), `preco` (obrigatório, decimal com 2 casas, ≥ 0) e `descricao` (opcional).
- SKU duplicado na criação ou atualização é rejeitado com erro de conflito.
- Preço ausente, não numérico ou negativo é rejeitado com erro de validação.
- Remoção é física (o produto deixa de existir), igual a clientes.
- Fora de escopo nesta change: controle de estoque, categorias, imagens, remoção lógica (ativo/inativo), relação com pedidos.

## Capabilities

### New Capabilities
- `produto`: cadastro de produtos — criação, listagem, consulta, atualização e remoção, com unicidade de SKU e validação de preço.

### Modified Capabilities
<!-- Nenhuma: o comportamento de `cliente` não muda. -->

## Impact

- `app.py`: novo model `Produto` (tabela `produtos`) e cinco novas rotas em `/produtos`.
- `test_app.py`: novos testes cobrindo os cenários da spec de produto.
- Banco SQLite: nova tabela criada via `db.create_all()`; sem migração de dados existentes.
- Sem novas dependências.

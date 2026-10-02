## 1. Model

- [x] 1.1 Adicionar model `Produto` em `app.py` (tabela `produtos`: `id`, `nome` obrigatório, `sku` obrigatório e único, `preco` `Numeric(10,2)`, `descricao` opcional) com `to_dict()` retornando `preco` como número; verificar que `create_app('testing')` cria a tabela sem erro
- [x] 1.2 Exportar `Produto` para uso nos testes (`from app import Produto`) e confirmar que a suíte existente de clientes continua passando com `pytest`

## 2. Validação

- [x] 2.1 Criar função auxiliar de validação de preço (rejeita bool, não numérico, NaN/Infinity, negativo, mais de 2 casas; converte via `Decimal(str(v))`) e verificar com testes cobrindo cada caso do requisito "Validação de Preço"

## 3. Rotas

- [x] 3.1 Implementar `POST /produtos` (400 campos ausentes, 400 preço inválido, 409 SKU duplicado, 201 sucesso) e verificar com testes dos cenários de "Criação de Produto"
- [x] 3.2 Implementar `GET /produtos` e verificar com testes de listagem com e sem produtos
- [x] 3.3 Implementar `GET /produtos/<id>` e verificar com testes de produto encontrado e 404
- [x] 3.4 Implementar `PUT /produtos/<id>` (404, 400, 409 só se o SKU mudou, 200) e verificar com testes dos cenários de "Atualização de Produto", incluindo manter o próprio SKU
- [x] 3.5 Implementar `DELETE /produtos/<id>` (204, 404) e verificar com testes de remoção e posterior 404 na consulta

## 4. Verificação final

- [x] 4.1 Teste de round-trip de precisão: criar com `19.90` e confirmar que GET retorna `19.9` exato (sem `19.899999...`)
- [x] 4.2 Rodar `pytest` completo e confirmar todos os testes (clientes e produtos) verdes
- [x] 4.3 Rodar `openspec validate add-produto --strict` e confirmar que passa

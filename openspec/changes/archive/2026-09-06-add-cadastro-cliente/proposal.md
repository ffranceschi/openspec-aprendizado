## Why

Não existe hoje nenhuma forma de registrar e gerenciar clientes no sistema. Este change adiciona o cadastro básico de clientes como ponto de partida (e como teste do fluxo OpenSpec), permitindo criar, consultar, atualizar e remover registros de clientes via API.

## What Changes

- Adiciona uma API REST em Flask para gerenciar clientes.
- Novo endpoint `POST /clientes` para criar um cliente (nome, email, telefone).
- Novo endpoint `GET /clientes` para listar clientes.
- Novo endpoint `GET /clientes/<id>` para consultar um cliente específico.
- Novo endpoint `PUT /clientes/<id>` para atualizar um cliente.
- Novo endpoint `DELETE /clientes/<id>` para remover um cliente.

## Capabilities

### New Capabilities
- `cliente`: cadastro (CRUD) de clientes — criação, consulta, atualização e remoção de registros com nome, email e telefone.

### Modified Capabilities
(nenhuma — este é o primeiro capability do projeto)

## Impact

- Novo serviço Flask (código de aplicação, a ser definido em design.md).
- Novo armazenamento de dados para clientes (mecanismo a definir em design.md).
- Nenhum sistema existente é afetado, pois o projeto está vazio.

## Purpose

Permite criar, consultar, atualizar e remover registros de clientes, servindo como cadastro central de clientes do sistema.

## ADDED Requirements

### Requirement: Criação de Cliente
O sistema SHALL permitir a criação de um cliente informando nome, email e telefone.

#### Scenario: Criação bem-sucedida
- **WHEN** um cliente é criado com nome, email e telefone válidos
- **THEN** o sistema armazena o cliente e retorna seus dados com um identificador único

#### Scenario: Campo obrigatório ausente
- **WHEN** a criação de um cliente é solicitada sem nome, email ou telefone
- **THEN** o sistema rejeita a solicitação com um erro indicando o campo ausente

#### Scenario: Email duplicado
- **WHEN** a criação de um cliente é solicitada com um email já cadastrado em outro cliente
- **THEN** o sistema rejeita a solicitação com um erro de conflito

### Requirement: Listagem de Clientes
O sistema SHALL permitir a listagem de todos os clientes cadastrados.

#### Scenario: Listagem com clientes existentes
- **WHEN** existem clientes cadastrados
- **THEN** o sistema retorna a lista de clientes com nome, email e telefone de cada um

#### Scenario: Listagem sem clientes
- **WHEN** não existem clientes cadastrados
- **THEN** o sistema retorna uma lista vazia

### Requirement: Consulta de Cliente por Identificador
O sistema SHALL permitir a consulta de um cliente específico pelo seu identificador.

#### Scenario: Cliente encontrado
- **WHEN** a consulta é feita com o identificador de um cliente existente
- **THEN** o sistema retorna os dados do cliente

#### Scenario: Cliente não encontrado
- **WHEN** a consulta é feita com um identificador que não corresponde a nenhum cliente
- **THEN** o sistema retorna um erro indicando que o cliente não foi encontrado

### Requirement: Atualização de Cliente
O sistema SHALL permitir a atualização do nome, email e telefone de um cliente existente.

#### Scenario: Atualização bem-sucedida
- **WHEN** a atualização é feita com dados válidos para um cliente existente
- **THEN** o sistema salva as alterações e retorna os dados atualizados do cliente

#### Scenario: Atualização de cliente inexistente
- **WHEN** a atualização é solicitada para um identificador que não corresponde a nenhum cliente
- **THEN** o sistema retorna um erro indicando que o cliente não foi encontrado

#### Scenario: Atualização com email duplicado
- **WHEN** a atualização altera o email para um valor já usado por outro cliente
- **THEN** o sistema rejeita a solicitação com um erro de conflito

### Requirement: Remoção de Cliente
O sistema SHALL permitir a remoção de um cliente existente pelo seu identificador.

#### Scenario: Remoção bem-sucedida
- **WHEN** a remoção é solicitada para um identificador de cliente existente
- **THEN** o sistema remove o cliente e ele deixa de aparecer em consultas e listagens

#### Scenario: Remoção de cliente inexistente
- **WHEN** a remoção é solicitada para um identificador que não corresponde a nenhum cliente
- **THEN** o sistema retorna um erro indicando que o cliente não foi encontrado

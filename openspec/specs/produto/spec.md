# produto Specification

## Purpose

Permite criar, consultar, atualizar e remover registros de produtos, servindo como cadastro central de produtos do sistema, com identificação única por SKU e preço com precisão monetária.

## Requirements

### Requirement: Criação de Produto
O sistema SHALL permitir a criação de um produto informando nome, SKU e preço, e opcionalmente uma descrição.

#### Scenario: Criação bem-sucedida
- **WHEN** um produto é criado com nome, SKU e preço válidos
- **THEN** o sistema armazena o produto e retorna seus dados (nome, SKU, preço e descrição) com um identificador único

#### Scenario: Criação sem descrição
- **WHEN** um produto é criado com nome, SKU e preço válidos e sem descrição
- **THEN** o sistema armazena o produto e retorna a descrição como vazia (nula)

#### Scenario: Campo obrigatório ausente
- **WHEN** a criação de um produto é solicitada sem nome, SKU ou preço
- **THEN** o sistema rejeita a solicitação com um erro indicando o campo ausente

#### Scenario: SKU duplicado
- **WHEN** a criação de um produto é solicitada com um SKU já cadastrado em outro produto
- **THEN** o sistema rejeita a solicitação com um erro de conflito

### Requirement: Validação de Preço
O sistema SHALL aceitar apenas preços numéricos, maiores ou iguais a zero e com no máximo duas casas decimais, e SHALL armazenar e retornar o preço sem perda de precisão.

#### Scenario: Preço negativo
- **WHEN** a criação ou atualização de um produto é solicitada com preço menor que zero
- **THEN** o sistema rejeita a solicitação com um erro de validação indicando o preço inválido

#### Scenario: Preço não numérico
- **WHEN** a criação ou atualização de um produto é solicitada com preço que não é um número
- **THEN** o sistema rejeita a solicitação com um erro de validação indicando o preço inválido

#### Scenario: Preço com mais de duas casas decimais
- **WHEN** a criação ou atualização de um produto é solicitada com preço com mais de duas casas decimais (ex.: 10.999)
- **THEN** o sistema rejeita a solicitação com um erro de validação indicando o preço inválido

#### Scenario: Preço zero
- **WHEN** um produto é criado com preço igual a zero e demais dados válidos
- **THEN** o sistema aceita e armazena o produto

#### Scenario: Precisão preservada
- **WHEN** um produto é criado com preço 19.90
- **THEN** consultas posteriores retornam o preço exatamente como 19.90, sem erro de arredondamento

### Requirement: Listagem de Produtos
O sistema SHALL permitir a listagem de todos os produtos cadastrados.

#### Scenario: Listagem com produtos existentes
- **WHEN** existem produtos cadastrados
- **THEN** o sistema retorna a lista de produtos com nome, SKU, preço e descrição de cada um

#### Scenario: Listagem sem produtos
- **WHEN** não existem produtos cadastrados
- **THEN** o sistema retorna uma lista vazia

### Requirement: Consulta de Produto por Identificador
O sistema SHALL permitir a consulta de um produto específico pelo seu identificador.

#### Scenario: Produto encontrado
- **WHEN** a consulta é feita com o identificador de um produto existente
- **THEN** o sistema retorna os dados do produto

#### Scenario: Produto não encontrado
- **WHEN** a consulta é feita com um identificador que não corresponde a nenhum produto
- **THEN** o sistema retorna um erro indicando que o produto não foi encontrado

### Requirement: Atualização de Produto
O sistema SHALL permitir a atualização do nome, SKU, preço e descrição de um produto existente, aplicando as mesmas validações da criação.

#### Scenario: Atualização bem-sucedida
- **WHEN** a atualização é feita com dados válidos para um produto existente
- **THEN** o sistema salva as alterações e retorna os dados atualizados do produto

#### Scenario: Atualização com campo obrigatório ausente
- **WHEN** a atualização é solicitada sem nome, SKU ou preço
- **THEN** o sistema rejeita a solicitação com um erro indicando o campo ausente

#### Scenario: Atualização de produto inexistente
- **WHEN** a atualização é solicitada para um identificador que não corresponde a nenhum produto
- **THEN** o sistema retorna um erro indicando que o produto não foi encontrado

#### Scenario: Atualização com SKU duplicado
- **WHEN** a atualização altera o SKU para um valor já usado por outro produto
- **THEN** o sistema rejeita a solicitação com um erro de conflito

#### Scenario: Atualização mantendo o próprio SKU
- **WHEN** a atualização é feita mantendo o mesmo SKU do produto
- **THEN** o sistema aceita a atualização sem acusar conflito

### Requirement: Remoção de Produto
O sistema SHALL permitir a remoção de um produto existente pelo seu identificador.

#### Scenario: Remoção bem-sucedida
- **WHEN** a remoção é solicitada para um identificador de produto existente
- **THEN** o sistema remove o produto e ele deixa de aparecer em consultas e listagens

#### Scenario: Remoção de produto inexistente
- **WHEN** a remoção é solicitada para um identificador que não corresponde a nenhum produto
- **THEN** o sistema retorna um erro indicando que o produto não foi encontrado

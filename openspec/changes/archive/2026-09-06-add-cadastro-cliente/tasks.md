## 1. Setup do projeto

- [x] 1.1 Criar estrutura do projeto Flask (`app.py`, `requirements.txt` com Flask e Flask-SQLAlchemy) e verificar que `flask run` inicia sem erros
- [x] 1.2 Configurar SQLite via Flask-SQLAlchemy (`create_app` factory, conexão ao arquivo local) e verificar que o app conecta ao banco sem erros na inicialização

## 2. Modelo de dados

- [x] 2.1 Criar o modelo `Cliente` (id, nome, email único, telefone) e verificar que a tabela é criada no banco (`db.create_all()` ou migração)

## 3. Endpoints CRUD

- [x] 3.1 Implementar `POST /clientes` com validação de campos obrigatórios e checagem de email duplicado, e verificar com teste cobrindo criação bem-sucedida, campo ausente (400) e email duplicado (409)
- [x] 3.2 Implementar `GET /clientes` e verificar com teste cobrindo lista vazia e lista com clientes cadastrados
- [x] 3.3 Implementar `GET /clientes/<id>` e verificar com teste cobrindo cliente encontrado e não encontrado (404)
- [x] 3.4 Implementar `PUT /clientes/<id>` com validação de campos e checagem de email duplicado, e verificar com teste cobrindo atualização bem-sucedida, cliente inexistente (404) e email duplicado (409)
- [x] 3.5 Implementar `DELETE /clientes/<id>` e verificar com teste cobrindo remoção bem-sucedida e cliente inexistente (404)

## 4. Verificação end-to-end

- [x] 4.1 Rodar a suíte de testes completa e confirmar que todos os cenários de `specs/cliente/spec.md` estão cobertos e passando

import pytest
from app import create_app, db, Cliente, Produto, parse_preco


@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


class TestCreateCliente:
    def test_create_cliente_success(self, client):
        response = client.post('/clientes', json={
            'nome': 'John Doe',
            'email': 'john@example.com',
            'telefone': '123456789'
        })
        assert response.status_code == 201
        data = response.get_json()
        assert data['nome'] == 'John Doe'
        assert data['email'] == 'john@example.com'
        assert data['telefone'] == '123456789'
        assert 'id' in data

    def test_create_cliente_missing_field(self, client):
        response = client.post('/clientes', json={
            'nome': 'John Doe',
            'email': 'john@example.com'
        })
        assert response.status_code == 400
        assert 'Missing required fields' in response.get_json()['error']

    def test_create_cliente_duplicate_email(self, client):
        client.post('/clientes', json={
            'nome': 'John Doe',
            'email': 'john@example.com',
            'telefone': '123456789'
        })
        response = client.post('/clientes', json={
            'nome': 'Jane Doe',
            'email': 'john@example.com',
            'telefone': '987654321'
        })
        assert response.status_code == 409
        assert 'Email already exists' in response.get_json()['error']


class TestListClientes:
    def test_list_clientes_empty(self, client):
        response = client.get('/clientes')
        assert response.status_code == 200
        assert response.get_json() == []

    def test_list_clientes_with_data(self, client):
        client.post('/clientes', json={
            'nome': 'John Doe',
            'email': 'john@example.com',
            'telefone': '123456789'
        })
        client.post('/clientes', json={
            'nome': 'Jane Doe',
            'email': 'jane@example.com',
            'telefone': '987654321'
        })
        response = client.get('/clientes')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 2
        assert data[0]['nome'] == 'John Doe'
        assert data[1]['nome'] == 'Jane Doe'


class TestGetCliente:
    def test_get_cliente_found(self, client):
        create_response = client.post('/clientes', json={
            'nome': 'John Doe',
            'email': 'john@example.com',
            'telefone': '123456789'
        })
        cliente_id = create_response.get_json()['id']

        response = client.get(f'/clientes/{cliente_id}')
        assert response.status_code == 200
        data = response.get_json()
        assert data['nome'] == 'John Doe'
        assert data['email'] == 'john@example.com'

    def test_get_cliente_not_found(self, client):
        response = client.get('/clientes/999')
        assert response.status_code == 404
        assert 'Cliente not found' in response.get_json()['error']


class TestUpdateCliente:
    def test_update_cliente_success(self, client):
        create_response = client.post('/clientes', json={
            'nome': 'John Doe',
            'email': 'john@example.com',
            'telefone': '123456789'
        })
        cliente_id = create_response.get_json()['id']

        response = client.put(f'/clientes/{cliente_id}', json={
            'nome': 'Jane Doe',
            'email': 'jane@example.com',
            'telefone': '987654321'
        })
        assert response.status_code == 200
        data = response.get_json()
        assert data['nome'] == 'Jane Doe'
        assert data['email'] == 'jane@example.com'

    def test_update_cliente_not_found(self, client):
        response = client.put('/clientes/999', json={
            'nome': 'Jane Doe',
            'email': 'jane@example.com',
            'telefone': '987654321'
        })
        assert response.status_code == 404
        assert 'Cliente not found' in response.get_json()['error']

    def test_update_cliente_duplicate_email(self, client):
        client.post('/clientes', json={
            'nome': 'John Doe',
            'email': 'john@example.com',
            'telefone': '123456789'
        })
        create_response = client.post('/clientes', json={
            'nome': 'Jane Doe',
            'email': 'jane@example.com',
            'telefone': '987654321'
        })
        cliente_id = create_response.get_json()['id']

        response = client.put(f'/clientes/{cliente_id}', json={
            'nome': 'Jane Doe',
            'email': 'john@example.com',
            'telefone': '987654321'
        })
        assert response.status_code == 409
        assert 'Email already exists' in response.get_json()['error']


class TestDeleteCliente:
    def test_delete_cliente_success(self, client):
        create_response = client.post('/clientes', json={
            'nome': 'John Doe',
            'email': 'john@example.com',
            'telefone': '123456789'
        })
        cliente_id = create_response.get_json()['id']

        response = client.delete(f'/clientes/{cliente_id}')
        assert response.status_code == 204

        # Verify cliente is deleted
        get_response = client.get(f'/clientes/{cliente_id}')
        assert get_response.status_code == 404

    def test_delete_cliente_not_found(self, client):
        response = client.delete('/clientes/999')
        assert response.status_code == 404
        assert 'Cliente not found' in response.get_json()['error']


PRODUTO = {
    'nome': 'Caneta',
    'sku': 'CAN-001',
    'preco': 19.90,
    'descricao': 'Caneta azul'
}


def make_produto(**overrides):
    return {**PRODUTO, **overrides}


class TestParsePreco:
    @pytest.mark.parametrize('value', [0, 10, 19.9, 19.90, '19.90', '0.01'])
    def test_valid(self, value):
        assert parse_preco(value) is not None

    @pytest.mark.parametrize('value', [
        -1, -0.01, 'abc', 10.999, '1.001', True, False,
        'NaN', 'Infinity', None, [], {}
    ])
    def test_invalid(self, value):
        assert parse_preco(value) is None


class TestCreateProduto:
    def test_create_produto_success(self, client):
        response = client.post('/produtos', json=PRODUTO)
        assert response.status_code == 201
        data = response.get_json()
        assert data['nome'] == 'Caneta'
        assert data['sku'] == 'CAN-001'
        assert data['preco'] == 19.9
        assert data['descricao'] == 'Caneta azul'
        assert 'id' in data

    def test_create_produto_without_descricao(self, client):
        payload = make_produto()
        del payload['descricao']
        response = client.post('/produtos', json=payload)
        assert response.status_code == 201
        assert response.get_json()['descricao'] is None

    @pytest.mark.parametrize('campo', ['nome', 'sku', 'preco'])
    def test_create_produto_missing_field(self, client, campo):
        payload = make_produto()
        del payload[campo]
        response = client.post('/produtos', json=payload)
        assert response.status_code == 400
        assert 'Missing required fields' in response.get_json()['error']

    def test_create_produto_duplicate_sku(self, client):
        client.post('/produtos', json=PRODUTO)
        response = client.post('/produtos', json=make_produto(nome='Outra'))
        assert response.status_code == 409
        assert 'SKU already exists' in response.get_json()['error']

    @pytest.mark.parametrize('preco', [-1, 'abc', 10.999, True])
    def test_create_produto_invalid_preco(self, client, preco):
        response = client.post('/produtos', json=make_produto(preco=preco))
        assert response.status_code == 400
        assert 'Invalid preco' in response.get_json()['error']

    def test_create_produto_preco_zero(self, client):
        response = client.post('/produtos', json=make_produto(preco=0))
        assert response.status_code == 201
        assert response.get_json()['preco'] == 0


class TestListProdutos:
    def test_list_produtos_empty(self, client):
        response = client.get('/produtos')
        assert response.status_code == 200
        assert response.get_json() == []

    def test_list_produtos_with_data(self, client):
        client.post('/produtos', json=PRODUTO)
        client.post('/produtos', json=make_produto(nome='Lápis', sku='LAP-001', preco=2.5))
        response = client.get('/produtos')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 2
        assert data[0]['sku'] == 'CAN-001'
        assert data[1]['sku'] == 'LAP-001'
        assert data[1]['preco'] == 2.5


class TestGetProduto:
    def test_get_produto_found(self, client):
        produto_id = client.post('/produtos', json=PRODUTO).get_json()['id']
        response = client.get(f'/produtos/{produto_id}')
        assert response.status_code == 200
        data = response.get_json()
        assert data['nome'] == 'Caneta'
        assert data['sku'] == 'CAN-001'

    def test_get_produto_not_found(self, client):
        response = client.get('/produtos/999')
        assert response.status_code == 404
        assert 'Produto not found' in response.get_json()['error']

    def test_preco_round_trip(self, client):
        produto_id = client.post('/produtos', json=make_produto(preco=19.90)).get_json()['id']
        response = client.get(f'/produtos/{produto_id}')
        assert response.get_json()['preco'] == 19.9
        assert '19.9' in response.get_data(as_text=True)
        assert '19.89' not in response.get_data(as_text=True)


class TestUpdateProduto:
    def test_update_produto_success(self, client):
        produto_id = client.post('/produtos', json=PRODUTO).get_json()['id']
        response = client.put(f'/produtos/{produto_id}', json=make_produto(
            nome='Caneta Vermelha', sku='CAN-002', preco=21.5, descricao=None
        ))
        assert response.status_code == 200
        data = response.get_json()
        assert data['nome'] == 'Caneta Vermelha'
        assert data['sku'] == 'CAN-002'
        assert data['preco'] == 21.5
        assert data['descricao'] is None

    def test_update_produto_keeps_own_sku(self, client):
        produto_id = client.post('/produtos', json=PRODUTO).get_json()['id']
        response = client.put(f'/produtos/{produto_id}', json=make_produto(nome='Novo nome'))
        assert response.status_code == 200
        assert response.get_json()['nome'] == 'Novo nome'

    def test_update_produto_missing_field(self, client):
        produto_id = client.post('/produtos', json=PRODUTO).get_json()['id']
        payload = make_produto()
        del payload['preco']
        response = client.put(f'/produtos/{produto_id}', json=payload)
        assert response.status_code == 400
        assert 'Missing required fields' in response.get_json()['error']

    def test_update_produto_invalid_preco(self, client):
        produto_id = client.post('/produtos', json=PRODUTO).get_json()['id']
        response = client.put(f'/produtos/{produto_id}', json=make_produto(preco=-5))
        assert response.status_code == 400
        assert 'Invalid preco' in response.get_json()['error']

    def test_update_produto_not_found(self, client):
        response = client.put('/produtos/999', json=PRODUTO)
        assert response.status_code == 404
        assert 'Produto not found' in response.get_json()['error']

    def test_update_produto_duplicate_sku(self, client):
        client.post('/produtos', json=PRODUTO)
        produto_id = client.post('/produtos', json=make_produto(sku='LAP-001')).get_json()['id']
        response = client.put(f'/produtos/{produto_id}', json=make_produto(sku='CAN-001'))
        assert response.status_code == 409
        assert 'SKU already exists' in response.get_json()['error']


class TestDeleteProduto:
    def test_delete_produto_success(self, client):
        produto_id = client.post('/produtos', json=PRODUTO).get_json()['id']
        response = client.delete(f'/produtos/{produto_id}')
        assert response.status_code == 204
        assert client.get(f'/produtos/{produto_id}').status_code == 404
        assert client.get('/produtos').get_json() == []

    def test_delete_produto_not_found(self, client):
        response = client.delete('/produtos/999')
        assert response.status_code == 404
        assert 'Produto not found' in response.get_json()['error']

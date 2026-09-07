import pytest
from app import create_app, db, Cliente


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

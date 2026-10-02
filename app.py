from decimal import Decimal, InvalidOperation

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Cliente(db.Model):
    __tablename__ = 'clientes'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    telefone = db.Column(db.String(20), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'telefone': self.telefone
        }


class Produto(db.Model):
    __tablename__ = 'produtos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    sku = db.Column(db.String(64), unique=True, nullable=False)
    preco = db.Column(db.Numeric(10, 2, asdecimal=True), nullable=False)
    descricao = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'sku': self.sku,
            'preco': float(self.preco),
            'descricao': self.descricao
        }


def parse_preco(value):
    """Return value as Decimal, or None if it is not a valid price."""
    # bool is a subclass of int, so it must be rejected explicitly
    if isinstance(value, bool) or not isinstance(value, (int, float, str)):
        return None
    try:
        preco = Decimal(str(value))
    except InvalidOperation:
        return None
    if not preco.is_finite() or preco < 0 or preco.as_tuple().exponent < -2:
        return None
    return preco


def create_app(config_name='development'):
    app = Flask(__name__)

    if config_name == 'testing':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clientes.db'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route('/clientes', methods=['POST'])
    def create_cliente():
        data = request.get_json()

        # Validate required fields
        if not data or not all(k in data for k in ['nome', 'email', 'telefone']):
            return jsonify({'error': 'Missing required fields: nome, email, telefone'}), 400

        # Check for duplicate email
        existing = Cliente.query.filter_by(email=data['email']).first()
        if existing:
            return jsonify({'error': 'Email already exists'}), 409

        cliente = Cliente(
            nome=data['nome'],
            email=data['email'],
            telefone=data['telefone']
        )
        db.session.add(cliente)
        db.session.commit()

        return jsonify(cliente.to_dict()), 201

    @app.route('/clientes', methods=['GET'])
    def list_clientes():
        clientes = Cliente.query.all()
        return jsonify([c.to_dict() for c in clientes]), 200

    @app.route('/clientes/<int:id>', methods=['GET'])
    def get_cliente(id):
        cliente = Cliente.query.get(id)
        if not cliente:
            return jsonify({'error': 'Cliente not found'}), 404
        return jsonify(cliente.to_dict()), 200

    @app.route('/clientes/<int:id>', methods=['PUT'])
    def update_cliente(id):
        cliente = Cliente.query.get(id)
        if not cliente:
            return jsonify({'error': 'Cliente not found'}), 404

        data = request.get_json()

        # Validate required fields
        if not data or not all(k in data for k in ['nome', 'email', 'telefone']):
            return jsonify({'error': 'Missing required fields: nome, email, telefone'}), 400

        # Check for duplicate email (if changing email)
        if data['email'] != cliente.email:
            existing = Cliente.query.filter_by(email=data['email']).first()
            if existing:
                return jsonify({'error': 'Email already exists'}), 409

        cliente.nome = data['nome']
        cliente.email = data['email']
        cliente.telefone = data['telefone']
        db.session.commit()

        return jsonify(cliente.to_dict()), 200

    @app.route('/clientes/<int:id>', methods=['DELETE'])
    def delete_cliente(id):
        cliente = Cliente.query.get(id)
        if not cliente:
            return jsonify({'error': 'Cliente not found'}), 404

        db.session.delete(cliente)
        db.session.commit()

        return '', 204

    @app.route('/produtos', methods=['POST'])
    def create_produto():
        data = request.get_json()

        # Validate required fields
        if not data or any(data.get(k) is None for k in ['nome', 'sku', 'preco']):
            return jsonify({'error': 'Missing required fields: nome, sku, preco'}), 400

        preco = parse_preco(data['preco'])
        if preco is None:
            return jsonify({'error': 'Invalid preco'}), 400

        # Check for duplicate SKU
        existing = Produto.query.filter_by(sku=data['sku']).first()
        if existing:
            return jsonify({'error': 'SKU already exists'}), 409

        produto = Produto(
            nome=data['nome'],
            sku=data['sku'],
            preco=preco,
            descricao=data.get('descricao')
        )
        db.session.add(produto)
        db.session.commit()

        return jsonify(produto.to_dict()), 201

    @app.route('/produtos', methods=['GET'])
    def list_produtos():
        produtos = Produto.query.all()
        return jsonify([p.to_dict() for p in produtos]), 200

    @app.route('/produtos/<int:id>', methods=['GET'])
    def get_produto(id):
        produto = db.session.get(Produto, id)
        if not produto:
            return jsonify({'error': 'Produto not found'}), 404
        return jsonify(produto.to_dict()), 200

    @app.route('/produtos/<int:id>', methods=['PUT'])
    def update_produto(id):
        produto = db.session.get(Produto, id)
        if not produto:
            return jsonify({'error': 'Produto not found'}), 404

        data = request.get_json()

        # Validate required fields
        if not data or any(data.get(k) is None for k in ['nome', 'sku', 'preco']):
            return jsonify({'error': 'Missing required fields: nome, sku, preco'}), 400

        preco = parse_preco(data['preco'])
        if preco is None:
            return jsonify({'error': 'Invalid preco'}), 400

        # Check for duplicate SKU (if changing SKU)
        if data['sku'] != produto.sku:
            existing = Produto.query.filter_by(sku=data['sku']).first()
            if existing:
                return jsonify({'error': 'SKU already exists'}), 409

        produto.nome = data['nome']
        produto.sku = data['sku']
        produto.preco = preco
        produto.descricao = data.get('descricao')
        db.session.commit()

        return jsonify(produto.to_dict()), 200

    @app.route('/produtos/<int:id>', methods=['DELETE'])
    def delete_produto(id):
        produto = db.session.get(Produto, id)
        if not produto:
            return jsonify({'error': 'Produto not found'}), 404

        db.session.delete(produto)
        db.session.commit()

        return '', 204

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

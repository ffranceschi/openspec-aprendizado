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

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

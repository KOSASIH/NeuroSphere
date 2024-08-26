import os
import logging
from flask import Flask, request, jsonify
from flask_restplus import Api, Resource, fields
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from node_module import NodeModule

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
api = Api(app, version='1.0', title='Node API', description='Advanced Node API')

# Define API namespace
ns = api.namespace('node', description='Node operations')

# Define Node model
node_model = api.model('Node', {
    'id': fields.Integer(readOnly=True, description='The node ID'),
    'name': fields.String(required=True, description='The node name'),
    'description': fields.String(description='The node description'),
    'ip_address': fields.String(required=True, description='The node IP address'),
    'port': fields.Integer(required=True, description='The node port')
})

# Define NodeModule instance
node_module = NodeModule()

# Define API endpoints
@ns.route('/')
class NodeList(Resource):
    @jwt_required
    def get(self):
        nodes = node_module.get_nodes()
        return {'nodes': [node.to_dict() for node in nodes]}

    @jwt_required
    def post(self):
        data = request.get_json()
        node = node_module.create_node(data['name'], data['description'], data['ip_address'], data['port'])
        return {'node': node.to_dict()}, 201

@ns.route('/<int:node_id>')
class Node(Resource):
    @jwt_required
    def get(self, node_id):
        node = node_module.get_node(node_id)
        if node is None:
            return {'error': 'Node not found'}, 404
        return {'node': node.to_dict()}

    @jwt_required
    def put(self, node_id):
        data = request.get_json()
        node = node_module.update_node(node_id, data['name'], data['description'], data['ip_address'], data['port'])
        return {'node': node.to_dict()}

    @jwt_required
    def delete(self, node_id):
        node_module.delete_node(node_id)
        return '', 204

# Define JWT authentication
jwt = JWTManager(app)

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    if username and password:
        user = node_module.authenticate(username, password)
        if user:
            access_token = create_access_token(identity=username)
            return {'access_token': access_token}
    return {'error': 'Invalid credentials'}, 401

if __name__ == '__main__':
    app.run(debug=True)

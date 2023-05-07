from flask import request, json, Response, Blueprint, jsonify, make_response
from marshmallow import ValidationError
from ..models.UserModel import UserModel, UserSchema
from ..shared.authorization import Authentication

user_api = Blueprint('users', __name__)
user_schema = UserSchema()


@user_api.route('/api/v1/users/', methods=['POST'], strict_slashes=False)
def create():
    request_data = request.get_json()
    print(request_data)
    try:
        data = user_schema.load(request_data)
    except ValidationError as error:
        return Response(response=error.messages, status=400, mimetype="application/json")

    user_exists = UserModel.get_user_by_username(data.get('username'))
    if user_exists:
        message = "Username is taken, please select another username"
        return Response(response=message, status=400, mimetype="application/json")

    user = UserModel(data)
    user.save()

    user_data = user_schema.dump(user)

    return make_response(jsonify(user_data), 201)

@user_api.route('/api/v1/users/login/', methods=['POST'])
def login():
    request_data = request.get_json()

    try:
        data = user_schema.load(request_data, partial=True)
    except Exception as error:
        return make_response(json.dumps({'error': error}), 400)

    print(data)
    if not data['username'] or not data['password']:
        return make_response(json.dumps({'error': 'Please provide a username and password'}), 400)

    user = UserModel.get_user_by_username(data['username'])

    if not user:
        return make_response(json.dumps({'error': 'invalid credentials'}), 400)

    if not user.check_hash(data.get('password')):
        return make_response(json.dumps({'error': 'invalid credentials'}), 400)

    user_data = user_schema.dump(user)

    token = Authentication.generate_token(user_data.get('user_id'))

    user_data['token'] = token

    print('Token' + token)

    return make_response(jsonify(user_data), 200)

@user_api.route('/api/v1/users/', methods=['GET'])
def get_all():
    users = UserModel.get_all_users()
    all_users = user_schema.dump(users, many=True)
    return make_response(jsonify(all_users), 200)


@user_api.route('/api/v1/users/<int:user_id>/', methods=['GET'])
def get_a_user(user_id):
    """
    Get a single user
    """
    user = UserModel.get_one_user(user_id)
    if not user:
        return make_response(json.dumps({'error': 'User not found'}),404)

    print(user_schema.dump(user))
    selected_user = user_schema.dump(user)
    return make_response(jsonify(selected_user), 200)

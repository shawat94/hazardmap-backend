from flask import request, json, Response, Blueprint
from ..models.UserModel import UserModel, UserSchema
from ..shared.authorization import Authentication

user_api = Blueprint('users', __name__)
user_schema = UserSchema()

@user_api.route('/', methods=['POST'])
def create():
    request_data = request.get_json()
    data, error = user_schema.load(request_data)

    if error:
        return Response(response=error, status=400)

    user_exists = UserModel.get_user_by_name(data.get('name'))
    if user_exists:
        message = "Username is taken, please select another username"
        return Response(response=message, status=400)

    user=UserModel(data)
    user.save()

    user_data = user_schema.dump(user).data

    token = Authentication.generate_token(user_data.get('id'))

    return Response(response=json.dumps({'jwt_token': token}), status=201)

@user_api.route('/login', methods=['POST'])
def login():
    request_data = request.get_json()

    data, error = user_schema.load(request_data, partial=True)

    if error:
        return Response(response=json.dumps({'error': error}, status=400))

    if not data.get('username') or data.get('password'):
        return Response(response=json.dumps({'error': 'Please provide a username and password'}, status=400))

    user = UserModel.get_user_by_email(data.get('username'))

    if not user:
        return Response(response=json.dumps({'error': 'invalid credentials'}), status=400)

    if not user.check_hash(data.get('password')):
        return Response(response=json.dumps({'error': 'invalid credentials'}), status=400)

    user_data = user_schema.dump(user).data

    token = Authentication.generate_token(user_data.get('id'))

    return Response(response=json.dumps({'jwt_token': token}), status=200)

@user_api.route('/', methods=['GET'])
@Authentication.auth_required
def get_all():
    users = UserModel.get_all_users()
    all_users = user_schema.dump(users, many=True).data
    return Response(response=json.dumps({'data': all_users}), status=200)


@user_api.route('/<int:user_id>', methods=['GET'])
@Authentication.auth_required
def get_a_user(user_id):
    """
    Get a single user
    """
    user = UserModel.get_one_user(user_id)
    if not user:
        return Response(response=json.dumps({'error': 'User not found'}), status=404)

    selected_user = user_schema.dump(user).data
    return Response(response=json.dumps({'data': selected_user}), status=200)

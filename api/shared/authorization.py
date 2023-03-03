import jwt
import os
import datetime
from flask import json, Response, request, g
from functools import wraps
from ..models.UserModel import UserModel

class Authentication():
    @staticmethod
    def generate_token(user_id):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                'iat': datetime.datetime.utcnow(),
                'id': user_id
                }
            return jwt.encode(payload,
                              os.getenv('JWT_SECRET_KEY'),
                              'HS256').decode('utf-8')
        except Exception as e:
            return Response(
                mimetype="application/json",
                response=json.dumps({'error': 'Unable to generate user token'}),
                status=400
            )

    @staticmethod
    def decode_token(token):
        response = {'data': {}, 'error': {}}
        try:
            payload = jwt.decode(token, os.getend('JWT_SECRET_KEY'))
            response['data'] = {'user_id': payload['id']}
            return response
        except jwt.ExpiredSignatureError:
            response['error'] = {'message': 'Authentication token has expired. Please log in again'}
            return response
        except jwt.InvalidTokenError:
            response['error'] = {'message': 'Authentication token is invalid'}

    @staticmethod
    def auth_required(func):
        @wraps(func)
        def decorated_auth(*args, **kwargs):
            if 'api_token' not in request.headers:
                return Response(
                    mimetype="application/json",
                    response=json.dumps({'error': 'No authentication token was provided. Please login or register to '
                                                  'retrieve token'}),
                    status=400
                )
            token = request.headers.get('api_token')
            data = Authentication.decode_token(token)
            if data['error']:
                return Response(
                    mimetype="application/json",
                    response=json.dumps(data['error']),
                    status=400
                )

            user_id = data['data']['user_id']
            check_user = UserModel.get_one_user(user_id)
            if not check_user:
                return Response(
                    mimetype="application/json",
                    response=json.dumps({'error': 'No user is associated with this token'}),
                    status=400
                )
            g.user = {'id': user_id}
            return func(*args, **kwargs)

        return decorated_auth



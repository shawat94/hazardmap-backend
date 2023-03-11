from flask import request, make_response, json, Response, Blueprint, jsonify
from ..models.HazardModel import HazardModel, HazardSchema
from .UserController import get_a_user
import re
from ..shared.authorization import Authentication
from marshmallow import ValidationError
from ..shared.geometry import wkb_hazard_to_geojson, feature_list_to_feature_collection

hazard_api = Blueprint('hazards', __name__)
hazard_schema = HazardSchema()


@hazard_api.route('/api/v1/hazards/', methods=['POST'])
def create():
    request_data = request.get_json()

    try:
        data = hazard_schema.load(request_data)
    except ValidationError as error:
        print(error)
        return Response(response=error.messages, status=400, mimetype="application/json")
    bearer_token = request.headers.get('Authorization')
    print(bearer_token)
    token = re.match("^Bearer\s+(.*)", bearer_token).group(1)
    print(token)
    user_id = Authentication.decode_token(token)['data']['user_id']
    data['created_by'] = user_id
    hazard = HazardModel(data)

    try:
        hazard.save()
    except Exception as error:
        return make_response(json.dumps({'error': error}), 400)
    hazard_data = wkb_hazard_to_geojson(hazard_schema.dump(hazard))

    return make_response(jsonify(hazard_data), 200)

@hazard_api.route('/api/v1/hazards/', methods=['GET'], strict_slashes=False)
def get_all():
    hazards = HazardModel.get_all_hazards()
    all_hazards = hazard_schema.dump(hazards, many=True)
    formatted_hazards_list = list(map(wkb_hazard_to_geojson, all_hazards))
    hazard_collection = feature_list_to_feature_collection(formatted_hazards_list)
    #response = Response(response=json.dumps({'data': formatted_hazards}), status=200)
    response = make_response(jsonify(hazard_collection), 200)
    return response

@hazard_api.route('/api/v1/hazards/<int:hazard_id>/', methods=['GET'], strict_slashes=False)
def get_a_hazard(hazard_id):
    hazard = HazardModel.get_one_hazard(hazard_id)
    if not hazard:
        return Response(response=json.dumps({'error': '/Hazard not found'}), status=404)

    selected_hazard = hazard_schema.dump(hazard)
    formatted_hazard = wkb_hazard_to_geojson(selected_hazard)
    return make_response(jsonify(formatted_hazard), 200)

@hazard_api.route('/api/v1/hazards/<int:hazard_id>/', methods=['DELETE'], strict_slashes=False)
def delete_a_hazard(hazard_id):
    hazard = HazardModel.get_one_hazard(hazard_id)
    if not hazard:
        return Response(response=json.dumps({'error': 'Hazard not found'}), status=404)

    hazard.delete()
    return make_response(jsonify(f'Hazard {hazard_id} has been deleted.'), 200)


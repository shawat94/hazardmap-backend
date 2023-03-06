from flask import request, make_response, json, Response, Blueprint, jsonify
from ..models.HazardModel import HazardModel, HazardSchema
from .UserController import get_a_user
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

    token = request.headers.get('authorization')

    print(token)

    user_id = Authentication.decode_token(token)['data']['user_id']

    print(json.dumps(user_id))

    user = json.loads(get_a_user(user_id).data)

    print(user)

    data['created_by'] = user_id

    print(data)

    hazard = HazardModel(data)

    try:
        hazard.save()
    except Exception as error:
        return make_response(json.dumps({'error': error}), 400)
    hazard_data = hazard_schema.dump(hazard)

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
    formatted_hazard = hazard_to_geojson(selected_hazard)
    return Response(response=json.dumps({'data': formatted_hazard}), status=200)

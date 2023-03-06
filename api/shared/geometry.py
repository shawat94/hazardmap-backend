import shapely
from shapely.geometry import mapping
from collections import ChainMap


def feature_list_to_feature_collection(feature_list):
    feature_collection_format = {'type': 'FeatureCollection', 'features': []}
    for feature in feature_list:
        feature_collection_format['features'].append(feature)
    return feature_collection_format


def wkb_hazard_to_geojson(feature):
    properties = []
    feature_format = {'type': 'Feature',
                      'geometry': {},
                      'properties': []}
    for key in feature.keys():
        if key == 'geom':
            feature_format['geometry'] = mapping(shapely.wkb.loads(str(feature[key]), True))
        else:
            properties.append({key: feature[key]})
    feature_format['properties'] = dict(ChainMap(*properties))
    return feature_format

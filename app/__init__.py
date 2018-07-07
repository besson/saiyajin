from flask import Flask
from flask_restful import reqparse, Resource, Api
from flask_cors import CORS

from app.queries.simple_match_builder import SimpleMatchBuilder

from . import config
import requests
import json

app = Flask(__name__)
CORS(app)

api = Api(app)
parser = reqparse.RequestParser()


class Search(Resource):

    def get(self):
        parser.add_argument('q')
        query_string = parser.parse_args()

        response = {}
        results = [self._get_results(SimpleMatchBuilder(30, query_string['q']).build(), 'simple_match')]
        response['results'] = results

        return response

    def _get_results(self, es_query, query_type):
        url = config.es_base_url['places'] + '/_search'
        data = requests.post(url, headers={'content-type': 'application/json'},
                             data=json.dumps(es_query)).json()

        result = {'type': query_type, 'total': data['hits']['total']}
        places = []

        for hit in data['hits']['hits']:
            place = {'name': hit['_source']['name'],
                     'city': hit['_source']['city'],
                     'reviews': hit['highlight']['reviews.text.search']}

            places.append(place)

        result['places'] = places

        return result


api.add_resource(Search, '/search')

from flask import Flask
from flask_restful import reqparse, Resource, Api
from flask_cors import CORS

from app.queries.simple_match_builder import SimpleMatchBuilder
from app.queries.phrase_match_builder import PhraseMatchBuilder

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
        results = [
            self._get_results(SimpleMatchBuilder(30, query_string['q']).build(), 'simple_match'),
            self._get_results(PhraseMatchBuilder(30, query_string['q']).build(), 'phrase_match')
        ]

        totals = []
        max_total = 0
        query_total = len(results)

        for result in results:
            if result['total'] > max_total:
                max_total = result['total']
            totals.append({'type': result['type'], 'total': result['total']})

        places = []
        for i in range(max_total):
            for j in range(query_total):
                if i < len(results[j]['places']):
                    places.append(results[j]['places'][i])

        response['totals'] = totals
        response['places'] = places

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
                     'reviews': hit['highlight']['reviews.text.search'],
                     'type': query_type}

            if len(hit['_source']['photos']) > 0:
               place['main_photo_url'] = self._photo_url(hit['_source']['photos'][0]['photo_id'])
               place['photos'] = hit['_source']['photos']

            places.append(place)

        result['places'] = places

        return result

    def _photo_url(self, photo_id):
        return "https://s3-media1.fl.yelpcdn.com/bphoto/%s/300s.jpg" % photo_id


api.add_resource(Search, '/search')

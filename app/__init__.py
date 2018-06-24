from flask import Flask
from flask_restful import reqparse, Resource, Api
from . import config
import requests
import json

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()

class Search(Resource):

    def get(self):
        parser.add_argument('q')
        query_string = parser.parse_args()
        url = config.es_base_url['places']+'/_search'

        query = {
            "_source": ["reviews.text", "city", "name"],
            "size": 10,
            "query": {
                "multi_match": {
                    "query": query_string['q'],
                    "fields": ["reviews.text", "city"]
                }
            },
            "highlight" : {
                "fields" : { "reviews.text" :  {"type" : "plain"} }
            }
        }

        data = requests.post(url, headers={'content-type': 'application/json'},
        data=json.dumps(query)).json()
        places = []

        for hit in data['hits']['hits']:
            #place = hit['_source']['city']
            #place = hit['_source']['name']
            #place = hit['_source']['reviews']
            place = hit['highlight']['reviews.text']
            places.append(place)

        return places

api.add_resource(Search, '/search')

from flask import Flask
from flask_restful import reqparse, Resource, Api
from flask_cors import CORS


from app.search_service import SearchService

app = Flask(__name__)
CORS(app)

api = Api(app)
parser = reqparse.RequestParser()


class SearchController(Resource):

    def get(self):
        parser.add_argument('q')
        query_string = parser.parse_args()

        return SearchService().phrase_search(query_string['q'])


class ExplorerController(Resource):

    def get(self):
        parser.add_argument('q')
        query_string = parser.parse_args()

        return SearchService().explore(query_string['q'])


api.add_resource(SearchController, '/search')
api.add_resource(ExplorerController, '/explore')

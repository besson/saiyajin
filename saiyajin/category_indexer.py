import elasticsearch.helpers
import json
import hashlib
from elasticsearch import Elasticsearch

REQUEST_TIMEOUT = 300


class CategoryIndexer:

    def __init__(self, es):
        self.__index = 'place_category'
        self.__es = es

    def index(self):

        def bulk_place_docs():
            with open('dataset/business.json') as data:
                for line in data:
                        _doc = json.loads(line)

                        categories = _doc['categories']

                        for name in categories:
                            doc = {'_index': self.__index,
                                   '_type': 'category',
                                   '_id': self._md5(name),
                                   '_source': {'name': name}}

                            print(doc)
                            yield doc

        self.__es.indices.delete(self.__index, ignore=[400, 404])
        self.__es.indices.create(self.__index, body=json.load(open('elasticsearch/category_mapping.json')))

        elasticsearch.helpers.bulk(es, bulk_place_docs(), request_timeout=REQUEST_TIMEOUT)

    def _md5(self, content):
        return hashlib.md5(content.lower().encode('utf-8')).hexdigest()

if __name__ == '__main__':
    es = Elasticsearch([{'host': 'localhost',  'port': 9200}])
    CategoryIndexer(es).index()

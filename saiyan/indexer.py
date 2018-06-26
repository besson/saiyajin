import json
import elasticsearch.helpers
from elasticsearch import Elasticsearch

class Indexer:

    def __init__(self, es):
        self.__index = 'saiyan'
        self.__es = es

    def index(self):
        self.__es.indices.delete(self.__index, ignore=[400, 404])
        self.__es.indices.create(self.__index, body=json.load(open('elasticsearch/mappings.json')))

        def bulk_place_docs():
            with open('dataset/business.json') as data:
                for line in data:
                        _doc = json.loads(line)
                        _doc['reviews'] = []

                        doc = {'_index': self.__index,
                               '_type': 'place',
                               '_id': _doc['business_id'],
                               '_source': _doc}

                        print(doc)
                        yield doc

        print('------------------------- Adding reviews -----------------------------')

        def bulk_review_docs():
            with open('dataset/review.json') as data:
                for line in data:
                    _doc = json.loads(line)

                    doc = {'_index': self.__index,
                           '_id': _doc['business_id'],
                           '_op_type': 'update',
                           '_type': 'place',
                           'script' : {
                                'source': 'ctx._source.reviews.add(params.review)',
                                'lang' : 'painless',
                                'params' : {'review' : _doc}
                                }
                            }

                    print(doc)
                    yield doc

        elasticsearch.helpers.bulk(es, bulk_place_docs())
        elasticsearch.helpers.bulk(es, bulk_review_docs())

if __name__ == '__main__':
    es = Elasticsearch([{'host': 'localhost',  'port': 9200}])
    Indexer(es).index()

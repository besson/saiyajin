import json
import elasticsearch.helpers
from elasticsearch import Elasticsearch
import sys

REQUEST_TIMEOUT = 300


class Indexer:

    def __init__(self, es):
        self.__index = 'saiyajin'
        self.__es = es

    def index(self, mode = 'all'):

        def bulk_place_docs():
            with open('dataset/business-short.json') as data:
                for line in data:
                        _doc = json.loads(line)
                        _doc['reviews'] = []
                        _doc['photos'] = []

                        doc = {'_index': self.__index,
                               '_type': 'place',
                               '_id': _doc['business_id'],
                               '_source': _doc}

                        print(doc)
                        yield doc

        def bulk_review_docs():
            with open('dataset/review-short.json') as data:
                for line in data:
                    _doc = json.loads(line)

                    doc = {'_index': self.__index,
                           '_id': _doc['business_id'],
                           '_op_type': 'update',
                           '_type': 'place',
                           'script': {
                                'source': 'ctx._source.reviews.add(params.review)',
                                'lang': 'painless',
                                'params': {'review': _doc}
                                }
                            }

                    print(doc)
                    yield doc

        def bulk_photo_docs():
            with open('dataset/photos.json') as data:
                for line in data:
                    _doc = json.loads(line)

                    doc = {'_index': self.__index,
                           '_id': _doc['business_id'],
                           '_op_type': 'update',
                           '_type': 'place',
                           'script': {
                               'source': 'ctx._source.photos.add(params.photo)',
                               'lang': 'painless',
                               'params': {'photo': _doc}
                           }
                           }

                    print(doc)

                    yield doc

        if mode == 'all':
            self.__es.indices.delete(self.__index, ignore=[400, 404])
            self.__es.indices.create(self.__index, body=json.load(open('elasticsearch/mappings.json')))

            elasticsearch.helpers.bulk(es, bulk_place_docs(), request_timeout=REQUEST_TIMEOUT)
            elasticsearch.helpers.bulk(es, bulk_review_docs(), request_timeout=REQUEST_TIMEOUT)
            elasticsearch.helpers.bulk(es, bulk_photo_docs(), request_timeout=REQUEST_TIMEOUT)
        elif mode == 'place':
            elasticsearch.helpers.bulk(es, bulk_place_docs(), request_time=REQUEST_TIMEOUT)
        elif mode == 'review':
            elasticsearch.helpers.bulk(es, bulk_review_docs(), request_timeout=REQUEST_TIMEOUT)
        elif mode == 'photo':
            elasticsearch.helpers.bulk(es, bulk_photo_docs(), request_timeout=REQUEST_TIMEOUT)


if __name__ == '__main__':
    es = Elasticsearch([{'host': 'localhost',  'port': 9200}])
    mode = sys.argv[1] if len(sys.argv) > 1 else 'all'
    Indexer(es).index(mode)

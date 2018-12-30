from app.queries.simple_match import SimpleMatch
from app.queries.simple_match_best import SimpleMatchBest
from app.queries.simple_match_cross import SimpleMatchCross
from app.queries.phrase_match import PhraseMatch
from app.queries.simple_agg import SimpleAgg
from . import config
import requests
import json


class SearchService:

    def phrase_search(self, query):
        response = {}
        results = [
            self._get_results(SimpleMatch(30, query).build(), 'simple_match'),
            self._get_results(PhraseMatch(30, query).build(), 'phrase_match')
        ]

        self._build_response(response, results)
        return response

    def explore(self, query):
        response = {}
        results = [
            self._get_results(SimpleMatchCross(30, query).build(), 'simple_match_cross'),
            self._get_results(SimpleMatchBest(30, query).build(), 'simple_match_best')
        ]

        self._build_response(response, results)
        return response

    def extract(self, text):
        return {'categories': self._get_aggs(SimpleAgg(text).build())}

    def _build_response(self, response, results):
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

    def _get_results(self, es_query, query_type):
        url = config.es_base_url['places'] + '/_search'
        data = requests.post(url, headers={'content-type': 'application/json'},
                             data=json.dumps(es_query)).json()

        result = {'type': query_type, 'total': data['hits']['total']}
        places = []

        for hit in data['hits']['hits']:
            try:
                place = {'name': hit['_source']['name'],
                         'city': hit['_source']['city'],
                         'type': query_type}

                if 'highlight' in hit:
                    place['reviews'] = hit['highlight']['reviews.text.search']

                if len(hit['_source']['photos']) > 0:
                    place['main_photo_url'] = self._photo_url(hit['_source']['photos'][0]['photo_id'])
                    place['photos'] = hit['_source']['photos']

                places.append(place)
            except Exception as e:
                print(e)
                pass


        result['places'] = places

        return result

    def _get_aggs(self, es_query):
        url = config.es_base_url['categories'] + '/_search'
        data = requests.post(url, headers={'content-type': 'application/json'},
                             data=json.dumps(es_query)).json()

        aggs = data['aggregations']['categ_agg']['buckets']
        result = []

        if len(aggs) > 0:
            for agg in aggs:
                result.append(agg['key'])

        return result

    def _photo_url(self, photo_id):
        return "https://s3-media1.fl.yelpcdn.com/bphoto/%s/300s.jpg" % photo_id

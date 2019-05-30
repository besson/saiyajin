class SimpleAgg:

    def __init__(self, query, size=0):
        self.__size = size
        self.__query = query

    def build(self):
        return {
                "size": self.__size,
                "query": {
                    "multi_match": {
                        "query": self.__query,
                        "analyzer": "english_expander",
                        "fields": ["name.keyword"]
                    }
                },
                "aggs": {
                    "categ_agg": {
                        "terms": {
                            "field": "name.keyword",
                            "size": 100
                        }
                    }
                }
            }


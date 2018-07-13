class PhraseMatchBuilder:

    def __init__(self, size, query):
        self.__size = size
        self.__query = query

    def build(self):
        return {
            "_source": [
                "reviews.text",
                "city",
                "name",
                "photos"
            ],
            "size": self.__size,
            "query": {
                "bool": {
                    "should": [
                        {
                            "multi_match": {
                                "query": self.__query,
                                "fields": [
                                    "reviews.text.search^2",
                                    "city",
                                    "photos.caption.search"
                                ],
                                "type": "cross_fields"
                            }
                        },
                        {
                            "match_phrase": {
                                "reviews.text.search": {
                                    "query": self.__query,
                                    "slop": 2
                                }
                            }
                        }
                    ]
                }
            },
            "highlight": {
                "fields": {
                    "reviews.text.search": {}
                },
                "pre_tags": ["<span class=\"badge badge-warning\">"],
                "post_tags": ["</span>"]
            }
        }

class SimpleMatchCross:

    def __init__(self, size, query):
        self.__size = size
        self.__query = query

    def build(self):
        return {
                    "_source": ["reviews.text", "city", "name", "photos"],
                    "size": self.__size,
                    "query": {
                        "bool": {
                            "should": [
                                {
                                    "multi_match": {
                                        "query": self.__query,
                                        "fields": ["reviews.text.search", "city", "name", "photos.caption.search^2"],
                                        "type": "cross_fields",
                                        "minimum_should_match": "50%"

                                    }
                                }
                            ],
                            "must": {
                                "exists": {"field": "photos"}
                            }
                        }
                    },
                    "highlight": {
                        "fields": {"reviews.text.search":  {}},
                        "pre_tags": ["<span class=\"badge badge-dark\">"],
                        "post_tags": ["</span>"]
                    }
                }

class SimpleMatchBuilder:

    def __init__(self, size, query):
        self.__size = size
        self.__query = query

    def build(self):
        return {
                    "_source": ["reviews.text", "city", "name"],
                    "size": self.__size,
                    "query": {
                        "multi_match": {
                            "query": self.__query,
                            "fields": ["reviews.text.search", "city"]
                        }
                    },
                    "highlight" : {
                        "fields" : { "reviews.text.search" :  {} },
                        "pre_tags" : ["<kbd>"],
                        "post_tags" : ["</kbd>"]
                    }
                }

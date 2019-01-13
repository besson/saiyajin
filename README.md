# saiyan
Project to study search features in general (full text relevance, NLP and LTR).
It will be extended to be a generic tool but so far it depends on some particular
Elasticsearch schemas.

## Dependencies
* Elasticsearch (> 6.0)
* Python 3
* [Yelp free dataset](https://www.yelp.com/dataset)

## Indexing
First run virtualevn:

1. ```cd saiyan```
2. ```virtualenv venv```
3. ```$pip3 install -r requirements.txt```

Then run indexer:
* everything: ```$python indexer.py``` or ```$python indexer.py all```
* Only places: ```$python indexer.py places```
* Only photos: ```$python indexer.py photos```
* Only reviews: ```$python indexer.py reviews```
* Categories: ```$python category_indexer.py```

## Running search service (backend)
1. ```cd saiyan```
2. ```virtualenv venv```
3. ```source venv/bin/activate```
4. ```python3 -m flask run```

## Running frontend
1. ```cd saiyan/frontend```
2. ```virtualenv venv```
3. ```source venv/bin/activate```
4. ```python3 -m http.server```

## Important urls
##### Search service runs on port 5000
* search: */search?q=term*
* explore: */explore?q=term*
* extract: */explore?q=text*

##### Frontend runs on port 8000
* search: */#/*  (compare match strategies and highlights found terms)
* visualize: */#/visualize* (visualize rank changes through photos)
* extract: */#/visualize* (extract entities)

## dataset
Yelp free dataset: https://www.yelp.com/dataset (thanks)

## frontend
Flask + AngularJs inspired by: https://github.com/bonzanini/CheerMeApp-demo (thanks)

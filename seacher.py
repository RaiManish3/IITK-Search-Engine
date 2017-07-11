import re
from elasticsearch import Elasticsearch
from elasticsearch_dsl import *
from elasticsearch_dsl.connections import connections

## establish the connection between elasticSearch and python
es = Elasticsearch()
es = connections.create_connection(hosts=['re-es.canary'])

def search():
    # make predictive.(i.e can handle common errors)
    key = input('Enter the search query: ')
    lst_urls = []

    es.indices.refresh(index="engine")
    search_body = {
            "query":{
                "pageData":key
                }
            }

    res = es.search(index="engine",body=search_body)
    for hit in res['hits']['hits']:
        data = hit["_source"]
        lst_urls.append(data["url"])

    print(lst_urls)

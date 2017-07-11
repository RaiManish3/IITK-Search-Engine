import re
from elasticsearch import Elasticsearch
from elasticsearch_dsl import *
from elasticsearch_dsl.connections import connections

if __name__ == "__main__":
    # make predictive.(i.e can handle common errors)
    key = raw_input('Enter the search query: ')
    lst_urls = []

    ## establish the connection between elasticSearch and python
    es = Elasticsearch(['http://localhost:9200/'],verify_certs=True)
    #es = connections.create_connection(hosts=['re-es.canary'])
    es.indices.refresh(index="engine")
    search_body = {
            "query":{
                "match":{
                    "pageData":key
                    }
                }
            }

    res = es.search(index="engine",body=search_body)
    for hit in res['hits']['hits']:
        data = hit["_source"]
        lst_urls.append(data["url"])

    print(lst_urls)

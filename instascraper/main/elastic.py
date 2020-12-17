import requests
from elasticsearch import Elasticsearch

r = requests.get('http://localhost:9200')

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

results = []

resp = es.search(index="scrapy-2020-12", size=10000, body={"query": {"match_all": {}}})

# print(resp)

for row in resp["hits"]["hits"]:
    results.append((row["_source"]["image_url"], row["_source"]["captions"], row["_source"]["image_description"]))

print(results)

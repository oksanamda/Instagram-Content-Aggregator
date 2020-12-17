from flask import Flask, render_template, request, jsonify, make_response, redirect, url_for
import random
import time
import requests
from elasticsearch import Elasticsearch
import json

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

db = list()  # The mock database

posts = 500  # num posts to generate

quantity = 20  # num posts to return per request

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.form.to_dict()
        return redirect(url_for("load", instatag = data['instatag']))
    return render_template('index.html')


@app.route('/result')
def result():
    return render_template('result_page.html')


@app.route("/result/load/<instatag>")
def load(instatag):
    """ Route to return the posts """

    #requests.post('http://localhost:1000', data={'tag': instatag})


    results = []
    #resp = es.search(index="scrapy", size=10000, body={"query": {"match_all": {}}})
    with open('C:/Users/Денис/Documents/милена/Instagram-Content-Aggregator/instascraper/main/items.json', encoding='utf8') as f:
        resp = json.loads(f.read())
    f.close() 
    for post in resp: # resp["hits"]["hits"]:
        results.append((post["image_url"], post["captions"], post["image_description"]))
        #results.append((row["_source"]["image_url"], row["_source"]["captions"], row["_source"]["image_description"]))

    return render_template('result_page.html', results=results)

if __name__ == '__main__':
    app.run(debug = True)
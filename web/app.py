from flask import Flask, render_template, request, jsonify, make_response, redirect, url_for
import random
import time
import requests
from elasticsearch import Elasticsearch
import json
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
import random
from flask import Response


es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


def create_figure():

    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)

    return fig


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

    # requests.post('http://localhost:1000', data={'tag': instatag})


    results = []

    resp = es.search(index="scrapy-2020-12", size=10000, body={"query": {"match_all": {}}})

    # with open('/home/oksana/Documents/Instagram-Content-Aggregator/instascraper/main/items.json', encoding='utf8') as f:
    #     resp = json.loads(f.read())
    # f.close()

    for row in resp["hits"]["hits"]:
        results.append((row["_source"]["image_url"], row["_source"]["captions"], row["_source"]["image_description"],
                        row["_source"]["sentiment"]))

        sent = float(row["_source"]["sentiment"])



    return render_template('result_page.html', results=results)


if __name__ == '__main__':
    app.run(debug = True)

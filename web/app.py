from flask import Flask, render_template, request, redirect, url_for
import requests
from elasticsearch import Elasticsearch
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import io
from flask import Response


es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/<sentiment>/plot.png')
def plot_png(sentiment):
    sentiment = float(sentiment)
    rgb = lambda x: x / 255
    pos = int(sentiment)
    neg = round((100 * (sentiment % 1)))
    fig, ax = plt.subplots(figsize=(8, 4))

    x = ['positive', 'neutral', 'negative']
    y = [pos, 100 - pos - neg, neg]
    ax.bar(x, y, color=[(rgb(168), rgb(206), rgb(220)),
                        (rgb(242), rgb(242), rgb(242)),
                        (rgb(255), rgb(192), rgb(192))])

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.form.to_dict()
        requests.post('http://scraping/', data={'instatag': data['instatag']})
        requests.post('http://scraping/', data={'instatag': 'restart_scrapy'})
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
                        float(row["_source"]["sentiment"])))

        #sent = float(row["_source"]["sentiment"])
        #print(sent)



    return render_template('result_page.html', results=results)


if __name__ == '__main__':
    app.run(debug=True, port=5001)

from flask import Flask, request, url_for, redirect
from hashtag import crawler, InstagramSpider, reactor
import scrapy
import requests

app = Flask(__name__)

def spider_ended(spider, reason):
    print('Spider ended:', spider.name, reason)

@app.route('/', methods=['POST', 'GET'])
def hello():
    if request.method == 'POST':
        class InstagramSpiderForTag(InstagramSpider):
            def __init__(self, hashtag = request.form.to_dict()['instatag']):
                self.hashtag = hashtag
                print(hashtag)
        crawler.crawl(InstagramSpiderForTag)
        print('something2')
        crawler.stop()
        print('something3')
        reactor.run()
        print('something4')
        reactor.stop()
        #rawler.signals.connect(reactor.stop, signal=scrapy.signals.spider_closed)
        print('something')
        #requests.post('http://localhost:1488', data={'status': 'okay'})
    return 'Hello world1!'#redirect(url_for(hello))

if __name__ == '__main__':
    app.run(debug=True, port=5002)

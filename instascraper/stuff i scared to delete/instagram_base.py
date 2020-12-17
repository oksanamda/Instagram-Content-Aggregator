import scrapy
from urllib.parse import urlencode
import json
from datetime import datetime
from twisted.internet import reactor
from scrapy.crawler import CrawlerProcess
from scrapy import signals
import scrapyelasticsearch
import requests
import pd
import cod


API = cod.apicod()
user_accounts = ['nice_merch'] 


def stop_reactor():
    reactor.stop()


def get_url(url):
    payload = {'api_key': API, 'url': url}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    return proxy_url


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['api.scraperapi.com']
    custom_settings = {'CONCURRENT_REQUESTS_PER_DOMAIN': 5}

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(InstagramSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_opened, signals.spider_opened)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_opened(self, spider):
        print('Opening {} spider'.format(spider.name))

    def spider_closed(self, spider):
        print('Closing {} spider'.format(spider.name))

    def start_requests(self):
        for username in user_accounts:
            url = f'https://www.instagram.com/{username}/?hl=ru'
            yield scrapy.Request(get_url(url), callback=self.parse)

    def parse(self, response):
        x = response.xpath("//script[starts-with(.,'window._sharedData')]/text()").extract_first()
        json_string = x.strip().split('= ')[1][:-1]
        data = json.loads(json_string)
        # all that we have to do here is to parse the JSON we have
        user_id = data['entry_data']['ProfilePage'][0]['graphql']['user']['id']
        next_page_bool = \
            data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['page_info'][
                'has_next_page']
        edges = data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_felix_video_timeline']['edges']
        for i in edges:
            url = 'https://www.instagram.com/p/' + i['node']['shortcode']
            video = i['node']['is_video']
            date_posted_timestamp = i['node']['taken_at_timestamp']
            date_posted_human = datetime.fromtimestamp(date_posted_timestamp).strftime("%d/%m/%Y %H:%M:%S")
            like_count = i['node']['edge_liked_by']['count'] if "edge_liked_by" in i['node'].keys() else ''
            comment_count = i['node']['edge_media_to_comment']['count'] if 'edge_media_to_comment' in i[
                'node'].keys() else ''
            captions = ""
            if i['node']['edge_media_to_caption']:
                for i2 in i['node']['edge_media_to_caption']['edges']:
                    captions += i2['node']['text'] + "\n"

            if video:
                image_url = i['node']['display_url']
            else:
                image_url = i['node']['thumbnail_resources'][-1]['src']
            item = {'postURL': url, 'isVideo': video, 'date_posted': date_posted_human,
                    'timestamp': date_posted_timestamp, 'likeCount': like_count, 'commentCount': comment_count, 'image_url': image_url,
                    'captions': captions[:-1]}
            if video:
                yield scrapy.Request(get_url(url), callback=self.get_video, meta={'item': item})
            else:
                item['videoURL'] = ''
                yield item
        if next_page_bool:
            cursor = \
                data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['page_info'][
                    'end_cursor']
            di = {'id': user_id, 'first': 12, 'after': cursor}
            # print(di)
            params = {'query_hash': 'e769aa130647d2354c40ea6a439bfc08', 'variables': json.dumps(di)}
            url = 'https://www.instagram.com/graphql/query/?' + urlencode(params)
            yield scrapy.Request(get_url(url), callback=self.parse_pages, meta={'pages_di': di})

    def parse_pages(self, response):
        di = response.meta['pages_di']
        data = json.loads(response.text)
        # print(data)
        for i in data['data']['user']['edge_owner_to_timeline_media']['edges']:
            video = i['node']['is_video']
            url = 'https://www.instagram.com/p/' + i['node']['shortcode']
            if video:
                image_url = i['node']['display_url']
                video_url = i['node']['video_url']
            else:
                video_url = ''
                image_url = i['node']['thumbnail_resources'][-1]['src']
            date_posted_timestamp = i['node']['taken_at_timestamp']
            captions = ""
            if i['node']['edge_media_to_caption']:
                for i2 in i['node']['edge_media_to_caption']['edges']:
                    captions += i2['node']['text'] + "\n"
            comment_count = i['node']['edge_media_to_comment']['count'] if 'edge_media_to_comment' in i['node'].keys() else ''
            print("\n\n\n\n")
            print(i['node']['edge_media_to_comment'])
            print("\n\n\n\n")
            date_posted_human = datetime.fromtimestamp(date_posted_timestamp).strftime("%d/%m/%Y %H:%M:%S")
            like_count = i['node']['edge_liked_by']['count'] if "edge_liked_by" in i['node'].keys() else ''

            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            Picture_request = requests.get(image_url)
            with open("tmp.jpg", 'wb') as f:
                f.write(Picture_request.content)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            item = {'postURL': url, 'isVideo': video, 'date_posted': date_posted_human,
                    'timestamp': date_posted_timestamp, 'likeCount': like_count, 'commentCount': comment_count,
                    'image_url': image_url,
                    'videoURL': video_url, 'captions': captions[:-1],
                    'image_description': pd.findObjects("tmp.jpg")}
            yield item
        next_page_bool = data['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
        if next_page_bool:
            cursor = data['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
            di['after'] = cursor
            params = {'query_hash': 'e769aa130647d2354c40ea6a439bfc08', 'variables': json.dumps(di)}
            url = 'https://www.instagram.com/graphql/query/?' + urlencode(params)
            yield scrapy.Request(get_url(url), callback=self.parse_pages, meta={'pages_di': di})

    def get_video(self, response):
        item = response.meta['item']
        video_url = response.xpath('//meta[@property="og:video"]/@content').extract_first()
        item['videoURL'] = video_url
        yield item


crawler = CrawlerProcess({
    "FEEDS": {
        "items.json": {"format": "json"},
    },
    "ITEM_PIPELINES": {
        'scrapyelasticsearch.scrapyelasticsearch.ElasticSearchPipeline': 500
    },
    "ELASTICSEARCH_SERVERS": ['http://127.0.0.1:9200'],
    "ELASTICSEARCH_INDEX": 'scrapy',
    "ELASTICSEARCH_TYPE": 'items',
})


crawler.crawl(InstagramSpider)

reactor.run()

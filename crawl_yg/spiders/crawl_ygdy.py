import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from crawl_yg.items import CrawlYgItem
import re

class CrawlYgdySpider(CrawlSpider):
    name = 'crawl_ygdy'
    allowed_domains = ['www.ygdy8.com']
    start_urls = ['https://www.ygdy8.com/html/gndy/dyzz/index.html']

    rules = (
        Rule(LinkExtractor(allow=r'/html/gndy/[a-z]+/\d+/\d+.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'html/gndy/[a-z]+/\w+.html'), follow=True),
    )

    def parse_item(self, res):
        item = CrawlYgItem()
        item['cat'] = res.xpath('//*[@class="path"]/ul/a[last()]/text()').extract_first()
        item['url'] = res.url
        item['title'] = res.xpath('//*[contains(@class,"bd3l") or contains(@class,"bd3r")]/div[2]/div[1]/h1/font/text()').extract_first()
        item['cover'] = res.xpath('//*[@id="Zoom"]//img[1]/@src').extract_first()
        item['source'] = res.xpath('//*[@id="Zoom"]//a[starts-with(@href,"magnet:?xt=urn:") or starts-with(@href,"ftp://")]/@href').extract_first()

        # 如果资源地址找不到，直接返回
        if not item['source']:
            return

        # 提取详情页面电影信息
        zoom_el = res.xpath('//*[@id="Zoom"]')[0].extract()
        film_info = {}
        film_info['trans_name'] = re.search(r'◎译　　名(.*?)<br>', zoom_el, re.S)
        if film_info['trans_name'] is None:
            film_info['trans_name'] = re.search(r'◎中文　名(.*?)<br>', zoom_el, re.S)

        film_info['name'] = re.search(r'◎片　　名(.*?)<br>', zoom_el, re.S)
        film_info['year'] = re.search(r'◎年　　代(.*?)<br>', zoom_el, re.S)
        film_info['country'] = re.search(r'◎国　　家(.*?)<br>', zoom_el, re.S)
        if film_info['country'] is None:
            film_info['country'] = re.search(r'◎产　　地(.*?)<br>', zoom_el, re.S)

        film_info['type'] = re.search(r'◎类　　别(.*?)<br>', zoom_el, re.S)
        film_info['language'] = re.search(r'◎语　　言(.*?)<br>', zoom_el, re.S)
        film_info['subtitles'] = re.search(r'◎字　　幕(.*?)<br>', zoom_el, re.S)
        film_info['length'] = re.search(r'◎片　　长(.*?)<br>', zoom_el, re.S)
        film_info['director'] = re.search(r'◎导　　演(.*?)<br>', zoom_el, re.S)
        film_info['actor'] = re.search(r'◎演　　员(.*?)◎', zoom_el, re.S)
        if film_info['actor'] is None:
            film_info['actor'] = re.search(r'◎主　　演(.*?)<br>', zoom_el, re.S)

        film_info['introduce'] = re.search(r'◎简　　介(.*?)<a ', zoom_el, re.S)

        for key, value in film_info.items():
            if value is not None:
                item[key] = value.group(1).strip()
            else:
                item[key] = 'No Value'
        if item['actor'] != 'No Value':
            lists = item['actor'].split('<br>')
            for index, value in enumerate(lists):
                lists[index] = value.strip()
                if index > 9:
                    lists = lists[: 10]
                    break
            item['actor'] = lists

        if len(item['introduce']) > 150:
            item['introduce'] = item['introduce'][:150]
        yield item

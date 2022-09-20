# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlYgItem(scrapy.Item):
    # define the fields for your item here like:
    # define the fields for your item here like:
    cat = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    source = scrapy.Field()
    cover = scrapy.Field()

    trans_name = scrapy.Field()
    name = scrapy.Field()
    year = scrapy.Field()
    country = scrapy.Field()

    type = scrapy.Field()
    language = scrapy.Field()
    subtitles = scrapy.Field()
    length = scrapy.Field()

    director = scrapy.Field()
    actor = scrapy.Field()
    introduce = scrapy.Field()

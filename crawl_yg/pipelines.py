# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class CrawlYgPipeline:
    def process_item(self, item, spider):
        with open('tmp/ygdy.txt', 'a', encoding='UTF-8', errors='ignore') as f:
            f.write(str(item) + ',\n')
        return item

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import csv
from posixpath import join as join, exists

from yaozhotc.items import YaozhotcItem

class YaozhotcPipeline(object):

    def __init__(self, base_dir):
        self.base_dir = base_dir

    def open_spider(self, spider):
        base_dir = self.base_dir
        data_dir = join(base_dir, 'data')
        if not exists(data_dir):
            os.mkdir(data_dir)
        filepath = join(data_dir, 'otc.csv')
        spider._f = fobj = open(filepath, 'w')
        spider._w = csv.DictWriter(
            fobj, fieldnames=YaozhotcItem.fields.keys()
        )
        spider._w.writeheader()

    def close_spider(self, spider):
        spider._f.close()
        self.convert_to_winfile()

    def convert_to_winfile(self):
        base_dir = self.base_dir
        data_dir = join(base_dir, 'data')
        filepath = join(data_dir, 'otc.csv')
        win_path = join(data_dir, 'otc.windows.csv')
        with open(filepath, 'r') as f:
            lines = f.readlines()
        with open(win_path, 'wb') as win_f:
            for line in lines:
                win_f.write(line.encode('gb18030'))

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            base_dir=crawler.settings.get('BASE_DIR')
        )

    def process_item(self, item, spider):
        spider._w.writerow(dict(item))
        spider._f.flush()
        return item

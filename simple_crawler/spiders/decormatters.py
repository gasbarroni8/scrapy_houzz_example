# -*- coding: utf-8 -*-
from __future__ import absolute_import

import scrapy
import pandas as pd
from ..items import ProductItem

class Houzz(scrapy.Spider):
    name = 'houzz'
    allowed_domains = ['www.houzz.com']
    style = ''
    start_urls = []    
        # df = pd.DataFrame({"style":[], "url":[]}) 

    def __init__(self, **kwargs):
      # self.start_urls = [
      #   f'https://www.houzz.com/products/{self.style}/living-room-furniture',
      # ]
      self.start_urls = [
        f'https://www.houzz.com/products/{self.style}/living-room-furniture',
        f'https://www.houzz.com/products/{self.style}/kitchen-and-dining-furniture',
        f'https://www.houzz.com/products/{self.style}/bedroom-furniture',
        f'https://www.houzz.com/products/{self.style}/home-office-furniture',
        f'https://www.houzz.com/products/{self.style}/patio-furniture',
        f'https://www.houzz.com/products/{self.style}/bathroom-storage-and-vanities',
        f'https://www.houzz.com/products/{self.style}/storage-furniture',
        f'https://www.houzz.com/products/{self.style}/entryway-furniture'
      ]
      super().__init__(**kwargs)

    def parse(self, response):
        products = response.css(".hz-product-card__link")
        for product in products:
            name = product.css('.hz-color-link__text ::text').extract_first()

            img = product.css('.hz-image-container img::attr(data-src)').extract_first()
            if not img:           
                img = product.css('.hz-image-container img::attr(src)').extract_first()
            item = ProductItem()
            item['name'] = name
            item['img'] = img
            yield item

        nextSelector = response.css('.hz-pagination-link--next::attr("href")')
        if nextSelector:
            nextSelectorLink = nextSelector[0].extract()
            nextLink = f"http://{self.allowed_domains[0]}{nextSelectorLink}"
            yield scrapy.Request(url=nextLink)
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
    styles = [
        'contemporary', 
        'eclectic', 
        'modern', 
        'traditional', 
        'asian', 
        'beach-style', 
        'craftsman', 
        'farmhouse',
        'industrial',
        'mediterranean',
        'midcentury',
        'rustic',
        'scandinavian',
        'southwestern',
        'tropical',
        'transitional',
        'victorian'
    ]

    def __init__(self, **kwargs):
        for style in self.styles:
            temp = [
                f'https://www.houzz.com/products/{style}/living-room-furniture',
                f'https://www.houzz.com/products/{style}/kitchen-and-dining-furniture',
                f'https://www.houzz.com/products/{style}/bedroom-furniture',
                f'https://www.houzz.com/products/{style}/home-office-furniture',
                f'https://www.houzz.com/products/{style}/patio-furniture',
                f'https://www.houzz.com/products/{style}/bathroom-storage-and-vanities',
                f'https://www.houzz.com/products/{style}/storage-furniture',
                f'https://www.houzz.com/products/{style}/entryway-furniture'
            ]
            self.start_urls.extend(temp)    

        super().__init__(**kwargs)

    def parse(self, response):
        style = [ele for ele in self.styles if(ele in response.url)] 
        assert len(style) == 1
        style = style[0]
        products = response.css(".hz-product-card__link")
        for product in products:
            name = product.css('.hz-color-link__text ::text').extract_first()

            img_url = product.css('.hz-image-container img::attr(src)').extract_first()
            item = ProductItem()
            item['name'] = name
            item['img_url'] = img_url
            item['style'] = style
            item['product_url'] = response.url

            if "data:image" in img_url:
                continue

            yield item

        nextSelector = response.css('.hz-pagination-link--next::attr("href")')
        if nextSelector:
            nextSelectorLink = nextSelector[0].extract()
            nextLink = f"http://{self.allowed_domains[0]}{nextSelectorLink}"
            yield scrapy.Request(url=nextLink)
import scrapy


class KbmkItem(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()

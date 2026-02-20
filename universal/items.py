import scrapy


class UniversalItem(scrapy.Item):

    url = scrapy.Field()

    title = scrapy.Field()

    content = scrapy.Field()

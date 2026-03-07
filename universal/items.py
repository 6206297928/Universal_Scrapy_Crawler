import scrapy


class UniversalItem(scrapy.Item):

    url = scrapy.Field()

    domain = scrapy.Field()

    title = scrapy.Field()

    content = scrapy.Field()

    length = scrapy.Field()

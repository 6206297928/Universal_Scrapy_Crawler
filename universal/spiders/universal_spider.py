import scrapy
from urllib.parse import urlparse
from scrapy_playwright.page import PageMethod
from universal.utils.content_extractor import clean_content


class UniversalSpider(scrapy.Spider):

    name = "universal"

    start_urls = [
        # "https://docs.scrapy.org/en/latest/",
        # "https://library.municode.com/tx/austin/codes/code_of_ordinances"
        #   "https://en.wikipedia.org/wiki/Web_scraping"
        # "https://httpbin.org/html",
        "https://example.com",
        # "https://quotes.toscrape.com",
        # "https://www.goodreads.com/quotes",
        # "https://www.zyte.com",
        # "https://en.wikipedia.org/wiki/Web_scraping",
        # "https://docs.scrapy.org/en/latest/",

    ]

    visited = set()

    # NEW Scrapy 2.13+ warning fix
    async def start(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta={
                    "playwright": True,
                    "playwright_page_methods": [
                        PageMethod("wait_for_selector", "body"),
                        PageMethod("wait_for_timeout", 3000),
                    ],
                },
                callback=self.parse,
            )

    def parse(self, response):

        url = response.url

        if url in self.visited:
            return

        self.visited.add(url)

        raw_content = self.extract_main_content(response)

        content = clean_content(raw_content)

        if len(content) > 200:

            yield {
                "url": url,
                "domain": urlparse(url).netloc,
                "title": response.css("title::text").get(),
                "content": content,
                "length": len(content),
            }

        # follow links safely
        for href in response.css("a::attr(href)").getall():

            if not href:
                continue

            href = href.strip()

            # skip invalid links
            if (
                href.startswith("mailto:")
                or href.startswith("javascript:")
                or href.startswith("#")
            ):
                continue

            next_url = response.urljoin(href)

            if next_url in self.visited:
                continue

            yield scrapy.Request(
                next_url,
                callback=self.parse,
                meta={
                    "playwright": True,
                    "playwright_page_methods": [
                        PageMethod("wait_for_timeout", 2000),
                    ],
                },
                errback=self.errback,
            )

    def extract_main_content(self, response):

        candidates = response.css("main, article, section, div")

        best_text = ""
        best_score = 0

        for el in candidates:

            text_list = el.css("*::text").getall()

            text = " ".join(
                t.strip() for t in text_list if t.strip()
            )

            text_length = len(text)

            if text_length < 200:
                continue

            link_count = len(el.css("a"))

            paragraph_count = len(el.css("p"))

            score = (
                text_length
                + paragraph_count * 200
                - link_count * 100
            )

            if score > best_score:

                best_score = score
                best_text = text

        return best_text

    def errback(self, failure):

        self.logger.warning(
            f"Request failed: {failure.request.url}"
        )

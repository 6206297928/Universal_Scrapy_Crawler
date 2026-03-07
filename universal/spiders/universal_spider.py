import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse
from scrapy_playwright.page import PageMethod
from universal.utils.content_extractor import extract_content
from universal.items import UniversalItem


class UniversalSpider(CrawlSpider):
    """
    Universal web crawler using Scrapy's built-in architecture:

    - CrawlSpider + Rule + LinkExtractor  → automatic link following
    - RFPDupeFilter (default)             → automatic deduplication
    - UniversalItem                       → structured item class
    - FEEDS setting                       → built-in JSON feed export
    """

    name = "universal"

    start_urls = [
        "https://example.com",
    ]

    # ─── Link-following rules ───────────────────────────────
    # LinkExtractor automatically:
    #   • extracts all <a href> links
    #   • filters out mailto:, javascript:, # fragments
    #   • canonicalizes URLs
    # Scrapy's RFPDupeFilter automatically:
    #   • fingerprints every request
    #   • drops duplicate URLs (no manual "visited" set needed)
    rules = (
        Rule(
            LinkExtractor(),
            callback="parse_page",
            follow=True,
            process_request="set_playwright_meta",
        ),
    )

    # ─── Scrapy 2.13+ async start ──────────────────────────
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
                # No callback → defaults to CrawlSpider.parse
                # which processes rules + calls parse_start_url
            )

    def parse_start_url(self, response):
        """Extract content from the start URLs as well."""
        return self.parse_page(response)

    # ─── Inject Playwright meta into followed requests ──────
    def set_playwright_meta(self, request, response):
        """Called by Rule's process_request for every followed link."""
        return request.replace(
            meta={
                **request.meta,
                "playwright": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_timeout", 2000),
                ],
            }
        )

    # ─── Content extraction callback ───────────────────────
    def parse_page(self, response):
        """
        Extract main content using trafilatura and yield a structured UniversalItem.

        trafilatura handles boilerplate removal, article detection,
        and noise filtering — replacing the old heuristic scorer.
        """

        content = extract_content(response.text)

        if len(content) > 200:

            item = UniversalItem()
            item["url"] = response.url
            item["domain"] = urlparse(response.url).netloc
            item["title"] = response.css("title::text").get()
            item["content"] = content
            item["length"] = len(content)
            yield item

BOT_NAME = "universal"

SPIDER_MODULES = ["universal.spiders"]
NEWSPIDER_MODULE = "universal.spiders"

ROBOTSTXT_OBEY = False

# Demo crawl limits
DEPTH_LIMIT = 2
CLOSESPIDER_PAGECOUNT = 10

LOG_LEVEL = "INFO"

# ========================
# PLAYWRIGHT DOWNLOAD HANDLER
# ========================

DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

# Required reactor
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

PLAYWRIGHT_BROWSER_TYPE = "chromium"

PLAYWRIGHT_LAUNCH_OPTIONS = {
    "headless": True,
}

# ========================
# PERFORMANCE
# ========================

CONCURRENT_REQUESTS = 8
DOWNLOAD_TIMEOUT = 60
AUTOTHROTTLE_ENABLED = True

# ========================
# IMPORTANT: DO NOT ADD THIS
# ========================
# DO NOT include scrapy_playwright.middleware

PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = 60000
DOWNLOAD_TIMEOUT = 120


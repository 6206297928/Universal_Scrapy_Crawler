BOT_NAME = "universal"

SPIDER_MODULES = ["universal.spiders"]
NEWSPIDER_MODULE = "universal.spiders"

ROBOTSTXT_OBEY = True

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

# ========================
# BUILT-IN FEED EXPORT
# ========================
# Replaces custom pipeline — Scrapy writes output.json automatically
FEEDS = {
    "output.json": {
        "format": "json",
        "overwrite": True,
    },
}

# ========================
# HTTP CACHE (dev speed boost)
# ========================
# Caches responses locally so re-runs don't re-download pages.
# Delete .scrapy_cache/ folder to force a fresh crawl.
HTTPCACHE_ENABLED = True
HTTPCACHE_DIR = ".scrapy_cache"
HTTPCACHE_EXPIRATION_SECS = 86400  # cache expires after 24 hours
HTTPCACHE_IGNORE_HTTP_CODES = [403, 500, 502, 503]  # don't cache error pages

# ============================================================
# Custom pipeline no longer needed.
#
# Output is handled by Scrapy's built-in Feed Export system
# configured via the FEEDS setting in settings.py:
#
#   FEEDS = {
#       "output.json": {"format": "json", "overwrite": True},
#   }
#
# This writes output.json automatically when the spider closes.
# ============================================================


class UniversalPipeline:
    """Placeholder — kept for future custom processing if needed."""

    def process_item(self, item, spider):
        return item

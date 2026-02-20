# 🕷️ Universal Scrapy Crawler

A production-ready, universal web scraper built with **Scrapy** and **Playwright** that can crawl any website, extract meaningful content, and chunk it into AI-ready pieces for vector databases and retrieval systems.

---

## ✨ Features

- **Universal Crawling** — Works on any website, no site-specific selectors needed
- **JavaScript Rendering** — Uses Playwright under the hood to handle SPAs and dynamic content
- **Smart Content Extraction** — Automatically identifies the main content area using a scoring algorithm (text length, paragraph count, link density)
- **Content Cleaning** — Strips extra whitespace, unicode artifacts, and noise
- **AI-Ready Chunking** — Splits extracted content into overlapping chunks with metadata, ready for vector DB ingestion
- **Link Following** — Automatically discovers and follows internal links up to a configurable depth
- **Auto-Throttling** — Built-in rate limiting and concurrency control to be respectful to target servers

---

## 📁 Project Structure

```
universal_scrapy_crawler/
├── main.py                              # Chunking pipeline entry point
├── scrapy.cfg                           # Scrapy project config
├── pyproject.toml                       # Project dependencies (uv/pip)
├── output.json                          # Raw scraped data (generated)
├── chunks.json                          # Chunked output (generated)
├── run.txt                              # Quick-reference run commands
│
└── universal/
    ├── __init__.py
    ├── items.py                         # Scrapy item schema
    ├── middlewares.py                   # Scrapy middlewares
    ├── pipelines.py                     # Data pipeline (saves to output.json)
    ├── settings.py                      # Scrapy + Playwright settings
    │
    ├── spiders/
    │   └── universal_spider.py          # Main spider with Playwright support
    │
    └── utils/
        ├── content_extractor.py         # Text cleaning utilities
        └── chunker.py                   # Content chunking engine
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| [Scrapy](https://scrapy.org/) | Web crawling framework |
| [Playwright](https://playwright.dev/) (via `scrapy-playwright`) | JavaScript rendering |
| [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) | HTML parsing |
| [lxml](https://lxml.de/) | Fast XML/HTML parser |
| [uv](https://docs.astral.sh/uv/) | Python package manager |

---

## 🚀 Getting Started

### Prerequisites

- Python **3.12+**
- [uv](https://docs.astral.sh/uv/) package manager

### Installation

```bash
# Clone the repo
git clone https://github.com/6206297928/Universal_Scrapy_Crawler.git
cd Universal_Scrapy_Crawler

# Install dependencies
uv sync

# Install Playwright browsers
uv run playwright install
```

---

## ▶️ Usage

### Step 1: Crawl a Website

Edit the `start_urls` list in `universal/spiders/universal_spider.py` to add your target URLs:

```python
start_urls = [
    "https://example.com",
    # Add more URLs here
]
```

Then run the spider:

```bash
uv run scrapy crawl universal -O output.json
```

This will:
- Crawl the target site(s) with JavaScript rendering
- Follow links up to depth 2 (configurable in `settings.py`)
- Extract and clean main content from each page
- Save structured results to `output.json`

### Step 2: Chunk the Content

Once you have `output.json`, run the chunking pipeline:

```bash
uv run python main.py
```

This will:
- Read the scraped data from `output.json`
- Filter out pages with less than 200 characters of content
- Split content into overlapping chunks (800 chars with 100 char overlap)
- Save AI-ready chunks to `chunks.json`

---

## ⚙️ Configuration

### Spider Settings (`universal/settings.py`)

| Setting | Default | Description |
|---------|---------|-------------|
| `DEPTH_LIMIT` | `2` | Max link-following depth |
| `CLOSESPIDER_PAGECOUNT` | `10` | Max pages to crawl per run |
| `CONCURRENT_REQUESTS` | `8` | Parallel request limit |
| `DOWNLOAD_TIMEOUT` | `120` | Page load timeout (seconds) |
| `AUTOTHROTTLE_ENABLED` | `True` | Automatic rate limiting |
| `PLAYWRIGHT_BROWSER_TYPE` | `chromium` | Browser engine to use |

### Chunker Settings (`universal/utils/chunker.py`)

| Parameter | Default | Description |
|-----------|---------|-------------|
| `chunk_size` | `800` | Max characters per chunk |
| `overlap` | `100` | Overlapping characters between chunks |
| `min_chunk_size` | `100` | Minimum useful chunk size |

---

## 📤 Output Format

### `output.json` — Raw scraped data

```json
[
  {
    "url": "https://example.com",
    "domain": "example.com",
    "title": "Example Domain",
    "content": "This domain is for use in illustrative examples...",
    "length": 1256
  }
]
```

### `chunks.json` — AI-ready chunks

```json
[
  {
    "url": "https://example.com",
    "domain": "example.com",
    "title": "Example Domain",
    "chunk_id": 0,
    "text": "This domain is for use in illustrative examples...",
    "length": 782
  }
]
```

---

## 🧠 How It Works

```
Target URL
    │
    ▼
┌──────────────────────┐
│  Playwright Browser   │  ← Renders JavaScript
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Universal Spider     │  ← Extracts main content using scoring algorithm
│  (Scrapy)             │     Score = text_length + (paragraphs × 200) - (links × 100)
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Content Cleaner      │  ← Removes whitespace, unicode artifacts
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Pipeline             │  ← Saves to output.json
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Content Chunker      │  ← Splits into overlapping chunks with metadata
└──────────┬───────────┘
           │
           ▼
      chunks.json          ← Ready for Vector DB / RAG pipeline
```

---

## 📄 License

This project is open source and available for personal and educational use.

---

## 👤 Author

**Sukumar Poddar**
- GitHub: [@6206297928](https://github.com/6206297928)

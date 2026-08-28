# Affinity Answers Assignment

This repository contains the solution for **Task 1: Product Information Extraction** (Web Scraping MDComputers).

## Project Overview

The objective of Task 1 is to write a Python program that accepts a search term as user input, constructs a search URL for [MDComputers](https://mdcomputers.in/), fetches and parses the search results page, and extracts the product names and selling prices.

---

## Directory Structure

```
Affinity-Answer assignment/
├── ReadMe.md                          # Master project documentation
└── question1/                         # Task 1 Solution Directory
    ├── scraper.PY                     # Main Python scraper script
    ├── requirements.txt               # Dependencies (requests, beautifulsoup4)
    └── scrapingdocumentation.md       # Full technical documentation for scraper.PY
```

---

## Quick Start

### 1. Install Dependencies
Navigate to the `question1` directory and install the required Python packages:
```bash
cd question1
pip install -r requirements.txt
```

### 2. Run the Scraper
Run `scraper.PY` using Python:
```bash
python scraper.PY
```

When prompted, enter your desired search term (e.g., `external hard drive`, `graphics card`, `ssd`):
```text
Enter search term: external hard drive
```

---

## Documentation

Full detailed technical documentation—including architecture, HTTP 403 WAF bypass details, DOM selector strategies, and function definitions—can be found in:

👉 **[question1/scrapingdocumentation.md](file:///d:/code/Affinity-Answer%20assignment/question1/scrapingdocumentation.md)**

# Affinity Answers Assignment

This repository contains the solutions for the Affinity Answers technical assessment tasks:
1. **Question 1 — Web Scraping**: Product Information Extraction from MDComputers.
2. **Question 2 — SQL & Database**: Database queries against the public Rfam MySQL database.
3. **Question 3 — Unix Shell Scripting**: Processing and sorting S&P 500 company CSV dataset.

---

## Directory Structure

```
Affinity-Answer assignment/
├── ReadMe.md                          # Master project documentation
├── question1/                         # Task 1: Web Scraping Solution
│   ├── scraper.PY                     # Python scraper script
│   ├── requirements.txt               # Dependencies (requests, beautifulsoup4)
│   └── scrapingdocumentation.md       # Technical documentation for Question 1
├── question2/                         # Task 2: SQL & Database Solution
│   ├── queries.sql                    # SQL queries for Rfam database (2A, 2B, 2C)
│   └── queriesdocumentation.md        # Documentation and explanation for Task 2
└── question3/                         # Task 3: Unix Shell Scripting Solution
    ├── companies.sh                   # Shell script to fetch, parse, and sort CSV
    └── unixdocumentation.md           # Documentation for Question 3
```

---

## Quick Start & Execution

### Task 1: Product Information Extractor (Web Scraping)
```bash
cd question1
pip install -r requirements.txt
python scraper.PY
```
*Prompt:* Enter search term (e.g., `external hard drive`).

### Task 2: SQL Queries
Review [`question2/queries.sql`](file:///d:/code/Affinity-Answer%20assignment/question2/queries.sql) for queries written against the public Rfam database (`mysql-rfam-public.ebi.ac.uk:4497`).

### Task 3: Unix Shell Scripting
```bash
cd question3
chmod +x companies.sh
./companies.sh "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/refs/heads/main/data/constituents.csv"
```

---

## Documentation Links

- **Task 1 Documentation:** 👉 [`question1/scrapingdocumentation.md`](file:///d:/code/Affinity-Answer%20assignment/question1/scrapingdocumentation.md)
- **Task 2 Documentation:** 👉 [`question2/queriesdocumentation.md`](file:///d:/code/Affinity-Answer%20assignment/question2/queriesdocumentation.md)
- **Task 3 Documentation:** 👉 [`question3/unixdocumentation.md`](file:///d:/code/Affinity-Answer%20assignment/question3/unixdocumentation.md)

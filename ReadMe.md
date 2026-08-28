# MDComputers Product Information Extractor

A Python program to search and extract product names and selling prices from [MDComputers](https://mdcomputers.in/).

## Features
- Dynamic search URL construction based on user input.
- Sends full browser headers to avoid HTTP 403 (Forbidden) WAF blocks.
- Parses modern OpenCart / custom MDComputers HTML templates (`product-grid-item` cards).
- Correctly isolates current selling prices (discounted `ins` prices vs strikethrough `del` prices).
- Formats console output into aligned columns with support for UTF-8 currency symbols.

## Requirements
- Python 3.8+
- `requests`
- `beautifulsoup4`

To install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
Run the script using Python:
```bash
python TASK1.PY
```

Example input and execution:
```
Enter search term: external hard drive
```

## Project Structure
- `TASK1.PY`: Main Python script for search and extraction.
- `test.py`: Copy of script for testing.
- `requirements.txt`: Python package dependencies.

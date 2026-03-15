# hedge-lens

Extract structured data from hedge fund investor letters using Claude.

## Overview

hedge-lens downloads PDF investor letters, parses them with pdfplumber, sends
the text to Claude for structured extraction (holdings, performance, commentary),
and stores the results in a local SQLite database.

## Project Structure

```
hedge-lens/
├── src/
│   └── hedge_lens/       # Main package (src layout)
│       ├── __init__.py
│       ├── cli.py         # Click CLI entry point
│       ├── downloader.py  # PDF download logic
│       ├── parser.py      # PDF text extraction (pdfplumber)
│       ├── extractor.py   # Claude API extraction
│       └── storage.py     # SQLite storage
├── letters/               # Downloaded PDF files (gitignored)
├── tests/                 # Test suite
├── pyproject.toml
└── README.md
```

## Setup

```bash
pip install -e ".[dev]"
```

## Usage

```bash
# Download a letter
hedge-lens download <url>

# Extract data from a letter
hedge-lens extract letters/example.pdf

# List stored extractions
hedge-lens list
```

## Dependencies

- **pdfplumber** — PDF text extraction
- **anthropic** — Claude API client for structured extraction
- **click** — CLI framework
- **sqlite3** — Built-in Python module for local storage

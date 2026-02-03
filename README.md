# PDF Digitizer

Convert scanned PDFs to markdown using [Marker](https://github.com/VikParuchuri/marker) OCR.

## Installation

Requires Python 3.10+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

## Usage

```bash
# Output to stdout
uv run python digitize.py input.pdf

# Save to file
uv run python digitize.py input.pdf -o output.md

# Plain text output (strips markdown formatting)
uv run python digitize.py input.pdf --format text
```

## Features

- Converts scanned PDFs to clean markdown
- Handles complex layouts (tables, multi-column)
- Works on CPU or GPU (GPU is faster)
- Ideal for preparing documents for LLM processing

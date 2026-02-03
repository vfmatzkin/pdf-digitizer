# PDF Digitizer

Convert scanned PDFs to markdown using [Marker](https://github.com/VikParuchuri/marker) OCR.

## Installation

Requires Python 3.10+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

## Usage

```bash
# Convert single PDF (saves to <input_dir>/converted/<name>.md)
uv run python digitize.py input.pdf

# Convert all PDFs in a folder (saves to <folder>/converted/)
uv run python digitize.py ./invoices/

# Save to specific file or directory
uv run python digitize.py input.pdf -o output.md
uv run python digitize.py ./invoices/ -o ./output/

# Overwrite existing files without asking
uv run python digitize.py ./invoices/ -y

# Output to stdout (single PDF only)
uv run python digitize.py input.pdf --stdout

# Plain text output (strips markdown formatting)
uv run python digitize.py input.pdf --format text
```

## Features

- Converts scanned PDFs to clean markdown
- Handles complex layouts (tables, multi-column)
- Batch conversion with skip/overwrite options for existing files
- Works on CPU or GPU (GPU is faster)
- Ideal for preparing documents for LLM processing

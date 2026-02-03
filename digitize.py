#!/usr/bin/env python3
"""Convert scanned PDFs to markdown using Marker OCR."""

import argparse
import sys
from pathlib import Path


def convert_pdf(pdf_path: Path) -> str:
    """Convert a PDF file to markdown using Marker."""
    from marker.converters.pdf import PdfConverter
    from marker.models import create_model_dict

    models = create_model_dict()
    converter = PdfConverter(artifact_dict=models)
    result = converter(str(pdf_path))

    return result.markdown


def main():
    parser = argparse.ArgumentParser(
        description="Convert scanned PDFs to markdown using Marker OCR"
    )
    parser.add_argument("pdf", type=Path, help="Path to the PDF file")
    parser.add_argument(
        "-o", "--output", type=Path, help="Output file path (default: stdout)"
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "text"],
        default="markdown",
        help="Output format (default: markdown)",
    )

    args = parser.parse_args()

    if not args.pdf.exists():
        print(f"Error: PDF file not found: {args.pdf}", file=sys.stderr)
        sys.exit(1)

    if not args.pdf.suffix.lower() == ".pdf":
        print(f"Error: File must be a PDF: {args.pdf}", file=sys.stderr)
        sys.exit(1)

    try:
        markdown = convert_pdf(args.pdf)

        if args.format == "text":
            # Strip markdown formatting for plain text
            import re

            text = markdown
            # Remove headers
            text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
            # Remove bold/italic
            text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
            text = re.sub(r"\*([^*]+)\*", r"\1", text)
            text = re.sub(r"__([^_]+)__", r"\1", text)
            text = re.sub(r"_([^_]+)_", r"\1", text)
            # Remove links, keep text
            text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
            output = text
        else:
            output = markdown

        if args.output:
            args.output.write_text(output)
            print(f"Output saved to: {args.output}", file=sys.stderr)
        else:
            print(output)

    except Exception as e:
        print(f"Error converting PDF: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

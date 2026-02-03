#!/usr/bin/env python3
"""Convert scanned PDFs to markdown using Marker OCR."""

import argparse
import sys
from pathlib import Path


def convert_pdf(pdf_path: Path, models=None) -> str:
    """Convert a PDF file to markdown using Marker."""
    from marker.converters.pdf import PdfConverter
    from marker.models import create_model_dict

    if models is None:
        models = create_model_dict()
    converter = PdfConverter(artifact_dict=models)
    result = converter(str(pdf_path))

    return result.markdown


def get_output_path(pdf_path: Path, output_dir: Path | None = None) -> Path:
    """Get the output path for a PDF file."""
    if output_dir:
        output_dir.mkdir(exist_ok=True)
        return output_dir / pdf_path.with_suffix(".md").name
    else:
        converted_dir = pdf_path.parent / "converted"
        converted_dir.mkdir(exist_ok=True)
        return converted_dir / pdf_path.with_suffix(".md").name


def format_output(markdown: str, fmt: str) -> str:
    """Format the output based on the requested format."""
    if fmt == "text":
        import re
        text = markdown
        text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
        text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
        text = re.sub(r"\*([^*]+)\*", r"\1", text)
        text = re.sub(r"__([^_]+)__", r"\1", text)
        text = re.sub(r"_([^_]+)_", r"\1", text)
        text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
        return text
    return markdown


def main():
    parser = argparse.ArgumentParser(
        description="Convert scanned PDFs to markdown using Marker OCR"
    )
    parser.add_argument("input", type=Path, help="Path to PDF file or folder containing PDFs")
    parser.add_argument(
        "-o", "--output", type=Path, help="Output file (for single PDF) or directory (for folder input)"
    )
    parser.add_argument(
        "--stdout", action="store_true", help="Output to stdout instead of file (single PDF only)"
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "text"],
        default="markdown",
        help="Output format (default: markdown)",
    )
    parser.add_argument(
        "-y", "--yes", action="store_true", help="Overwrite existing files without asking"
    )

    args = parser.parse_args()

    if not args.input.exists():
        print(f"Error: Path not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    # Collect PDF files to process
    if args.input.is_dir():
        pdf_files = sorted(args.input.glob("*.pdf"))
        if not pdf_files:
            print(f"Error: No PDF files found in {args.input}", file=sys.stderr)
            sys.exit(1)
        if args.stdout:
            print("Error: --stdout not supported for folder input", file=sys.stderr)
            sys.exit(1)
    else:
        if not args.input.suffix.lower() == ".pdf":
            print(f"Error: File must be a PDF: {args.input}", file=sys.stderr)
            sys.exit(1)
        pdf_files = [args.input]

    # For folder input, determine output directory
    output_dir = None
    if args.input.is_dir() and args.output:
        output_dir = args.output
    elif args.input.is_dir():
        output_dir = args.input / "converted"

    # Check for existing outputs and ask for confirmation
    skip_existing = False
    if not args.stdout:
        existing_outputs = []
        for pdf_path in pdf_files:
            if args.input.is_file() and args.output:
                out_path = args.output
            else:
                out_path = get_output_path(pdf_path, output_dir)
            if out_path.exists():
                existing_outputs.append((pdf_path, out_path))

        if existing_outputs and not args.yes:
            print(f"{len(existing_outputs)} output file(s) already exist:", file=sys.stderr)
            for _, p in existing_outputs:
                print(f"  {p}", file=sys.stderr)
            response = input("Overwrite existing files? [y/N/s=skip existing]: ").strip().lower()
            if response == "y":
                pass  # Will overwrite
            elif response == "s":
                skip_existing = True
                # Remove already converted PDFs from the list
                existing_pdfs = {pdf for pdf, _ in existing_outputs}
                pdf_files = [p for p in pdf_files if p not in existing_pdfs]
                if not pdf_files:
                    print("All files already converted.", file=sys.stderr)
                    sys.exit(0)
            else:
                print("Aborted.", file=sys.stderr)
                sys.exit(0)

    # Load models once for batch processing
    models = None
    if len(pdf_files) > 1:
        print(f"Loading OCR models...", file=sys.stderr)
        from marker.models import create_model_dict
        models = create_model_dict()

    # Process each PDF
    for i, pdf_path in enumerate(pdf_files, 1):
        if len(pdf_files) > 1:
            print(f"[{i}/{len(pdf_files)}] Processing {pdf_path.name}...", file=sys.stderr)

        try:
            markdown = convert_pdf(pdf_path, models)
            output = format_output(markdown, args.format)

            if args.stdout:
                print(output)
            else:
                if args.input.is_file() and args.output:
                    output_path = args.output
                else:
                    output_path = get_output_path(pdf_path, output_dir)

                output_path.write_text(output)
                print(f"Output saved to: {output_path}", file=sys.stderr)

        except Exception as e:
            print(f"Error converting {pdf_path}: {e}", file=sys.stderr)
            if len(pdf_files) == 1:
                sys.exit(1)


if __name__ == "__main__":
    main()

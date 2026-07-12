#!/usr/bin/env python3
"""
pdf_metadata_extractor.py

Extracts bibliographic metadata from a directory of PDF source files and
batch-exports it as CSL-JSON for direct import into Zotero.

Three-tier fallback strategy per file:
  1. Embedded PDF metadata (XMP / DocInfo dictionary) via pypdf.
  2. Heuristic parse of the first-page text (title = largest early line,
     author/year patterns via regex) for PDFs with poor/missing metadata.
  3. Manual-review stub: if neither tier produces a usable title, the file
     is logged to a review queue instead of silently emitting a bad record.

Usage:
    pip install pypdf --break-system-packages
    python pdf_metadata_extractor.py /path/to/pdf/directory -o library.json

Output:
    A CSL-JSON array suitable for Zotero's "Import" (File > Import) feature.
"""

import argparse
import json
import re
import sys
from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError:
    print("Missing dependency. Run: pip install pypdf --break-system-packages", file=sys.stderr)
    sys.exit(1)

YEAR_RE = re.compile(r"\b(1[5-9]\d{2}|20\d{2})\b")
# Rough "Firstname Lastname" / "Lastname, F." author heuristics.
AUTHOR_LINE_RE = re.compile(
    r"^(?:by\s+)?([A-Z][a-zA-Z\.\-]+(?:\s+[A-Z][a-zA-Z\.\-]+){0,3})\s*$"
)


def tier1_embedded_metadata(reader: PdfReader) -> dict | None:
    """Attempt extraction from embedded PDF DocInfo/XMP metadata."""
    meta = reader.metadata
    if not meta:
        return None

    title = (meta.title or "").strip()
    author = (meta.author or "").strip()
    if not title:
        return None

    record = {
        "type": "article-journal",
        "title": title,
    }
    if author:
        record["author"] = [_split_author(a) for a in re.split(r";|,\s+and\s+| and ", author) if a.strip()]

    date_str = meta.get("/CreationDate") or ""
    year_match = YEAR_RE.search(str(date_str))
    if not year_match and meta.get("/ModDate"):
        year_match = YEAR_RE.search(str(meta.get("/ModDate")))
    if year_match:
        record["issued"] = {"date-parts": [[int(year_match.group(0))]]}

    return record


def tier2_first_page_heuristic(reader: PdfReader) -> dict | None:
    """Fall back to parsing visible text on the first page."""
    if len(reader.pages) == 0:
        return None
    try:
        text = reader.pages[0].extract_text() or ""
    except Exception:
        return None

    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    if not lines:
        return None

    # Heuristic: title is usually the longest of the first few non-trivial lines.
    candidate_lines = lines[:8]
    title = max(candidate_lines, key=len) if candidate_lines else None
    if not title or len(title) < 6:
        return None

    record = {"type": "article-journal", "title": title}

    authors = []
    for ln in lines[:12]:
        m = AUTHOR_LINE_RE.match(ln)
        if m and ln != title:
            authors.append(_split_author(m.group(1)))
    if authors:
        record["author"] = authors[:6]

    year_match = YEAR_RE.search(text[:2000])
    if year_match:
        record["issued"] = {"date-parts": [[int(year_match.group(0))]]}

    return record


def _split_author(name: str) -> dict:
    name = name.strip().rstrip(",")
    if "," in name:
        family, given = [p.strip() for p in name.split(",", 1)]
    else:
        parts = name.split()
        family = parts[-1] if parts else name
        given = " ".join(parts[:-1])
    return {"family": family, "given": given}


def extract_one(pdf_path: Path, review_queue: list) -> dict | None:
    try:
        reader = PdfReader(str(pdf_path))
    except Exception as e:
        review_queue.append((pdf_path.name, f"unreadable: {e}"))
        return None

    record = tier1_embedded_metadata(reader)
    tier_used = 1

    if record is None:
        record = tier2_first_page_heuristic(reader)
        tier_used = 2

    if record is None:
        review_queue.append((pdf_path.name, "no usable title from tiers 1-2; needs manual entry"))
        return None

    record["id"] = pdf_path.stem
    record["_extraction_tier"] = tier_used  # informational; strip before Zotero import if strict CSL-JSON needed
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("directory", type=Path, help="Directory containing PDF files")
    parser.add_argument("-o", "--output", type=Path, default=Path("library.json"), help="Output CSL-JSON path")
    parser.add_argument("--strict-csl", action="store_true", help="Strip non-CSL fields (e.g. _extraction_tier) from output")
    args = parser.parse_args()

    if not args.directory.is_dir():
        print(f"Not a directory: {args.directory}", file=sys.stderr)
        sys.exit(1)

    pdf_files = sorted(args.directory.glob("*.pdf"))
    if not pdf_files:
        print(f"No PDFs found in {args.directory}", file=sys.stderr)
        sys.exit(1)

    review_queue: list = []
    records = []
    for pdf_path in pdf_files:
        record = extract_one(pdf_path, review_queue)
        if record:
            if args.strict_csl:
                record.pop("_extraction_tier", None)
            records.append(record)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    print(f"Extracted {len(records)}/{len(pdf_files)} records -> {args.output}")
    if review_queue:
        print(f"\n{len(review_queue)} file(s) need manual review:")
        for name, reason in review_queue:
            print(f"  - {name}: {reason}")


if __name__ == "__main__":
    main()

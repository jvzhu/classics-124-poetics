"""
validate_recension_dataset.py

Validates a Jin Ping Mei recension-attribution benchmark file against
recension_schema.json, and prints basic dataset statistics (split
balance, task-type balance, difficulty balance) so you can spot gaps
before submitting to Kaggle.

Usage:
    python validate_recension_dataset.py recension_examples.json
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

from jsonschema import Draft7Validator


def load_schema(schema_path: Path) -> dict:
    return json.loads(schema_path.read_text(encoding="utf-8"))


def validate(records: list[dict], schema: dict) -> list[str]:
    validator = Draft7Validator(schema)
    errors = []
    for i, record in enumerate(records):
        for err in validator.iter_errors(record):
            rid = record.get("id", f"index-{i}")
            errors.append(f"[{rid}] {err.message} (at {'/'.join(str(p) for p in err.path)})")
    return errors


def check_placeholders(records: list[dict]) -> list[str]:
    """Flag records that still contain [PLACEHOLDER ...] scaffolding text,
    so you don't accidentally submit unfinished annotations."""
    warnings = []
    for record in records:
        blob = json.dumps(record)
        if "PLACEHOLDER" in blob:
            warnings.append(f"[{record.get('id', '?')}] still contains placeholder text")
    return warnings


def print_stats(records: list[dict]) -> None:
    print(f"\nTotal records: {len(records)}")
    for field in ("split", "task_type", "difficulty", "recension"):
        counts = Counter(r.get(field, "MISSING") for r in records)
        print(f"\n{field} distribution:")
        for value, count in counts.most_common():
            print(f"  {value}: {count}")


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python validate_recension_dataset.py <data.json> [schema.json]")
        sys.exit(1)

    data_path = Path(sys.argv[1])
    schema_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).parent / "recension_schema.json"

    records = json.loads(data_path.read_text(encoding="utf-8"))
    schema = load_schema(schema_path)

    errors = validate(records, schema)
    if errors:
        print(f"FAILED: {len(errors)} schema validation error(s):")
        for e in errors:
            print(f"  - {e}")
    else:
        print("Schema validation: PASSED")

    placeholder_warnings = check_placeholders(records)
    if placeholder_warnings:
        print(f"\n{len(placeholder_warnings)} record(s) still contain placeholder text:")
        for w in placeholder_warnings:
            print(f"  - {w}")

    print_stats(records)

    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Validate repository structure and the reviewed knowledge handoff."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "AGENTS.md",
    "PROJECT.md",
    "STATUS.md",
    "TODO.md",
    "RUNBOOK.md",
    "DECISIONS.md",
    "CLAIMS.md",
    "literature/protocol.yaml",
    "literature/search-log.md",
    "literature/source-inventory.csv",
    "literature/evidence-matrix.csv",
    "literature/notes/SOURCE_NOTE_TEMPLATE.md",
    "knowledge/schema/mindmap.schema.json",
    "knowledge/exports/mindmap.json",
    "sutras/manifest.csv",
]

EXPECTED_HEADERS = {
    "literature/source-inventory.csv": [
        "source_id", "locator", "bibliographic_identity", "source_type",
        "tradition_or_context", "language", "discovered_via", "access",
        "screening_stage", "decision", "reason", "duplicate_of",
        "overlap_notes", "version_or_date", "access_date", "notes",
    ],
    "literature/evidence-matrix.csv": [
        "source_id", "concept_ids", "claim_ids", "question_relevance",
        "tradition_context", "design_or_source_type", "text_or_sample",
        "source_language_and_translation", "phenomenon_or_teaching",
        "comparison", "outcomes_or_concepts", "analysis_or_hermeneutic",
        "result_or_passage", "author_interpretation",
        "reviewer_interpretation", "reported_limitations",
        "appraised_limitations", "funding_or_conflicts", "exact_locators",
        "access_level", "appraisal_summary",
    ],
    "sutras/manifest.csv": [
        "path", "source_id", "title", "canonical_id", "version",
        "source_url", "license", "sha256",
    ],
}


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def load_json(relative_path: str, errors: list[str]) -> dict:
    try:
        with (ROOT / relative_path).open(encoding="utf-8") as handle:
            value = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"{relative_path}: cannot load JSON: {exc}", errors)
        return {}
    if not isinstance(value, dict):
        fail(f"{relative_path}: top level must be an object", errors)
        return {}
    return value


def validate_export(data: dict, errors: list[str]) -> None:
    required = {
        "schema_version", "project", "generated_at", "review_status",
        "concepts", "edges", "sources",
    }
    missing = sorted(required - data.keys())
    if missing:
        fail(f"mindmap export: missing keys {missing}", errors)
        return
    if data.get("schema_version") != "0.1.0":
        fail("mindmap export: unsupported schema_version", errors)
    if data.get("project") != "sutrastudies":
        fail("mindmap export: project must be sutrastudies", errors)
    if data.get("review_status") not in {"draft", "reviewed", "released"}:
        fail("mindmap export: invalid review_status", errors)

    concepts = data.get("concepts")
    edges = data.get("edges")
    sources = data.get("sources")
    if not all(isinstance(items, list) for items in (concepts, edges, sources)):
        fail("mindmap export: concepts, edges, and sources must be arrays", errors)
        return

    concept_ids = [item.get("id") for item in concepts if isinstance(item, dict)]
    edge_ids = [item.get("id") for item in edges if isinstance(item, dict)]
    source_ids = [item.get("id") for item in sources if isinstance(item, dict)]
    for label, values in (("concept", concept_ids), ("edge", edge_ids), ("source", source_ids)):
        if len(values) != len(set(values)):
            fail(f"mindmap export: duplicate {label} IDs", errors)

    concept_set = set(concept_ids)
    source_set = set(source_ids)
    source_pattern = re.compile(r"^S\d{3,}$")
    claim_pattern = re.compile(r"^C\d{3,}$")

    for concept in concepts:
        if not isinstance(concept, dict):
            fail("mindmap export: each concept must be an object", errors)
            continue
        if not re.fullmatch(r"concept-[a-z0-9]+(?:-[a-z0-9]+)*", str(concept.get("id", ""))):
            fail(f"mindmap export: invalid concept ID {concept.get('id')!r}", errors)
        validate_provenance(concept, "concept", source_set, source_pattern, claim_pattern, errors)

    for edge in edges:
        if not isinstance(edge, dict):
            fail("mindmap export: each edge must be an object", errors)
            continue
        if edge.get("from") not in concept_set or edge.get("to") not in concept_set:
            fail(f"mindmap export: edge {edge.get('id')!r} has an unknown endpoint", errors)
        validate_provenance(edge, "edge", source_set, source_pattern, claim_pattern, errors)

    for source_id in source_ids:
        if not isinstance(source_id, str) or not source_pattern.fullmatch(source_id):
            fail(f"mindmap export: invalid source ID {source_id!r}", errors)


def validate_provenance(
    item: dict,
    item_type: str,
    source_set: set,
    source_pattern: re.Pattern,
    claim_pattern: re.Pattern,
    errors: list[str],
) -> None:
    item_id = item.get("id", "<missing>")
    for source_id in item.get("source_ids", []):
        if not isinstance(source_id, str) or not source_pattern.fullmatch(source_id):
            fail(f"mindmap export: {item_type} {item_id} has invalid source ID {source_id!r}", errors)
        elif source_id not in source_set:
            fail(f"mindmap export: {item_type} {item_id} references missing source {source_id}", errors)
    for claim_id in item.get("claim_ids", []):
        if not isinstance(claim_id, str) or not claim_pattern.fullmatch(claim_id):
            fail(f"mindmap export: {item_type} {item_id} has invalid claim ID {claim_id!r}", errors)
    if item.get("review_status") in {"reviewed", "released"}:
        if not item.get("source_ids") or not item.get("claim_ids"):
            fail(f"mindmap export: reviewed {item_type} {item_id} lacks provenance", errors)


def validate_sutra_manifest(errors: list[str]) -> None:
    manifest = ROOT / "sutras/manifest.csv"
    try:
        with manifest.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
    except OSError as exc:
        fail(f"sutras/manifest.csv: cannot read: {exc}", errors)
        return

    seen_paths: set[str] = set()
    for row in rows:
        relative_path = row.get("path", "")
        if not relative_path or relative_path in seen_paths:
            fail(f"sutras manifest: missing or duplicate path {relative_path!r}", errors)
            continue
        seen_paths.add(relative_path)
        source_path = ROOT / relative_path
        if not source_path.is_file():
            fail(f"sutras manifest: missing source file {relative_path}", errors)
            continue
        digest = hashlib.sha256(source_path.read_bytes()).hexdigest()
        if digest != row.get("sha256"):
            fail(f"sutras manifest: checksum mismatch for {relative_path}", errors)
        with source_path.open("rb") as handle:
            if source_path.suffix.lower() == ".pdf" and handle.read(5) != b"%PDF-":
                fail(f"sutras manifest: {relative_path} is not a PDF", errors)


def main() -> int:
    errors: list[str] = []
    for relative_path in REQUIRED_FILES:
        if not (ROOT / relative_path).is_file():
            fail(f"missing required file: {relative_path}", errors)

    for relative_path, expected in EXPECTED_HEADERS.items():
        try:
            with (ROOT / relative_path).open(newline="", encoding="utf-8") as handle:
                actual = next(csv.reader(handle))
        except (OSError, StopIteration) as exc:
            fail(f"{relative_path}: cannot read header: {exc}", errors)
            continue
        if actual != expected:
            fail(f"{relative_path}: unexpected CSV header", errors)

    schema = load_json("knowledge/schema/mindmap.schema.json", errors)
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        fail("mindmap schema: expected JSON Schema draft 2020-12", errors)
    export = load_json("knowledge/exports/mindmap.json", errors)
    validate_export(export, errors)
    validate_sutra_manifest(errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Repository validation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1

    print("Repository structure, ledgers, and knowledge handoff are valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

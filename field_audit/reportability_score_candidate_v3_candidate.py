"""Outcome-blind candidate scorer for Route A reportability rows.

This module implements only the owner-approved Route A amendment's source-role
rules. It remains a review candidate and must not be used on corpus claims until
independent review and a dated owner binding are complete.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from collections.abc import Mapping
from datetime import date
import hashlib
import json
from pathlib import Path
import re
from typing import Iterable, Union


STATUSES = ("REPORTED", "REFERENCED", "PARTIAL", "NOT_REPORTED")
REFERENCE_ALLOWED = frozenset({"T1-03"})
ITEM_TRANSITION = {
    "T1-01": "T1",
    "T1-02": "T1",
    "T1-03": "T1",
    "T2-01": "T2",
    "T2-02": "T2",
    "T3-01": "T3",
    "T3-02": "T3",
    "T4-01": "T4",
    "T4-02": "T4",
    "T5-01": "T5",
    "T5-02": "T5",
}
FIELDS = (
    "claim_id",
    "coder",
    "transition",
    "item_id",
    "status",
    "evidence_pointer",
    "source_file_sha256",
    "source_role",
    "source_id",
    "source_locator",
    "note",
    "adjudicator",
    "adjudication_date",
    "adjudication_rationale",
    "adjudication_source_pointer",
)
_SHA256 = re.compile(r"^[0-9a-f]{64}$")


class ReportabilityError(ValueError):
    """Raised when candidate rows cannot support a complete summary."""


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _validate_row(
    row: dict,
    claim_ids: set[str],
    coders: tuple[str, str],
    source_registry_by_claim_id: Mapping[str, dict],
) -> None:
    if not isinstance(row, dict):
        raise ReportabilityError("row must be an object")
    if any(not isinstance(field, str) for field in row):
        raise ReportabilityError("row keys must be strings")
    missing = [field for field in FIELDS if field not in row]
    extra = sorted(set(row) - set(FIELDS))
    if missing or extra:
        raise ReportabilityError(f"row schema mismatch: missing={missing}, extra={extra}")
    claim_id = row["claim_id"]
    if not _nonempty(claim_id) or claim_id not in claim_ids:
        raise ReportabilityError("claim_id is missing or outside the sampled claim set")
    item_id = row["item_id"]
    if not isinstance(item_id, str) or item_id not in ITEM_TRANSITION or row["transition"] != ITEM_TRANSITION[item_id]:
        raise ReportabilityError("item_id and transition do not match the frozen candidate map")
    status = row["status"]
    if status not in STATUSES:
        raise ReportabilityError(f"invalid status: {status!r}")
    if status == "REFERENCED" and item_id not in REFERENCE_ALLOWED:
        raise ReportabilityError(f"REFERENCED is not permitted for {item_id}")
    if any(not isinstance(row[field], str) for field in FIELDS):
        raise ReportabilityError("row fields must be strings")
    if not _nonempty(row["evidence_pointer"]) or not _nonempty(row["source_locator"]):
        raise ReportabilityError("evidence_pointer and source_locator are required")
    if not isinstance(row["source_file_sha256"], str) or not _SHA256.fullmatch(row["source_file_sha256"]):
        raise ReportabilityError("source_file_sha256 must be a lowercase SHA-256 digest")
    if status in {"PARTIAL", "NOT_REPORTED"} and not _nonempty(row["note"]):
        raise ReportabilityError("PARTIAL and NOT_REPORTED rows require a specific note")

    _validate_source_role(row, source_registry_by_claim_id)
    if status == "REFERENCED":
        _validate_referenced_pointer(row)

    coder = row["coder"]
    adjudication_fields = (
        row["adjudicator"],
        row["adjudication_date"],
        row["adjudication_rationale"],
        row["adjudication_source_pointer"],
    )
    if coder in coders:
        if any(_nonempty(value) for value in adjudication_fields):
            raise ReportabilityError("independent coder rows must leave adjudication fields blank")
    elif coder == "ADJUDICATED":
        if not all(_nonempty(value) for value in adjudication_fields):
            raise ReportabilityError("adjudicated rows require adjudicator, date, rationale, and pointer")
        if not isinstance(row["adjudication_date"], str) or not re.fullmatch(
            r"[0-9]{4}-[0-9]{2}-[0-9]{2}", row["adjudication_date"]
        ):
            raise ReportabilityError("adjudication_date must use ISO YYYY-MM-DD format")
        try:
            date.fromisoformat(row["adjudication_date"])
        except (TypeError, ValueError) as exc:
            raise ReportabilityError("adjudication_date must use ISO YYYY-MM-DD format") from exc
    else:
        raise ReportabilityError(f"unknown coder role: {coder!r}")


def _validate_referenced_pointer(row: dict) -> None:
    """Require the pointer to name both the target citation location and source ID.

    Candidate v3 serialization:
      target_locator=<target-paper locator>;cited_source_id=<registered source ID>
    The scorer validates the declared structure and ID match, not whether the
    locator truthfully identifies a citation in the target paper.
    """
    pointer = row["evidence_pointer"]
    prefix = "target_locator="
    marker = ";cited_source_id="
    if not pointer.startswith(prefix) or marker not in pointer:
        raise ReportabilityError(
            "REFERENCED evidence_pointer must bind target citation location and registered source ID"
        )
    locator, _, cited_source_id = pointer[len(prefix):].rpartition(marker)
    if not _nonempty(locator) or cited_source_id != row["source_id"]:
        raise ReportabilityError(
            "REFERENCED evidence_pointer must bind target citation location and registered source ID"
        )


def _validate_source_role(row: dict, source_registry_by_claim_id: Mapping[str, dict]) -> None:
    claim_id = row["claim_id"]
    if claim_id not in source_registry_by_claim_id:
        raise ReportabilityError(f"no source registry is bound for claim {claim_id}")
    claim_sources = source_registry_by_claim_id[claim_id]
    if not isinstance(claim_sources, Mapping):
        raise ReportabilityError(f"source registry for claim {claim_id} must be an object")
    required = {"target_sha256", "supplement_sha256_by_id", "cited_sha256_by_id"}
    if set(claim_sources) != required:
        raise ReportabilityError(f"source registry schema mismatch for claim {claim_id}")
    target_sha = claim_sources["target_sha256"]
    supplement_hashes = claim_sources["supplement_sha256_by_id"]
    cited_hashes = claim_sources["cited_sha256_by_id"]
    if not isinstance(target_sha, str) or not _SHA256.fullmatch(target_sha):
        raise ReportabilityError(f"invalid target-paper hash for claim {claim_id}")
    for label, registered in (("supplement", supplement_hashes), ("cited source", cited_hashes)):
        if not isinstance(registered, Mapping):
            raise ReportabilityError(f"registered {label} sources for claim {claim_id} must be a mapping")
        if any(
            not _nonempty(source_id) or not isinstance(digest, str) or not _SHA256.fullmatch(digest)
            for source_id, digest in registered.items()
        ):
            raise ReportabilityError(f"invalid registered {label} source for claim {claim_id}")

    status = row["status"]
    role = row["source_role"]
    source_id = row["source_id"]
    digest = row["source_file_sha256"]
    if status == "NOT_REPORTED":
        if role != "TARGET" or source_id or digest != target_sha:
            raise ReportabilityError("NOT_REPORTED must bind the claim's target paper")
    elif status == "REFERENCED":
        if role != "CITED_SOURCE" or not source_id or cited_hashes.get(source_id) != digest:
            raise ReportabilityError("REFERENCED must bind a registered cited source ID and hash")
    elif role == "TARGET":
        if source_id or digest != target_sha:
            raise ReportabilityError("TARGET source role must bind the claim's target paper")
    elif role == "SUPPLEMENT":
        if not source_id or supplement_hashes.get(source_id) != digest:
            raise ReportabilityError("SUPPLEMENT source role must bind a registered supplement ID and hash")
    else:
        raise ReportabilityError(f"source role {role!r} is not permitted for status {status}")


def _verify_source_files(rows: list[dict], source_paths_by_sha256: Mapping[str, Union[str, Path]]) -> None:
    if not isinstance(source_paths_by_sha256, Mapping):
        raise ReportabilityError("source_paths_by_sha256 must map declared hashes to pinned files")
    expected_hashes = {row["source_file_sha256"] for row in rows}
    for expected in expected_hashes:
        if not _SHA256.fullmatch(expected):
            raise ReportabilityError("source binding contains an invalid SHA-256 digest")
        if expected not in source_paths_by_sha256:
            raise ReportabilityError(f"no pinned file is bound for source SHA-256 {expected}")
        try:
            path = Path(source_paths_by_sha256[expected])
            if not path.is_file():
                raise ReportabilityError(f"bound source file is missing: {path}")
            digest = hashlib.sha256()
            with path.open("rb") as source_file:
                for chunk in iter(lambda: source_file.read(1024 * 1024), b""):
                    digest.update(chunk)
            actual = digest.hexdigest()
        except (OSError, TypeError, ValueError) as exc:
            raise ReportabilityError(f"cannot read bound source file for {expected}") from exc
        if actual != expected:
            raise ReportabilityError(f"bound source file hash mismatch for {expected}: got {actual}")


def _canonical_registry_sha256(source_registry_by_claim_id: Mapping[str, dict]) -> str:
    try:
        canonical = json.dumps(
            source_registry_by_claim_id,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ReportabilityError("source registry must be JSON-serializable") from exc
    return hashlib.sha256(canonical).hexdigest()


def summarize_reportability(
    claim_ids: Iterable[str],
    coders: tuple[str, str],
    rows: Iterable[dict],
    source_paths_by_sha256: Mapping[str, Union[str, Path]],
    source_registry_by_claim_id: Mapping[str, dict],
    expected_source_registry_sha256: str,
) -> dict:
    """Verify source bytes, validate a complete two-coder grid, and return descriptions."""
    if isinstance(claim_ids, (str, bytes)):
        raise ReportabilityError("claim_ids must be an iterable of claim identifiers, not a scalar string")
    try:
        claim_ids = tuple(claim_ids)
    except TypeError as exc:
        raise ReportabilityError("claim_ids must be an iterable of claim identifiers") from exc
    try:
        row_iter = iter(rows)
    except TypeError as exc:
        raise ReportabilityError("rows must be an iterable of row objects") from exc
    if not claim_ids or any(not _nonempty(claim_id) for claim_id in claim_ids):
        raise ReportabilityError("claim_ids must be a nonempty sequence of nonempty strings")
    if len(set(claim_ids)) != len(claim_ids):
        raise ReportabilityError("claim_ids contain duplicates")
    if not isinstance(source_registry_by_claim_id, Mapping):
        raise ReportabilityError("source_registry_by_claim_id must map claims to registered sources")
    if set(source_registry_by_claim_id) != set(claim_ids):
        raise ReportabilityError("source registry claim IDs must exactly match the sampled claims")
    if not isinstance(expected_source_registry_sha256, str) or not _SHA256.fullmatch(
        expected_source_registry_sha256
    ):
        raise ReportabilityError("expected source registry SHA-256 must be lowercase hexadecimal")
    actual_registry_sha256 = _canonical_registry_sha256(source_registry_by_claim_id)
    if actual_registry_sha256 != expected_source_registry_sha256:
        raise ReportabilityError("source registry hash does not match the owner-bound digest")
    if (
        not isinstance(coders, tuple)
        or len(coders) != 2
        or any(not _nonempty(coder) or coder == "ADJUDICATED" for coder in coders)
        or coders[0] == coders[1]
    ):
        raise ReportabilityError("exactly two distinct named coders are required")

    claim_set = set(claim_ids)
    keyed: dict[tuple[str, str, str], dict[str, dict]] = defaultdict(dict)
    for row in row_iter:
        _validate_row(row, claim_set, coders, source_registry_by_claim_id)
        key = (row["claim_id"], row["transition"], row["item_id"])
        coder = row["coder"]
        if coder in keyed[key]:
            raise ReportabilityError(f"duplicate row for {key} / {coder}")
        keyed[key][coder] = row

    expected = {
        (claim_id, ITEM_TRANSITION[item_id], item_id)
        for claim_id in claim_ids
        for item_id in ITEM_TRANSITION
    }
    if set(keyed) != expected:
        missing = sorted(expected - set(keyed))
        extra = sorted(set(keyed) - expected)
        raise ReportabilityError(f"incomplete claim/item grid: missing={missing}, extra={extra}")

    for key, rowset in keyed.items():
        if set(rowset) not in (set(coders), set(coders) | {"ADJUDICATED"}):
            raise ReportabilityError(f"missing independent coder row for {key}")
        left, right = (rowset[coder] for coder in coders)
        adjudicated = rowset.get("ADJUDICATED")
        if left["status"] != right["status"] and adjudicated is None:
            raise ReportabilityError(f"status disagreement lacks adjudication for {key}")
        if left["status"] == right["status"] and adjudicated is not None:
            raise ReportabilityError(f"unneeded adjudication row for agreeing statuses: {key}")
    validated_rows = [row for rowset in keyed.values() for row in rowset.values()]
    _verify_source_files(validated_rows, source_paths_by_sha256)

    raw_counts = {coder: {item: Counter({s: 0 for s in STATUSES}) for item in ITEM_TRANSITION} for coder in coders}
    final_counts = {item: Counter({s: 0 for s in STATUSES}) for item in ITEM_TRANSITION}
    disagreements = Counter({item: 0 for item in ITEM_TRANSITION})
    denominators = {item: len(claim_ids) for item in ITEM_TRANSITION}
    complete_counts = Counter({item: 0 for item in ITEM_TRANSITION})

    for key, rowset in keyed.items():
        claim_id, transition, item_id = key
        if set(rowset) not in (set(coders), set(coders) | {"ADJUDICATED"}):
            raise ReportabilityError(f"missing independent coder row for {key}")
        left, right = (rowset[coder] for coder in coders)
        for coder, row in ((coders[0], left), (coders[1], right)):
            raw_counts[coder][item_id][row["status"]] += 1
        differs = left["status"] != right["status"]
        adjudicated = rowset.get("ADJUDICATED")
        if differs and adjudicated is None:
            raise ReportabilityError(f"status disagreement lacks adjudication for {key}")
        if not differs and adjudicated is not None:
            raise ReportabilityError(f"unneeded adjudication row for agreeing statuses: {key}")
        if differs:
            disagreements[item_id] += 1
            final_status = adjudicated["status"]
        else:
            final_status = left["status"]
        final_counts[item_id][final_status] += 1
        if final_status == "REPORTED" or (final_status == "REFERENCED" and item_id in REFERENCE_ALLOWED):
            complete_counts[item_id] += 1

    result = {
        "claim_count": len(claim_ids),
        "source_registry_sha256": actual_registry_sha256,
        "item_ids": tuple(ITEM_TRANSITION),
        "raw_counts_by_coder": {
            coder: {item: dict(counts) for item, counts in by_item.items()}
            for coder, by_item in raw_counts.items()
        },
        "post_adjudication_counts": {
            item: dict(counts) for item, counts in final_counts.items()
        },
        "complete_count_by_item": dict(complete_counts),
        "denominator_by_item": denominators,
        "disagreement_by_item": {
            item: {"numerator": disagreements[item], "denominator": denominators[item]}
            for item in ITEM_TRANSITION
        },
    }
    return result

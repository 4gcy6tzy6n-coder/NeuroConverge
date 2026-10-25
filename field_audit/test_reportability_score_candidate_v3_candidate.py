import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

from reportability_score_candidate_v3_candidate import (
    ITEM_TRANSITION,
    ReportabilityError,
    summarize_reportability,
)


CODERS = ("coder_a", "coder_b")
SOURCE_BYTES = b"synthetic pinned source"
SHA = hashlib.sha256(SOURCE_BYTES).hexdigest()
CITED_BYTES = b"synthetic registered cited source"
CITED_SHA = hashlib.sha256(CITED_BYTES).hexdigest()


def row(claim_id, coder, item_id, status="REPORTED", **updates):
    result = {
        "claim_id": claim_id,
        "coder": coder,
        "transition": ITEM_TRANSITION[item_id],
        "item_id": item_id,
        "status": status,
        "evidence_pointer": (
            "target_locator=page=2;paragraph=3;cited_source_id=citation-1"
            if status == "REFERENCED"
            else "paper p. 2, paragraph 3"
        ),
        "source_file_sha256": CITED_SHA if status == "REFERENCED" else SHA,
        "source_role": "CITED_SOURCE" if status == "REFERENCED" else "TARGET",
        "source_id": "citation-1" if status == "REFERENCED" else "",
        "source_locator": "page=2;paragraph=3",
        "note": "",
        "adjudicator": "",
        "adjudication_date": "",
        "adjudication_rationale": "",
        "adjudication_source_pointer": "",
    }
    result.update(updates)
    return result


def complete_rows(claim_id="C1"):
    return [row(claim_id, coder, item) for item in ITEM_TRANSITION for coder in CODERS]


def adjudication_row(claim_id, item_id, status="REPORTED"):
    return row(
        claim_id,
        "ADJUDICATED",
        item_id,
        status,
        note="adjudication record",
        adjudicator="reviewer_1",
        adjudication_date="2026-10-19",
        adjudication_rationale="Reviewed both coder records and the pinned source.",
        adjudication_source_pointer="review note section 1",
    )


class ReportabilityCandidateTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.source_path = Path(self.temp_dir.name) / "paper.txt"
        self.source_path.write_bytes(SOURCE_BYTES)
        self.cited_path = Path(self.temp_dir.name) / "cited.txt"
        self.cited_path.write_bytes(CITED_BYTES)

    def tearDown(self):
        self.temp_dir.cleanup()

    def score(self, claim_ids, rows):
        ids = tuple(claim_ids) if not isinstance(claim_ids, str) else ("C", "1")
        registry = self.registry(ids)
        return summarize_reportability(
            claim_ids,
            CODERS,
            rows,
            {SHA: self.source_path, CITED_SHA: self.cited_path},
            registry,
            self.registry_hash(registry),
        )

    @staticmethod
    def registry(claim_ids=("C1",)):
        return {
            claim_id: {
                "target_sha256": SHA,
                "supplement_sha256_by_id": {},
                "cited_sha256_by_id": {"citation-1": CITED_SHA},
            }
            for claim_id in claim_ids
        }

    @staticmethod
    def registry_hash(registry):
        canonical = json.dumps(registry, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        return hashlib.sha256(canonical).hexdigest()

    def test_complete_grid_emits_itemwise_descriptions(self):
        result = self.score(["C1"], complete_rows())
        self.assertEqual(result["claim_count"], 1)
        self.assertEqual(result["complete_count_by_item"]["T1-01"], 1)
        self.assertEqual(result["denominator_by_item"]["T1-01"], 1)
        self.assertEqual(result["disagreement_by_item"]["T1-01"], {"numerator": 0, "denominator": 1})

    def test_each_status_and_permitted_reference_are_preserved(self):
        rows = []
        chosen = {"T1-01": "PARTIAL", "T1-02": "NOT_REPORTED", "T1-03": "REFERENCED"}
        for item_id in ITEM_TRANSITION:
            status = chosen.get(item_id, "REPORTED")
            note = "missing element" if status == "PARTIAL" else "searched section 2" if status == "NOT_REPORTED" else ""
            for coder in CODERS:
                rows.append(row("C1", coder, item_id, status, note=note))
        result = self.score(["C1"], rows)
        self.assertEqual(result["post_adjudication_counts"]["T1-03"]["REFERENCED"], 1)
        self.assertEqual(result["complete_count_by_item"]["T1-03"], 1)
        self.assertEqual(result["complete_count_by_item"]["T1-01"], 0)
        self.assertEqual(result["complete_count_by_item"]["T1-02"], 0)

    def test_reference_is_rejected_for_nonpermitted_item(self):
        rows = complete_rows()
        rows[0] = row("C1", CODERS[0], "T2-01", "REFERENCED")
        with self.assertRaisesRegex(ReportabilityError, "not permitted"):
            self.score(["C1"], rows)

    def test_missing_and_duplicate_independent_rows_fail_closed(self):
        rows = complete_rows()
        with self.assertRaisesRegex(ReportabilityError, "missing independent coder row"):
            self.score(["C1"], rows[:-1])
        with self.assertRaisesRegex(ReportabilityError, "duplicate row"):
            self.score(["C1"], rows + [rows[0]])

    def test_status_disagreement_requires_adjudication_and_keeps_raw_counts(self):
        rows = complete_rows()
        rows[0] = row("C1", CODERS[0], "T1-01", "REPORTED")
        rows[1] = row("C1", CODERS[1], "T1-01", "PARTIAL", note="missing comparator")
        with self.assertRaisesRegex(ReportabilityError, "lacks adjudication"):
            self.score(["C1"], rows)

        adjudicated = adjudication_row("C1", "T1-01", "NOT_REPORTED")
        adjudicated["note"] = "required comparison is absent"
        adjudicated["adjudication_rationale"] = "Neither coder found a reported comparator."
        adjudicated["adjudication_source_pointer"] = "paper p. 3, Methods search"
        result = self.score(["C1"], rows + [adjudicated])
        self.assertEqual(result["raw_counts_by_coder"][CODERS[0]]["T1-01"]["REPORTED"], 1)
        self.assertEqual(result["raw_counts_by_coder"][CODERS[1]]["T1-01"]["PARTIAL"], 1)
        self.assertEqual(result["post_adjudication_counts"]["T1-01"]["NOT_REPORTED"], 1)
        self.assertEqual(result["disagreement_by_item"]["T1-01"], {"numerator": 1, "denominator": 1})

    def test_invalid_adjudication_grid_fails_before_source_access(self):
        rows = complete_rows()
        rows[0] = row("C1", CODERS[0], "T1-01", "REPORTED")
        rows[1] = row("C1", CODERS[1], "T1-01", "PARTIAL", note="missing comparator")
        with self.assertRaisesRegex(ReportabilityError, "lacks adjudication"):
            registry = self.registry()
            summarize_reportability(["C1"], CODERS, rows, {}, registry, self.registry_hash(registry))

    def test_unneeded_or_incomplete_adjudication_fails(self):
        rows = complete_rows()
        adjudicated = adjudication_row("C1", "T1-01")
        with self.assertRaisesRegex(ReportabilityError, "unneeded adjudication"):
            self.score(["C1"], rows + [adjudicated])

        rows[0] = row("C1", CODERS[0], "T1-01", "REPORTED")
        rows[1] = row("C1", CODERS[1], "T1-01", "PARTIAL", note="missing element")
        adjudicated = row("C1", "ADJUDICATED", "T1-01", adjudicator="reviewer_1")
        with self.assertRaisesRegex(ReportabilityError, "require adjudicator"):
            self.score(["C1"], rows + [adjudicated])

    def test_adjudication_date_requires_exact_calendar_format(self):
        rows = complete_rows()
        rows[0] = row("C1", CODERS[0], "T1-01", "REPORTED")
        rows[1] = row("C1", CODERS[1], "T1-01", "PARTIAL", note="missing element")
        for date_value in ("2026-W43-2", "20261020", "2026-02-30", "0000-01-01"):
            adjudicated = adjudication_row("C1", "T1-01", "NOT_REPORTED")
            adjudicated["note"] = "required comparison is absent"
            adjudicated["adjudication_date"] = date_value
            adjudicated["adjudication_source_pointer"] = "paper p. 3, Methods search"
            with self.subTest(date_value=date_value):
                with self.assertRaisesRegex(ReportabilityError, "ISO YYYY-MM-DD"):
                    self.score(["C1"], rows + [adjudicated])

    def test_invalid_hash_and_unhashable_item_id_are_named_errors(self):
        rows = complete_rows()
        rows[0]["source_file_sha256"] = "not-a-hash"
        with self.assertRaisesRegex(ReportabilityError, "SHA-256"):
            self.score(["C1"], rows)

        rows = complete_rows()
        rows[0]["item_id"] = []
        with self.assertRaisesRegex(ReportabilityError, "item_id and transition"):
            self.score(["C1"], rows)

    def test_nonreported_and_partial_rows_need_reasons(self):
        rows = complete_rows()
        rows[0] = row("C1", CODERS[0], "T1-01", "PARTIAL")
        with self.assertRaisesRegex(ReportabilityError, "require a specific note"):
            self.score(["C1"], rows)

    def test_noniterable_inputs_fail_with_named_errors(self):
        with self.assertRaisesRegex(ReportabilityError, "claim_ids must be an iterable"):
            registry = self.registry()
            summarize_reportability(None, CODERS, [], {}, registry, self.registry_hash(registry))
        with self.assertRaisesRegex(ReportabilityError, "rows must be an iterable"):
            registry = self.registry()
            summarize_reportability(["C1"], CODERS, None, {}, registry, self.registry_hash(registry))
        with self.assertRaisesRegex(ReportabilityError, "rows must be an iterable"):
            registry = self.registry()
            summarize_reportability(["C1"], CODERS, 7, {}, registry, self.registry_hash(registry))

    def test_scalar_claim_id_string_is_not_split_into_characters(self):
        rows = complete_rows("C") + complete_rows("1")
        with self.assertRaisesRegex(ReportabilityError, "claim identifiers, not a scalar string"):
            self.score("C1", rows)

    def test_row_fields_must_be_strings(self):
        rows = complete_rows()
        rows[0]["note"] = ["silently malformed"]
        with self.assertRaisesRegex(ReportabilityError, "row fields must be strings"):
            self.score(["C1"], rows)

    def test_nonstring_extra_row_keys_fail_with_named_schema_error(self):
        rows = complete_rows()
        rows[0][1] = "unexpected numeric key"
        rows[0]["z_extra"] = "unexpected text key"
        with self.assertRaisesRegex(ReportabilityError, "row keys must be strings"):
            self.score(["C1"], rows)

        rows = complete_rows()
        rows[0]["adjudication_date"] = None
        with self.assertRaisesRegex(ReportabilityError, "row fields must be strings"):
            self.score(["C1"], rows)

    def test_declared_source_hash_must_match_pinned_bytes(self):
        rows = complete_rows()
        with self.assertRaisesRegex(ReportabilityError, "no pinned file is bound"):
            registry = self.registry()
            summarize_reportability(["C1"], CODERS, rows, {}, registry, self.registry_hash(registry))

        self.source_path.write_bytes(b"changed after pinning")
        with self.assertRaisesRegex(ReportabilityError, "hash mismatch"):
            self.score(["C1"], rows)

    def test_source_bytes_are_verified_before_summary_counts(self):
        rows = complete_rows()
        self.source_path.write_bytes(b"changed after pinning")
        registry = self.registry()
        with mock.patch(
            "reportability_score_candidate_v3_candidate.Counter",
            side_effect=AssertionError("summary counts computed before source verification"),
        ):
            with self.assertRaisesRegex(ReportabilityError, "hash mismatch"):
                summarize_reportability(
                    ["C1"], CODERS, rows,
                    {SHA: self.source_path, CITED_SHA: self.cited_path},
                    registry, self.registry_hash(registry),
                )

    def test_wrong_claim_target_hash_is_rejected_even_when_locally_pinned(self):
        other_bytes = b"another locally pinned paper"
        other_hash = hashlib.sha256(other_bytes).hexdigest()
        other_path = Path(self.temp_dir.name) / "other.txt"
        other_path.write_bytes(other_bytes)
        rows = complete_rows()
        rows[0]["source_file_sha256"] = other_hash
        with self.assertRaisesRegex(ReportabilityError, "TARGET source role"):
            summarize_reportability(
                ["C1"], CODERS, rows,
                {SHA: self.source_path, CITED_SHA: self.cited_path, other_hash: other_path},
                self.registry(),
                self.registry_hash(self.registry()),
            )

    def test_unregistered_supplement_hash_is_rejected(self):
        other_bytes = b"unregistered supplement"
        other_hash = hashlib.sha256(other_bytes).hexdigest()
        other_path = Path(self.temp_dir.name) / "supplement.txt"
        other_path.write_bytes(other_bytes)
        rows = complete_rows()
        rows[0].update(source_role="SUPPLEMENT", source_id="supp-1", source_file_sha256=other_hash)
        with self.assertRaisesRegex(ReportabilityError, "registered supplement"):
            summarize_reportability(
                ["C1"], CODERS, rows,
                {SHA: self.source_path, CITED_SHA: self.cited_path, other_hash: other_path},
                self.registry(),
                self.registry_hash(self.registry()),
            )

    def test_registered_supplement_hash_is_accepted(self):
        supplement_bytes = b"registered supplement"
        supplement_hash = hashlib.sha256(supplement_bytes).hexdigest()
        supplement_path = Path(self.temp_dir.name) / "registered-supplement.txt"
        supplement_path.write_bytes(supplement_bytes)
        rows = complete_rows()
        rows[0].update(
            source_role="SUPPLEMENT",
            source_id="supp-1",
            source_file_sha256=supplement_hash,
        )
        registry = self.registry()
        registry["C1"]["supplement_sha256_by_id"]["supp-1"] = supplement_hash
        result = summarize_reportability(
            ["C1"], CODERS, rows,
            {SHA: self.source_path, CITED_SHA: self.cited_path, supplement_hash: supplement_path},
            registry,
            self.registry_hash(registry),
        )
        self.assertEqual(result["complete_count_by_item"]["T1-01"], 1)

    def test_source_registry_claim_ids_must_match_sampled_claims(self):
        with self.assertRaisesRegex(ReportabilityError, "exactly match"):
            summarize_reportability(
                ["C1"], CODERS, complete_rows(),
                {SHA: self.source_path, CITED_SHA: self.cited_path},
                self.registry(("C2",)),
                self.registry_hash(self.registry(("C2",))),
            )

    def test_source_registry_must_match_owner_bound_digest(self):
        registry = self.registry()
        expected = self.registry_hash(registry)
        registry["C1"]["target_sha256"] = CITED_SHA
        with self.assertRaisesRegex(ReportabilityError, "owner-bound digest"):
            summarize_reportability(
                ["C1"], CODERS, complete_rows(),
                {SHA: self.source_path, CITED_SHA: self.cited_path},
                registry,
                expected,
            )

    def test_unregistered_cited_source_id_is_rejected(self):
        rows = complete_rows()
        cited_row = next(r for r in rows if r["item_id"] == "T1-03" and r["coder"] == CODERS[0])
        cited_row.update(
            status="REFERENCED",
            source_role="CITED_SOURCE",
            source_id="unregistered",
            source_file_sha256=CITED_SHA,
        )
        with self.assertRaisesRegex(ReportabilityError, "registered cited source"):
            self.score(["C1"], rows)

    def test_referenced_pointer_must_bind_target_citation_location_and_source_id(self):
        invalid_pointers = (
            "paper p. 2, paragraph 3",
            "target_locator=page=2;paragraph=3;cited_source_id=other-id",
            "target_locator=;cited_source_id=citation-1",
        )
        for pointer in invalid_pointers:
            rows = complete_rows()
            for cited_row in rows:
                if cited_row["item_id"] == "T1-03":
                    cited_row.update(
                        status="REFERENCED",
                        source_role="CITED_SOURCE",
                        source_id="citation-1",
                        source_file_sha256=CITED_SHA,
                        evidence_pointer=pointer,
                    )
            with self.subTest(pointer=pointer):
                with self.assertRaisesRegex(ReportabilityError, "target citation location and registered source ID"):
                    self.score(["C1"], rows)

    def test_not_reported_must_bind_target_paper_not_other_valid_source(self):
        other_bytes = b"another locally pinned paper"
        other_hash = hashlib.sha256(other_bytes).hexdigest()
        other_path = Path(self.temp_dir.name) / "other.txt"
        other_path.write_bytes(other_bytes)
        rows = complete_rows()
        rows[0].update(status="NOT_REPORTED", note="searched target methods", source_file_sha256=other_hash)
        with self.assertRaisesRegex(ReportabilityError, "NOT_REPORTED must bind"):
            summarize_reportability(
                ["C1"], CODERS, rows,
                {SHA: self.source_path, CITED_SHA: self.cited_path, other_hash: other_path},
                self.registry(),
                self.registry_hash(self.registry()),
            )


if __name__ == "__main__":
    unittest.main()

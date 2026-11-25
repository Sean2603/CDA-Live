#!/usr/bin/env python3
"""Assert-based self-test for the publication gates in validate_content.py. Run: python tool/test_publication_gates.py"""
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_content as v


def bands(*pairs, escalations=None):
    doc = {"results": [{"id": f"r{i}", "minimumScore": a, "maximumScore": b} for i, (a, b) in enumerate(pairs)]}
    if escalations:
        doc["escalations"] = escalations
    errs = []
    v.validate_result_bands(doc, "t", errs)
    return errs


assert bands((0, 2), (3, 4)) == []
assert any("overlaps" in e for e in bands((0, 3), (3, 4)))  # overlap rejected
assert bands((0, 3), (3, 4), escalations=[{"id": "e"}]) == []  # overlap allowed with escalations
assert any("gap" in e for e in bands((0.0, 2.5), (2.7, 4.0)))  # decimal gap rejected (step 0.1)
assert bands((0.0, 2.5), (2.6, 4.0)) == []
assert any("gap" in e for e in bands((0, 2), (4, 5)))  # whole-number gap rejected


def notice(**kw):
    n = {"id": "n", "effectiveFrom": None, "expiresOn": None, "affectedContentType": None, "affectedContentId": None, **kw}
    errs = []
    v.validate_notice_gates(n, "t", {"scoring-tool": {"centor": {}}}, errs)
    return errs


assert any("before" in e for e in notice(effectiveFrom="2026-02-01T00:00:00Z", expiresOn="2026-01-01T00:00:00Z"))
assert notice(effectiveFrom="2026-01-01T00:00:00Z", expiresOn="2026-02-01T00:00:00Z") == []
assert any("required" in e for e in notice(affectedContentType="scoring-tool"))
assert any("does not match" in e for e in notice(affectedContentType="scoring-tool", affectedContentId="nope"))
assert notice(affectedContentType="scoring-tool", affectedContentId="centor") == []

assert v.parse_rfc3339("2026-13-45T00:00:00Z") is None
assert v.parse_rfc3339("2026-02-30T00:00:00Z") is None
assert v.parse_rfc3339("2026-02-01T00:00:00") is None  # offset required
assert v.parse_rfc3339("2026-02-01T10:00:00+01:00") is not None
assert not v.is_calendar_date("2026-02-30") and not v.is_calendar_date("20260230") and v.is_calendar_date("2026-02-28")

schema = v.ROOT / "schema" / "clinical-notices-schema.json"
errs = []
v.validate_date_fields({"notices": [{"expiresOn": "2026-13-45T00:00:00Z"}]}, schema, "t", errs)
assert errs, "nested bad date-time must be rejected"
errs = []
v.validate_date_fields({"notices": [{"expiresOn": "2026-12-01T00:00:00Z"}]}, schema, "t", errs)
assert not errs


def run_procedure(status):
    with tempfile.TemporaryDirectory() as d:
        (Path(d) / "x.json").write_text(json.dumps({"id": "x", "status": status}), encoding="utf-8")
        errs = []
        v.validate_collection("procedure", {**v.COLLECTIONS["procedure"], "directory": Path(d)}, set(), set(), errs)
        return errs


assert any("draft procedures" in e for e in run_procedure("draft"))
assert not any("draft procedures" in e for e in run_procedure("active"))

legacy = {"id": "a", "title": "t", "version": "1.0.0", "targetEnvironment": "prod",
          "features": [{"id": i, "state": "enabled"} for i in sorted(v.KNOWN_APP_FEATURE_IDS - {"procedures"})]}
with tempfile.TemporaryDirectory() as d:
    path = Path(d) / "f.json"
    path.write_text(json.dumps(legacy), encoding="utf-8")
    original = v.FEATURE_AVAILABILITY_PATH
    v.FEATURE_AVAILABILITY_PATH = path
    errs = []
    v.validate_app_feature_availability(errs)
    v.FEATURE_AVAILABILITY_PATH = original
assert any("missing required feature ids: procedures" in e for e in errs), errs
print("publication gate self-test passed")

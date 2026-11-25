#!/usr/bin/env python3
"""Self-test for the reference review window (expiry = nextReviewDue)."""
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_references import review_window  # noqa: E402

DUE = date(2026, 12, 31)


def at(offset):
    return review_window(DUE, DUE + timedelta(days=offset))


assert at(-8) is None, "D-8: no message"
assert at(-7) and at(-7)[0] == "warning", "D-7 warns"
assert date(2026, 12, 24) == DUE - timedelta(days=7)
assert at(0) and at(0)[0] == "warning" and "expired" not in at(0)[1], "expiry day warns"
assert at(1) and at(1)[0] == "warning" and "expired" in at(1)[1], "D+1 warns expired"
assert at(89) and at(89)[0] == "warning", "D+89 warns, not an error"
assert at(90) and at(90)[0] == "error", "D+90 is a publish block"
assert date(2027, 3, 31) == DUE + timedelta(days=90)
assert "more than 90 days past its review date" in at(90)[1]
assert review_window(None, DUE) is None, "no due date: no message"
# Non-current statuses never reach review_window (caller gates on "current").
print("test_reference_review_window: all passed")

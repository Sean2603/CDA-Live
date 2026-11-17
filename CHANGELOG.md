# Changelog

## 2026-11-17 — Attachment folder rule relaxed

- `tool/validate_content.py` no longer requires `attachments/<content-kind>/` (for example `attachments/blood_panels/`). Attachments may sit in any lowercase category or content-kind folder under `attachments/`, matching how CDM stores them (`attachments/<category>/...`). Schemas are unchanged (they already require only the `attachments/` prefix). Path-escape, extension, existence and SHA-256 checks are unchanged.
- Companion CDM entry: attachment paths built from category folders are now accepted by full-repository validation.

## 2026-11-12 — Formal content reset

**Clinical Decision Assessments (CDA) reset to 0.0.1.**

- All content starts again at version 0.0.1. Earlier version numbers from the archived `clinical-decision-assessments` repository do not apply.
- The repository restart entry below previously recorded 0.1.0. That was corrected to 0.0.1.
- README updated: version, naming (CDA = Clinical Decision Assessments; CDM is the backend; App is the iOS/Android app), and the rule that content is published only through CDM.
- Added `CLAUDE.md`: content is never committed from chat; tooling and schema changes are committed only when requested.

Content reset to `0.0.1`.

## 2026-11-09 — Repository restarted

- New repository `CDA-Live` replaces the archived `clinical-decision-assessments`.
- Content restarts at version 0.0.1 (corrected from 0.1.0 on 2026-11-12). No content has been published yet.
- Initial structure: empty content folders (including prescribing care-setting folders), schemas and validation tools.
- Added README and this changelog.

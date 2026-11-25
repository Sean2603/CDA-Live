# Changelog

## 2026-11-25 — Prescribing cross-file rules (tooling)

- `tool/validate_content.py` now enforces, for prescribing content: unique `rank` and unique `prescribingChoiceLabel` within a pathway; an explicit `relationship` when a choice has more than one component; no link to a `superseded` pathway (as well as `withdrawn`); no `withdrawn` medicine in an `active` pathway; every pathway component has a matching indication regimen in the medicine (backlink); a medicine's `ageGroup` matches a choice of its pathway; at most one active pathway per condition and care setting.
- Schemas unchanged. Companion CDM change: the same rules in `src/lib/content-validation.ts` and `src/lib/prescribing-cross-links.ts` (see CROSS-REPO.md XR-016).

## 2026-11-25 — ageGroup accepts both

- `schema/medication-schema.json` (`indicationRegimen`) and `schema/prescribing-schema.json` (pathway `regimen`): the `ageGroup` enum is now `"adult"`, `"child"` or `"both"`. `validate_content.py` validates through the schemas, so no code change was needed.
- Content using `"both"` must wait for the App release that accepts it. Until then the app and CDM validators reject it (see CROSS-REPO.md). App ships first, then content.

## 2026-11-19 — Pathway regimens require ageGroup

- `schema/prescribing-schema.json`: each pathway `regimen` now has a required `ageGroup` field, either `"adult"` or `"child"`.
- Pathway regimens must set `ageGroup`. The CDM authoring editor must be updated before content is published. Breaking: the app ships first, then content that uses the field.

## 2026-11-19 — Medication regimens require ageGroup

- `schema/medication-schema.json`: each `indicationRegimen` now has a required `ageGroup` field, either `"adult"` or `"child"`. `population` is unchanged (free text).
- Published medication content must set `ageGroup` on every regimen. `validate_content.py` reports a missing or other value through the schema check.
- Breaking: the app update ships first, then content that uses the field. CDM validators and the app model must match (see CROSS-REPO.md).

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

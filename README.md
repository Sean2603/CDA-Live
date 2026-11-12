# CDA-Live

Clinical Decision Assessments (CDA) is the governed clinical content for the **Clinical Decision Support** app. The repository is CDA-Live. CDA was formally reset, and all content starts again at version 0.0.1.

This repository replaces the archived `clinical-decision-assessments` repository. Content is added one item at a time, each going through review and clinical validation before it can be published.

> **Content is authored, reviewed, validated and published through CDM Content Manager (the backend), never committed here from chat or edited by hand.** Direct commits are for tooling and schema changes only, when requested, and must be recorded in the changelog.

## Status

Empty. No content has been published yet. The folders, schemas and validation tools are in place.

## Folder structure

| Folder | Contents | Schema |
| --- | --- | --- |
| `assessments/` | Assessment guides (one JSON file per assessment) | `schema/assessment-schema.json` |
| `blood_panels/` | Blood panel interpretations and calculations | `schema/blood-panel-schema.json` |
| `guidelines/` | Clinical guidelines | `schema/guideline-schema.json` |
| `medications/` | Medication monographs | `schema/medication-schema.json` |
| `prescribing/` | Prescribing pathways, one subfolder per care setting (see below) | `schema/prescribing-schema.json` |
| `procedures/` | Skills and procedures | `schema/procedure-schema.json` |
| `scoring_tools/` | Scoring tools and calculators | `schema/scoring-tool-schema.json` |
| `shared_learning/` | Shared learning resources | `schema/shared-learning-schema.json` |
| `schema/` | JSON Schemas for every collection, plus reference, glossary, categories and app feature availability | — |
| `tool/` | Validation and manifest scripts | — |

Folders marked empty contain a `.gitkeep` file so Git keeps them.

### Prescribing care settings

Prescribing pathways are grouped by care setting, one folder each:

- `prescribing/primary-care/`
- `prescribing/bhsct/`
- `prescribing/nhsct/`
- `prescribing/sehsct/`
- `prescribing/shsct/`
- `prescribing/whsct/`

Each file's `careSetting` field must match its folder. The same condition across settings should share a `conditionId`.

## What each item needs

Every content file is one JSON object that validates against its schema in `schema/`. Common fields:

- `id`: a stable, lowercase identifier using letters, numbers, hyphens or underscores. It must not change once published.
- `title`
- `version`: semantic version (`MAJOR.MINOR.PATCH`). Versions only increase. A version number that has been published is never reused.
- `status`: `active`, `withdrawn` or `superseded` (where the schema allows it).
- `clinicalValidation`: whether a clinician has validated the item, with `reviewedBy`, `reviewedOn`, `reviewerRole` and `nextReviewDue`. The app shows this to users, so it must be recorded by the clinician who validated the content, never filled in by code.
- `references`, where the content cites sources. Every cited reference must exist in `references/references.json`.

Blood panels, scoring tools and assessments also have their own required structures; the schema for each is the authority.

## Publication and the manifest

`manifest.json` is generated, not written by hand. It lists every published item with its file path, schema path, SHA-256 hash, size and version, and it computes the minimum app version the content needs. The Flutter app downloads the content through this manifest.

It is regenerated when content is published through CDM. To regenerate it locally:

```bash
python tool/sync_manifest.py --write
python tool/validate_manifest_safety.py
python tool/sync_manifest.py --check
```

## Validation

Run these before committing:

```bash
python tool/validate_content.py
python tool/validate_references.py
python tool/validate_manifest_safety.py
python tool/sync_manifest.py --check
```

- `validate_content.py`: checks every item against its schema, plus attachment and cross-reference rules.
- `validate_references.py`: checks that every cited reference exists and is current.
- `validate_manifest_safety.py`: checks the manifest's update policy and emergency revocation controls.
- `sync_manifest.py --check`: checks that the manifest matches the content on disk.

## Adding content

1. Create the item in CDM and move it through review and clinical validation.
2. Publish it through CDM, which writes the file here and regenerates the manifest.
3. Check the validation commands above pass.

## Related repositories

- **CDM Content Manager** (`cdm-content-manager`): the backend where items are authored and governed. It publishes content here.
- **Clinical Decision App** (`clinical-decision-app`): the Flutter app for iOS and Android that downloads and displays this content.
- **clinical-decision-assessments** (archived): the previous content repository. Kept read-only for history; its version numbers do not apply here.

## Changelog

Changes to schemas, tools or the repository structure are recorded in `CHANGELOG.md`.

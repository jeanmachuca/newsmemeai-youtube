# Schemas

## Scope

This folder defines the serialization contracts for the package manifest and YouTube
metadata. Both are JSON documents. The manifest is the integrity boundary; metadata is
the future upload boundary.

## Normative Statements (RFC 2119)

- Every schema MUST be versioned with an integer `schema_version`.
- Every schema MUST declare JSON Schema 2020-12 as its serialization format.
- The manifest MUST list every required artifact with a SHA-256 digest and byte size.
- The manifest MUST NOT include itself in its own file list.
- `metadata.json` MUST keep `privacy_status` at `private` for v0.1.
- The validator MUST reject a manifest that lists an absolute path or a parent traversal.
- The validator MUST reject a package whose manifest omits, adds, or renames an artifact
  outside the seven-name contract.
- The validator MUST reject metadata that is not `privacy_status: private`,
  `made_for_kids: false`, `shorts: true`, and `category_id: "24"`.
- The validator MUST reject a manifest whose `review.status` is not `draft`.
- Future schema changes MUST preserve backward validation within the same major version.

## Manifest v1

File: [`manifest.schema.json`](manifest.schema.json)

| Field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `schema_version` | integer | yes | `1` |
| `generator` | object | yes | `name` and `version` |
| `style` | string | yes | `classic`, `reaction`, or `headline` |
| `headline` | object | yes | Source headline and feed provenance |
| `script` | object | yes | Hook, context, punchline, rationale, model, style |
| `review` | object | yes | `status`, `required`, `checklist` |
| `dimensions` | object | yes | Frame and thumbnail pixel dimensions |
| `files` | object | yes | Artifact name → `{sha256, bytes}` |

Rules:

1. `files` MUST contain exactly the seven required artifacts:
   `frame-01-hook.svg`, `frame-02-context.svg`, `frame-03-punchline.svg`,
   `thumbnail.svg`, `script.md`, `metadata.json`, and `REVIEW.md`.
2. `files` MUST NOT contain `manifest.json`.
3. A filename MUST be a relative POSIX path with no `..` segment.
4. A digest MUST be 64 lowercase hexadecimal characters.

## Metadata v1

File: [`metadata.schema.json`](metadata.schema.json)

| Field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `schema_version` | integer | yes | `1` |
| `title` | string | yes | YouTube title, ≤100 characters |
| `description` | string | yes | Description, ≤5000 characters |
| `tags` | array of strings | yes | Total budget ≤500 characters |
| `category_id` | string | yes | `24` (Entertainment) |
| `privacy_status` | string | yes | `private` in v0.1 |
| `made_for_kids` | boolean | yes | `false` |
| `shorts` | boolean | yes | `true` |

## Versioning

- A compatible field addition MAY bump the minor product version without changing
  `schema_version`.
- A breaking field change MUST increment `schema_version` and add an ADR.
- The validator MUST reject an unknown `schema_version`.

## Open Questions

- Should `manifest.json` be signed once a manual upload workflow exists?
- Should the metadata schema include a locale field before a second language is added?

## Change Log

| Date | Author | RFC 2119 level changed | Rationale |
| --- | --- | --- | --- |
| 2026-11-16 | Pilot | Initial | Manifest and metadata v1 contracts. |

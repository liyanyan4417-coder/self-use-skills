# Skill Package Repository

This workspace stores skills from draft to packaged release.

## Structure

- `skills/source/`: canonical editable skill folders.
- `skills/drafts/`: experimental or incomplete skills.
- `skills/review/`: skills waiting for validation before packaging.
- `packages/ready/`: packaged skill archives ready to distribute.
- `packages/archive/`: old package builds kept for reference.
- `releases/`: release notes and publishing records.
- `templates/skill/`: starter template for new skills.
- `docs/`: repository process notes.
- `scripts/`: local helper scripts for validation, packaging, or indexing.

## Recommended Flow

1. Create or update a skill in `skills/source/<skill-name>/`.
2. Move unfinished work to `skills/drafts/` when it is not ready for review.
3. Copy review candidates into `skills/review/` with a short changelog.
4. Package reviewed skills into `packages/ready/`.
5. Record each published version in `releases/`.

## Naming

Use lowercase kebab-case for skill folders and package files:

```text
skills/source/literature-review-writer/
packages/ready/literature-review-writer-1.0.0.zip
```


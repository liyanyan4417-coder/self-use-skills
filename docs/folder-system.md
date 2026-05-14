# Folder System

This repository separates working skill source from packaged artifacts.

## Skill Lifecycle

| Stage | Folder | Purpose |
| --- | --- | --- |
| Draft | `skills/drafts/` | Ideas, sketches, and incomplete skills. |
| Source | `skills/source/` | Maintained skill source of record. |
| Review | `skills/review/` | Candidate skills awaiting validation. |
| Packaged | `packages/ready/` | Versioned package files ready to share. |
| Archived | `packages/archive/` | Superseded package files. |
| Released | `releases/` | Notes and records for shipped versions. |

## Skill Folder Convention

Each skill should use this layout:

```text
skill-name/
  SKILL.md
  README.md
  assets/
  scripts/
  tests/
  metadata.json
```

Only `SKILL.md` is required for a minimal skill. Add the other folders when the skill needs assets, helpers, or tests.

## Package Convention

Package files should include the skill name and semantic version:

```text
packages/ready/skill-name-1.2.0.zip
```

Keep release notes in:

```text
releases/skill-name/1.2.0.md
```


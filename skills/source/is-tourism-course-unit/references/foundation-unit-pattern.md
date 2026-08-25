# Foundation Unit Pattern

Use this reference when building a foundational course unit for first-time IS learners, especially units like:

- IS foundations
- IT artifact
- design science basics
- IS problem recognition
- digital system / work system foundations

This pattern differs from applied paper-pair units.

## 1. Human Output Rule

For foundational units, keep human-readable DOCX outputs minimal:

```text
human-deliverables/docx/
├── unit-XX-teacher-course-outline.docx
└── unit-XX-teaching-content-activity-script.docx
```

Do not export every component as a separate DOCX unless the user explicitly asks.

Keep component materials as Markdown under `ai-source/` and research cards.

## 2. Two Main Documents

### Teacher Course Outline

Purpose: structure-first teacher reading.

Include:

1. Unit positioning.
2. Learning goals.
3. Teaching structure with 1-2-3 level headings.
4. Time allocation.
5. Literature and materials.
6. Unit outputs.
7. References.

### Teaching Content, Activity, and Script

Purpose: classroom execution.

Include:

1. Preparation.
2. Opening.
3. Part-by-part teaching content.
4. Teacher script.
5. Classroom interactions.
6. Scaffolded activity steps.
7. Reference diagram or board model.
8. Closing.
9. References.

## 3. Concept Before Definition

For difficult IS concepts, do not start with a formal definition.

Use:

```text
concept ladder
-> concept location
-> student confusion
-> literature-based unpacking
-> applied example
```

Example from Unit 01:

```text
Data
-> Information
-> Information Technology
-> IT Artifact
-> Information System
-> Use / Work / Organization / Value / Governance
```

In the first pass, IT artifact is only positioned. It is then unpacked through Orlikowski & Iacono (2001).

## 4. Literature Teaching Rule

Do not teach a paper by reproducing the paper's section order.

Reorganize the paper around student understanding:

```text
student's intuitive confusion
-> why the intuition is incomplete
-> what lenses the paper provides
-> which lens fits the unit
-> how the lens changes the tourism example
```

For Unit 01, Orlikowski & Iacono (2001) becomes:

```text
PMS: software, tool, or system?
-> IT disappears in IT research
-> nominal / tool / proxy / computational views as incomplete lenses
-> ensemble view as the target lens
-> five premises applied to PMS
```

## 5. Scaffolded Activity Rule

For first-time learners, do not start with independent system selection.

Use:

```text
teacher-led common case
-> shared reference diagram
-> student fills local details
-> teacher adds risks and governance
-> later units move toward independent analysis
```

For Unit 01:

```text
PMS artifact in ensemble reference diagram
```

This means:

```text
center = PMS artifact
surrounding layers = ensemble / work system needed to understand the artifact
whole diagram approximates an information system, but the teaching purpose is artifact-in-ensemble analysis
```

## 6. A/B/C/D Alignment Rule

Every major reference diagram should map to the course's four modules:

```text
A 数字系统与 IS 基础: system, artifact, modules, boundaries
B 人机使用、工作与体验: users, tasks, workflows, experience
C 数字商业、平台与旅游创新: platform links, transactions, revenue, value, innovation
D 数据、信任、治理与社会后果: data, rules, privacy, risk, responsibility, governance
```

Prefer full labels in diagrams:

```text
[B 人机使用、工作与体验：任务流程 / Workflows]
[D 数据、信任、治理与社会后果：数据 / Data]
[C 数字商业、平台与旅游创新：价值 / Value]
```

Put workflows before data and users when the teaching goal is to show how a system enters work:

```text
Workflows
-> Data
-> Users
-> Rules
-> Value
-> Risks & Governance
```

## 7. Validation Checklist

Before delivering:

1. DOCX folder contains only the intended human-facing outputs.
2. Markdown sources remain available for AI maintenance.
3. The paper is not merely summarized in article order.
4. The classroom activity is appropriately scaffolded.
5. Any reference diagram clearly distinguishes artifact, ensemble, and information system.
6. A/B/C/D mapping is explicit.
7. DOI and APA references are present where literature is used.

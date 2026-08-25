---
name: is-tourism-course-unit
description: Build reusable Information Systems-to-tourism course learning units and foundational IS teaching units. Use when the user asks to develop IS-Learning course units, process IS and tourism papers into teaching materials, create foundation units such as IS basics / IT artifact / design science, produce teacher course outlines, lecture scripts, activities, DOCX/PPT outputs, or preserve a repeatable teaching workflow. Especially use for local PDFs, DOI verification, Top 7 tourism journals, professional-master teaching outputs, A/B/C/D module alignment, and Unit 01-style foundation patterns.
---

# IS-Tourism Course Unit

## Overview

Create complete IS-to-tourism learning units and foundational IS teaching units. The unit must preserve the IS learning goal while making the tourism application teachable for professional master's students.

This skill is itself a design-science artifact for course development. When the user asks to improve the course-development method, read `references/design-science-skill-principles.md` and treat March & Smith (1995), Hevner et al. (2004), Peffers et al. (2007), and Gregor & Hevner (2013) as design logic for the skill, not merely as papers to summarize.

There are two supported unit types.

## Unit Types

### Type A: Applied Paper-Pair Unit

Use when the unit is built from one IS core paper and one tourism / hospitality counterpart paper.

The governing logic is:

```text
IS core paper
-> tourism application bridge
-> tourism counterpart paper
-> comparison, integration, reflection
-> teaching outputs
-> Personal IS Model update
```

### Type B: Foundation Concept Unit

Use when the unit teaches a foundational IS concept or method before students can independently analyze papers or systems.

Read `references/foundation-unit-pattern.md`.

The governing logic is:

```text
concept ladder
-> student confusion
-> core literature reorganized around understanding
-> teacher-led common case
-> reference diagram
-> A/B/C/D module alignment
-> two main human-facing DOCX outputs
```

## Non-Negotiable Rules

1. Read `LEARNING_OS.md` and `research/deep-reading/CARD_STRUCTURE.md` before changing the project structure.
2. Prefer full local PDF reading before judging any paper or learner summary. If the local PDF is invalid, mark it clearly and stop before making Deep Reading claims.
3. Verify or record DOI for every paper. If DOI cannot be verified, label it pending and do not invent it.
4. Analyze one paper at a time. Do not mix tourism application into the IS paper analysis before the IS paper card is complete.
5. For tourism counterparts, obey the user's journal scope. If the user says Top 7 only, use only: `Tourism Management`, `Annals of Tourism Research`, `Journal of Travel Research`, `International Journal of Hospitality Management`, `International Journal of Contemporary Hospitality Management`, `Journal of Hospitality & Tourism Research`, and `Journal of Sustainable Tourism`.
6. Keep cards bilingual when they are intended for teaching or sharing.
7. Mark human intervention honestly. If the learner has not provided a retrieval summary, do not pretend to evaluate it.
8. Every completed applied paper-pair unit must end with a reusable comparison, integration, reflection, and teaching discussion section.
9. For foundation units, do not force the IS-paper + tourism-paper closure. Use the foundation pattern and scaffolded classroom activity instead.
10. For human-readable DOCX outputs in foundation units, export only two main documents unless the user explicitly asks for more: teacher course outline; teaching content, activity, and script.
11. Keep component files as Markdown for AI maintenance, but avoid cluttering the DOCX folder.
12. Reorganize literature around student understanding, not around the article's section order.
13. For first-time learners, use teacher-led common-case diagrams before asking students to independently analyze systems.
14. Align major diagrams with A/B/C/D modules.
15. If a unit involves assigned or core papers, create a standalone student-facing literature understanding material in both Markdown source and DOCX output.
16. For skill or workflow improvement tasks, separate the design artifact, design process, evaluation logic, boundary conditions, and transferable knowledge value. Do not frame the output only as paper theoretical contribution.

## Workflow

### Step 1: Locate Inputs

- Locate the project root, usually `IS-Learning/`.
- Find the local PDFs under `research/deep-reading/papers/`.
- Identify existing cards under `research/deep-reading/cards/`.
- Identify the target unit file under `research/deep-reading/units/`.

### Step 2: Read Full Text

For each paper:

1. Inspect PDF metadata and page count where possible.
2. Extract full text into `work/`.
3. Read abstract, introduction, theory, method, findings, discussion, implications, limitations, and appendices when relevant.
4. Record PDF status in the card.

### Step 3: Build Paper Cards

Use the card template in `references/paper-card-template.md`.

Each card should include:

- metadata and DOI
- local PDF path and PDF status
- human retrieval summary assessment
- research question
- theory
- concepts
- relationship model
- evidence
- findings
- theoretical contribution
- management practice
- application to the learning unit
- limitations
- Personal IS Model update
- retrieval questions
- human intervention needed
- APA reference

### Step 4: Build Or Update The Learning Unit

If this is an applied paper-pair unit, use `references/unit-template.md`.

If this is a foundation concept unit, use `references/foundation-unit-pattern.md`.

Applied paper-pair units must include:

- IS problem
- IS core paper
- tourism application bridge
- tourism counterpart paper
- comparison table
- integrated model
- reflection
- teaching discussion
- human intervention needed

Foundation units must include:

- teacher course outline
- teaching content, activity, and script
- concept ladder
- core literature reorganized for student understanding
- scaffolded activity
- reference diagram or board model
- A/B/C/D alignment
- human intervention needed

### Step 5: Create Teaching Outputs

For applied paper-pair units, use `references/teaching-output-checklist.md`.

For foundation units, use `references/foundation-unit-pattern.md` and export only:

```text
human-deliverables/docx/unit-XX-teacher-course-outline.docx
human-deliverables/docx/unit-XX-teaching-content-activity-script.docx
```

For applied paper-pair units, create at minimum:

- course PPTX
- lecture script Markdown
- lecture script DOCX
- student handout Markdown
- comparison / discussion Markdown

For PPT:

- Keep the first screen as the usable teaching deck, not a marketing page.
- Use the project's existing visual style if a prior unit deck exists.
- Put navigation at the top if that is the established course style.
- Keep visible slide text audience-facing and concise.
- Add speaker notes with source blocks.
- Render and check slides before delivery.

For DOCX:

- Render or QuickLook-check if possible.
- If LibreOffice cannot display CJK fonts but QuickLook works, state that distinction.

### Step 6: Update Project Memory

Update:

- `research/deep-reading/queue.md`
- `research/deep-reading/units/README.md`
- target unit file status
- relevant output indexes if present

## Output Standard

The final response should tell the user:

- what was completed
- where the files are
- what was verified
- what still needs human intervention

Do not over-explain implementation details. The user needs a usable course unit, not a build log.

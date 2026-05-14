---
name: literature-review-writer
description: Use when writing, outlining, revising, or prompting an AI to draft the Literature Review / Theoretical Background / Concept Definition / Hypotheses Development sections of empirical journal papers, especially when the user wants a theory-concept-relationship structure and may provide sources through a NotebookLM notebook.
---

# Literature Review Writer

Use this skill to write or guide the writing of empirical journal-paper literature reviews using a **theory -> concept -> relationship** structure. Prefer this skill when the user asks for 文献综述, Literature Review, Theoretical Background, 概念界定, Hypotheses Development, hypothesis writing, or wants AI to write from uploaded literature.

## Core Principle

Do not organize the review as a timeline or author-by-author list. Build a logical chain:

1. **Theory**: what explanatory lens frames the problem?
2. **Concepts**: what constructs are being defined, distinguished, or reconstructed?
3. **Relationships**: why should variables relate as hypothesized?

The final review should justify why the current study must exist.

## NotebookLM-First Workflow

If the user says the literature is in NotebookLM, or references a registered NotebookLM notebook:

1. Use the NotebookLM tool to query the relevant notebook before drafting.
2. Ask NotebookLM for structured evidence, not polished prose. Request: key theories, concept definitions, variable relationships, agreements, contradictions, gaps, methods, and representative citations.
3. If the notebook is ambiguous, search/list notebooks or ask the user for the notebook URL/name.
4. Preserve source-grounded claims. If evidence is thin, say what literature is missing instead of inventing support.
5. Then draft using the framework below.

Suggested NotebookLM question:

```text
请基于笔记本中的文献，为我的核心期刊实证论文整理 Literature Review 写作材料。请按以下结构输出：
1. 可用理论及核心假设；
2. 核心概念/构念的定义、维度、测量方式与争议；
3. 变量关系的已有发现，包括一致结论、矛盾结论、中介机制、调节条件；
4. 现有研究不足：理论不足、概念模糊、机制不清、情境边界、方法局限；
5. 可支持每个观点/假设的代表性文献，必须给出作者、年份，并尽可能给出完整 APA 参考文献信息。
请不要写成正文，先输出结构化证据。
```

## Citation Rules

When drafting from literature, citations are part of the output by default unless the user explicitly asks for no citations.

- Use APA-style in-text citations for claims derived from literature, e.g. `(Dovidio et al., 2006)` or `Dovidio et al. (2006)`.
- Every conceptual definition, theory claim, empirical finding, research gap, or methodological limitation should have a nearby citation.
- Do not put citations only at the end of a paragraph if the paragraph contains multiple source-dependent claims from different studies.
- If NotebookLM reports a source as cited inside another source, use secondary citation format, e.g. `(Penner et al., 2005, as cited in Cai et al., 2025)`.
- Include a **References** section after the draft using APA style as completely as the available source data allows.
- If NotebookLM does not provide complete bibliographic fields, list the available author, year, title/source name, and mark missing fields with a concise note such as `[journal details unavailable in notebook]`.
- Never invent authors, years, titles, journals, volumes, DOIs, or page ranges. If uncertain, say the reference needs verification.
- If the user's citation style differs from APA, follow the user's requested style instead.

## Writing Structure

For ordinary empirical journal papers, use:

```text
2. Literature Review and Hypotheses Development
2.1 Theoretical Background
2.2 Concept Definition / Key Constructs
2.3 Hypotheses Development
```

If there are multiple hypotheses:

```text
2.3 Independent Variable and Dependent Variable
2.4 Mediating Mechanism
2.5 Moderating Mechanism
2.6 Moderated Mediation / Boundary Condition
```

## Module Guidance

### 1. Theoretical Background

Goal: introduce the guiding theory, its assumptions, prior use, and the tension it leaves unresolved in the current context.

Paragraph pattern:

1. Introduce the theory and its core assumptions.
2. Summarize how prior studies used it in related domains.
3. Identify theory-context tension or an explanatory blind spot.
4. State how the current study extends or refines the theory.

Avoid: generic theory summaries, decorative theory name-dropping, or stacking multiple theories without explaining their roles.

### 2. Concept Definition / Key Constructs

Goal: define the constructs as research objects, compare existing definitions, clarify boundaries, and state the paper's adopted definition.

Paragraph pattern:

1. Explain why the concept matters to the research problem.
2. Compare definitions, dimensions, measurements, or debates.
3. Identify ambiguity, static treatment, overlap with adjacent concepts, or context mismatch.
4. Provide the paper's working definition and justify it.

Avoid: dictionary definitions, unsupported redefinitions, or concepts disconnected from the theory.

### 3. Hypotheses Development

Goal: synthesize evidence and use conceptual reasoning to justify each hypothesis.

For each hypothesis:

1. Summarize prior findings on the focal relationship.
2. Identify agreement, contradiction, missing mechanism, or missing boundary condition.
3. Use the guiding theory to explain why the relationship should occur.
4. State the hypothesis in a clean H1/H2/H3 format.

Avoid: jumping from citations to hypotheses, averaging away contradictory findings, or using citations as a list instead of a debate.

## Output Quality Rules

- Write in polished academic Chinese unless the user asks for English.
- Critique constructively: focus on what prior research leaves unanswered, not what authors “failed” to do.
- If citations are provided, use them where claims depend on evidence.
- If citations are absent, draft with citation placeholders such as `(Author, Year)` and clearly mark where verified sources are needed.
- If the provided literature cannot support a proposed hypothesis, say exactly what support is missing.

## Detailed Prompt Template

When the user asks for a reusable prompt, or when you need a fuller drafting scaffold, read:

- `references/ai_prompt_template.md`

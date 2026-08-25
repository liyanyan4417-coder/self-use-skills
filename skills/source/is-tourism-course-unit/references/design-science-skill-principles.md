# Design Science Principles for `is-tourism-course-unit`

This reference translates the logic of March & Smith (1995), Hevner et al. (2004), Peffers et al. (2007), and Gregor & Hevner (2013) into rules for designing, using, evaluating, and improving the `is-tourism-course-unit` skill.

中文：

本文件不是总结四篇论文的理论贡献，而是把 March & Smith (1995)、Hevner et al. (2004)、Peffers et al. (2007)、Gregor & Hevner (2013) 的设计科学逻辑转化为 `is-tourism-course-unit` 的设计、使用、评价和升级规则。

---

## 1. What Kind of Artifact Is This Skill? / 这个 skill 是什么类型的 artifact？

Following March & Smith (1995), this skill should be understood as a course-development artifact with four nested outputs:

1. Constructs: terms and distinctions used to organize work, such as foundation unit, applied paper-pair unit, tourism bridge, micro-build, student reading material, A/B/C/D module, and Personal IS Model.
2. Models: relationships among those constructs, such as `IS core paper -> tourism bridge -> tourism counterpart -> comparison -> teaching output`.
3. Methods: repeatable procedures, such as full-PDF reading, DOI verification, paper card construction, teaching transformation, DOCX/PPT generation, and evaluation.
4. Instantiations: concrete outputs in `IS-Learning/teaching/`, including Unit 01, Unit 02, Unit 03, Unit 04, student materials, scripts, decks, and micro-builds.

中文：

按照 March & Smith (1995) 的逻辑，这个 skill 不是一句提示词，也不只是一个文件模板，而是一个课程开发 artifact。它至少包含四层产物：

1. 构念：基础概念型单元、应用文献闭环型单元、旅游桥接、micro-build、学生文献理解材料、A/B/C/D 模块、Personal IS Model 等。
2. 模型：这些构念之间的关系，例如 `IS 核心文献 -> 旅游桥接 -> 旅游对应文献 -> 对比 -> 教学输出`。
3. 方法：可重复执行的流程，例如全文读取、DOI 核验、文献卡片、教学转化、DOCX/PPT 生成和评价。
4. 实例化：真实落地的课程文件，例如 Unit 01、Unit 02、Unit 03、Unit 04、学生材料、讲稿、PPT 和 micro-build。

Design implication:

The skill should not be evaluated only by whether it produces many files. It should be evaluated by whether its constructs are clear, its models are coherent, its methods are repeatable, and its instantiations are useful in teaching.

中文设计含义：

不能只用“是否生成了很多文件”来评价这个 skill。应评价它的构念是否清楚、模型是否一致、方法是否可重复、实例化是否真的能服务课堂。

---

## 2. Problem Class / 这类 skill 解决哪一类问题？

The skill is for ill-structured teaching transformation problems where a teacher must turn research knowledge into teachable, shareable, and reusable course units.

Use this skill when the task has all or most of these features:

1. The source material is research-heavy: papers, problem maps, reading cards, or academic concepts.
2. The target audience needs scaffolding: first-time IS learners, tourism management students, professional master's students, or mixed graduate classes.
3. The output must be human-facing: DOCX, PPTX, classroom script, student material, discussion activity, micro-build, or course architecture.
4. The task requires a controlled transfer from Information Systems to tourism / hospitality, not a loose analogy.
5. The result should be reusable as part of a longer course system.

中文：

这个 skill 适用于一类结构不完全清楚的教学转化问题：教师需要把研究知识转化为可讲、可读、可练、可分享、可复用的课程单元。

适用条件：

1. 输入材料具有研究密度：论文、问题地图、文献卡片或学术概念。
2. 学生需要脚手架：第一次学习 IS、旅游管理学生、专硕研究生或学硕/专硕混合班。
3. 输出要给人使用：Word、PPT、课堂讲稿、学生材料、讨论活动、micro-build 或课程结构。
4. 任务需要从 IS 到旅游/酒店的受控迁移，而不是随意类比。
5. 结果应能沉淀到长期课程系统中复用。

Do not use this skill as the main method when:

1. The user only wants a generic summary of a paper.
2. The task is a pure literature review with no teaching transformation.
3. The target field is not tourism / hospitality and no transfer logic is requested.
4. The user needs a formal empirical research manuscript rather than teaching materials.
5. The paper PDF is unavailable or invalid and the user asks for deep-reading claims.

---

## 3. Design Principles / 设计原则

### 3.1 Build and Evaluate, Not Merely Summarize

March & Smith (1995) distinguish building/evaluating from theorizing/justifying. For this skill, the main activity is build/evaluate:

```text
build a course-development artifact
-> evaluate whether it helps teaching, reading, discussion, and reuse
```

中文：

这个 skill 的核心不是“总结论文”，而是构建并评价一个课程开发 artifact：

```text
构建课程开发 artifact
-> 评价它是否帮助教学、阅读、讨论和复用
```

### 3.2 Preserve Problem Relevance

Following Hevner et al. (2004), every unit must start from a relevant problem:

```text
What IS problem or foundational IS concept does this unit help students understand?
Why does this matter in tourism / hospitality?
```

If a unit cannot answer these questions, do not proceed to slides or DOCX generation.

中文：

每个单元必须先回答：

```text
本单元帮助学生理解哪个 IS 问题或基础概念？
为什么这个问题在旅游/酒店情境中重要？
```

如果回答不了，不能急着做 PPT 或 Word。

### 3.3 Treat Teaching Materials as Artifacts

A course outline, lecture script, student literature material, PPT deck, discussion activity, and micro-build are all artifacts. They must have:

1. a purpose;
2. a target user;
3. input evidence;
4. internal structure;
5. evaluation criteria;
6. version status.

中文：

课程大纲、讲稿、学生文献理解材料、PPT、课堂讨论活动和 micro-build 都是 artifact。每个 artifact 都应说明：

1. 用途；
2. 使用者；
3. 输入证据；
4. 内部结构；
5. 评价标准；
6. 版本状态。

### 3.4 Reorganize Around Student Understanding

For teaching, literature should be reorganized around student understanding rather than article order.

Required logic:

```text
student confusion
-> why the confusion is reasonable but incomplete
-> paper lens or concept
-> tourism/hospitality case
-> discussion or micro-build
```

中文：

教学转化不是按论文原章节复制，而是按学生理解路径重组：

```text
学生困惑
-> 为什么这个困惑合理但不完整
-> 文献提供的概念或镜头
-> 旅游/酒店案例
-> 讨论或 micro-build
```

### 3.5 Separate Original Analysis From Application Transfer

Analyze the IS paper on its own terms first. Only then build the tourism bridge.

中文：

先按 IS 文献自身逻辑理解，再进行旅游情境迁移。不要一开始就把旅游应用混入原文分析。

### 3.6 Make Evaluation Explicit

Following Hevner et al. (2004), the skill must ask:

```text
What utility does this artifact provide?
What evidence shows that utility?
```

For this course skill, utility means:

1. the teacher can understand the unit structure quickly;
2. students can understand the assigned literature without distortion;
3. classroom activities are feasible for the students' level;
4. tourism transfer is controlled and not superficial;
5. outputs are stored in the right file formats and locations;
6. the unit updates the larger Personal IS Model.

中文：

评价时必须问：

```text
这个 artifact 提供什么效用？
有什么证据说明它有这个效用？
```

在本课程 skill 中，效用包括：

1. 教师能快速理解单元结构；
2. 学生能不失真地理解指定文献；
3. 课堂活动符合学生水平；
4. 旅游迁移是受控的，不是表面类比；
5. 输出文件格式和位置正确；
6. 单元能更新更大的 Personal IS Model。

---

## 4. Method Logic / 方法逻辑

Following Peffers et al. (2007), this skill should use a design process similar to DSRM:

```text
1. Identify teaching problem
2. Define objectives for the course artifact
3. Design and develop the unit
4. Demonstrate it through a tourism/hospitality case or classroom flow
5. Evaluate it against teaching, evidence, format, and reuse criteria
6. Communicate it through DOCX, PPTX, Markdown, index files, and final notes
```

中文：

按照 Peffers et al. (2007) 的方法逻辑，这个 skill 的工作过程应是：

```text
1. 识别教学问题
2. 确定课程 artifact 的目标
3. 设计并开发单元
4. 通过旅游/酒店案例或课堂流程进行展示
5. 根据教学、证据、格式和复用标准进行评价
6. 通过 DOCX、PPTX、Markdown、索引文件和最终说明进行沟通
```

The process does not have to be strictly linear. Acceptable entry points include:

1. a downloaded paper;
2. a student confusion;
3. a course unit gap;
4. a tourism management problem;
5. a micro-build idea;
6. a need to retrofit existing outputs.

中文：

流程不必机械线性。可以从以下入口进入：

1. 已下载文献；
2. 学生困惑；
3. 课程单元缺口；
4. 旅游管理问题；
5. micro-build 想法；
6. 已有输出需要系统化补齐。

---

## 5. Evaluation Logic / 评价逻辑

Use four evaluation layers.

### 5.1 Construct Clarity

Ask:

- Are key terms clearly distinguished?
- Does the unit avoid confusing technology, IT artifact, information system, platform, tool, and AI function?
- Does each term help teaching rather than add jargon?

中文：

- 核心术语是否清楚区分？
- 是否避免混淆 technology、IT artifact、information system、platform、tool、AI function？
- 术语是否服务教学，而不是制造术语堆积？

### 5.2 Model Coherence

Ask:

- Does the unit preserve a visible logic chain?
- Are IS problem, tourism bridge, evidence, activity, and output connected?
- Does the A/B/C/D module alignment clarify rather than decorate?

中文：

- 单元是否有清楚的逻辑链？
- IS 问题、旅游桥接、证据、活动和输出是否相互连接？
- A/B/C/D 模块标注是否真的帮助理解，而不是装饰？

### 5.3 Method Repeatability

Ask:

- Could the same method be used for another paper pair or foundation concept?
- Are file locations, formats, and statuses clear?
- Are human intervention points explicit?

中文：

- 这个方法是否能迁移到另一个文献对或基础概念？
- 文件位置、格式和状态是否清楚？
- 需要人工介入的地方是否明确？

### 5.4 Teaching Utility

Ask:

- Can the teacher teach from the output?
- Can students read and discuss from the output?
- Is the activity feasible in the given class time?
- Does the material support professional master's learning rather than only academic reading?

中文：

- 教师能否直接据此授课？
- 学生能否据此阅读和讨论？
- 活动是否能在课时内完成？
- 材料是否支持专硕学习，而不只是学术阅读？

---

## 6. Contribution and Transfer Value / 贡献与迁移价值

Following Gregor & Hevner (2013), do not judge this skill only by whether it produces one useful unit. Judge what kind of reusable knowledge it creates.

### 6.1 Routine Design

Use existing templates to create a normal course unit.

Example:

```text
Generate a teacher outline and teaching script for a familiar unit.
```

Value:

```text
efficient production
```

### 6.2 Improvement

Improve an existing course unit or workflow.

Example:

```text
Add standalone student literature understanding materials to all literature-based units.
```

Value:

```text
better fit, less clutter, more reliable teaching use
```

### 6.3 Exaptation

Apply an existing IS learning method to a new teaching context.

Example:

```text
Move from self-learning paper cards to professional-master teaching materials.
```

Value:

```text
controlled transfer across use contexts
```

### 6.4 Invention

Create a new reusable course-development artifact where no adequate method exists.

Example:

```text
Develop a hybrid IS-to-tourism course unit system that combines full-text reading, tourism transfer, micro-build, and human-facing deliverables.
```

Value:

```text
new method for a class of teaching transformation problems
```

中文：

按照 Gregor & Hevner (2013) 的逻辑，不应只看这个 skill 是否做出一个有用单元，还要判断它创造了哪类可复用知识：

1. routine design：用现有模板高效生成普通单元；
2. improvement：改进已有单元或流程；
3. exaptation：把原来自学系统中的方法迁移到教学场景；
4. invention：创造一种新的 IS-to-tourism 课程开发 artifact。

本 skill 的长期价值应向 improvement、exaptation 和 invention 升级，而不是停留在 routine design。

---

## 7. Boundary Conditions / 边界条件

The skill works best when:

1. local PDFs or reliable full-text sources are available;
2. the user can clarify target students, class hours, teaching goals, and output format;
3. tourism / hospitality application is meaningful rather than forced;
4. there is enough time to evaluate and revise the human-facing outputs;
5. the course belongs to a longer system rather than a one-off summary task.

The skill is weak or should pause when:

1. PDFs are unavailable but the user asks for deep reading;
2. DOI or source metadata cannot be verified;
3. the tourism counterpart is low quality or outside the agreed journal scope;
4. the requested output is only a generic summary with no course use;
5. the student's level makes independent analysis too difficult and teacher scaffolding has not been designed;
6. a micro-build is requested but the problem, user, artifact boundary, and evaluation criteria are not yet defined.

中文：

适用条件：

1. 有本地 PDF 或可靠全文来源；
2. 用户能明确学生对象、课时、教学目标和输出格式；
3. 旅游/酒店迁移是有意义的，不是强行类比；
4. 有时间检查和修订人类可读输出；
5. 课程属于长期系统，而不是一次性摘要。

暂停或弱适用条件：

1. 没有 PDF 却要求深度阅读；
2. DOI 或来源信息无法核验；
3. 旅游对应文献质量低或不符合约定期刊范围；
4. 用户只要泛泛摘要，不需要课程转化；
5. 学生水平不支持独立分析，但还没有设计教师脚手架；
6. 用户要求 micro-build，但问题、用户、artifact 边界和评价标准尚未定义。

---

## 8. Skill Upgrade Checklist / Skill 升级检查表

When improving this skill or using it for a new type of unit, check:

1. Artifact: What exactly is being designed?
2. Problem relevance: What teaching or learning problem does it solve?
3. Objectives: What must the artifact help the teacher or students do?
4. Construction: What files, templates, sources, and processes create it?
5. Demonstration: Where is it shown in a unit, case, classroom flow, or micro-build?
6. Evaluation: What evidence shows that it works?
7. Communication: Which Markdown, DOCX, PPTX, index, or final note communicates it?
8. Boundary: When should this skill not be used or should ask for human intervention?
9. Transfer: What reusable rule, method, or model should be added back to the skill?

中文：

升级 skill 或用于新类型单元时，检查：

1. Artifact：到底在设计什么？
2. 问题相关性：它解决什么教学或学习问题？
3. 目标：它必须帮助教师或学生做到什么？
4. 构建：哪些文件、模板、来源和流程构成它？
5. 展示：它在哪个单元、案例、课堂流程或 micro-build 中被呈现？
6. 评价：有什么证据说明它有效？
7. 沟通：通过哪些 Markdown、DOCX、PPTX、索引或最终说明传达它？
8. 边界：什么时候不该使用这个 skill，或必须要求人工介入？
9. 迁移：哪些可复用规则、方法或模型应回写到 skill？

---

## References / 参考文献

Gregor, S., & Hevner, A. R. (2013). Positioning and presenting design science research for maximum impact. *MIS Quarterly, 37*(2), 337-355. https://doi.org/10.25300/MISQ/2013/37.2.01

Hevner, A. R., March, S. T., Park, J., & Ram, S. (2004). Design science in information systems research. *MIS Quarterly, 28*(1), 75-105. https://doi.org/10.2307/25148625

March, S. T., & Smith, G. F. (1995). Design and natural science research on information technology. *Decision Support Systems, 15*(4), 251-266. https://doi.org/10.1016/0167-9236(94)00041-2

Peffers, K., Tuunanen, T., Rothenberger, M. A., & Chatterjee, S. (2007). A design science research methodology for information systems research. *Journal of Management Information Systems, 24*(3), 45-77. https://doi.org/10.2753/MIS0742-1222240302

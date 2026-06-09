---
name: paper-logic-reviser
description: >
  论文逻辑修改 / paper logic reviser. ALWAYS invoke this skill immediately when the user says
  「按照模版修改论文」「按模版改论文」「用模版/对照模版改论文」「把论文对齐模版/期刊模版」 or the English
  equivalents "revise/align the paper to the template" — these are strong, direct triggers; do not answer from
  scratch. Also use it whenever the user wants to revise, restructure, polish, or align the LOGIC and SECTION
  STRUCTURE of an empirical paper, especially tourism/hospitality/management papers using PLS-SEM with an
  "antecedent X → mediator(s) M → outcome Y, moderated by case/group type W" chain (the Yi et al. TM
  template). Trigger for: 改论文逻辑, 重写/润色 引言/文献/假设/结论/讨论/理论贡献/实践启示/局限,
  restructure the discussion, make the conclusion match the template, check whether gaps map onto contributions,
  ensure hypotheses–results–discussion line up, or revise ANY single section. Use it EVEN WHEN the user names
  only one section — it keeps that section coherent with the whole via a shared model card and coherence checks.
---

# Paper Logic Reviser（论文逻辑修改）

帮助把一篇实证论文（典型为旅游/酒店/管理类、PLS-SEM、双案例、含中介与调节）逐部分修改、重组、润色，
使其**结构与逻辑严格对齐"Yi et al., Tourism Management"模版**，并且**每一部分单独修改时仍与全文前后呼应**。

本技能的核心信念：一篇好论文是**一条因果链贯穿六大部分**。任何单点修改若脱离这条链，就会破坏呼应。
因此本技能要求：先把链建成"模型卡"，再以模型卡为锚去改任何一部分，改完必须跑"跨章节呼应自检"。

---

## 第 0 步（必做）：建立论文"模型卡"

在动任何笔之前，先从论文里抽出因果链，填好下面的模型卡。后续每一部分的修改都引用它，这是保证"单独改也呼应"的关键。

```
论文模型卡 (Model Card)
- 理论透镜 (Theory lens)：____（如 群际接触理论 / Dewey美学 / Tuan地方感）
- 自变量 X (前因)：____（可拆成 X1, X2）
- 中介 M：____（M1, M2…）
- 结果 Y：____
- 调节 W：____（两案例/两群组的"差异化属性"是什么？）
- 案例 A / 案例 B：____ / ____（各自的历史—文化—经济差异，用于支撑 W）
- 核心发现序列：哪些 H 成立/不成立？是否有"效应强弱排序"？
- 支撑文献池：每条链路可引用的前人实证（用于讨论的"对照前人"）
```

抽不全时，先向用户确认缺口，不要臆造数据或文献。模型卡是后续一切修改的"唯一事实源"。

---

## 第 1 步：定位要修改的部分

用户可能说"改全文逻辑"，也可能只说"重写 5.1"。无论范围大小，都按下表路由到对应拆解与手册。
**即使只改一个部分，也必须读 `references/logic-loops.md` 跑该部分相关的呼应回路。**

| 用户想改的部分 | 先读（拆解） | 再读（独立修改手册） | 必跑的呼应回路 |
|---|---|---|---|
| 引言 Introduction | anatomy §1 | playbooks §A | Loop① 空白↔贡献 |
| 文献综述 Literature | anatomy §2 | playbooks §B | Loop① + 透镜↔假设 |
| 假设发展 Hypotheses | anatomy §3 | playbooks §C | Loop② 假设↔结果↔讨论 |
| 方法 Methodology | anatomy §4 | playbooks §D | Loop③ 选案例↔调节 |
| 结果 Results | anatomy §5 | playbooks §E | Loop② |
| 结论与讨论 Conclusion & discussion | anatomy §6 | playbooks §F | Loop① + ② + ③（全部）|
| 理论贡献 5.1 | anatomy §6.2 | playbooks §G | Loop① 空白↔贡献 |
| 实践启示 5.2 | anatomy §6.3 | playbooks §H | 链条逐节点 + Loop③ |
| 局限与未来 5.3 | anatomy §6.4 | playbooks §I | 与发现/调节挂钩 |
| 影响声明 Impact statement | anatomy §6.5 | playbooks §J | 三点呼应三大贡献 |

拆解文件：`references/template-anatomy.md`（逐段功能拆解 + 话术库）
修改手册：`references/section-playbooks.md`（每部分可独立执行的修改公式、填空槽、自检表）
呼应回路：`references/logic-loops.md`（三条必须闭合的回路 + 全文映射总表 + 呼应点清单）

---

## 第 2 步：按手册修改该部分

修改任一部分时遵循通用三动作：

1. **复述模版功能**：先回到 `template-anatomy.md` 看这部分"每段该干什么"。
2. **套用独立修改公式**：在 `section-playbooks.md` 找到该部分的"段落模版 + 填空槽 + 话术库"，用模型卡的内容填空。
3. **本地自检**：用该部分手册末尾的自检表逐条打勾。

修改原则（务必遵守）：
- **不臆造**：文献、β值、案例事实只能来自论文本身或用户确认；缺则标注待补，不杜撰。
- **保留作者实质观点**：是"重构逻辑与表达"，不是"改写结论"。除非数据要求，不改变研究发现的方向。
- **术语一致**：构念名、缩写、效应方向在全文统一（与模型卡一致）。
- **讨论 vs 理论贡献分工**：讨论(Discussion)以"实证对照前人"为主；理论贡献(5.1)以"理论拔高/补缺口"为主。两者可呼应但不重复。

---

## 第 3 步（必做）：跨章节呼应自检

无论改了多少，最后都读 `references/logic-loops.md` 跑三条回路，确认前后呼应没有断裂：

- **Loop① 空白↔贡献**：引言提的每个空白，5.1 必逐条回收；数量与措辞对应。
- **Loop② 假设↔结果↔讨论**：H1…Hn 的数量、顺序、命名在三处完全一致，不增不减；不成立的假设也要在讨论里解释。
- **Loop③ 选案例↔调节**：方法里"为何选这两个案例/群组"的差异化论证，必须支撑调节假设，并在讨论的调节段与 5.2 的差异化管理里收尾。

若只改了单一部分，至少跑该部分在路由表里标注的回路，并检查它对相邻部分是否产生了未同步的措辞（如改了 5.1 的贡献表述，需回头确认引言空白是否仍对应）。

---

## 交付物规范（编辑 Word 文档时）

当任务是直接修改 `.docx` 文件时：
- **先读 docx 技能** `/mnt/skills/public/docx/SKILL.md`，按"unpack → 改 XML → pack"流程操作。
- **重写/新增的正文用红色字体**（`<w:color w:val="FF0000"/>`），方便作者区分改动。
- **只给意见、不改写的部分，用 Word 批注**（用 `comment.py`，作者署名 Claude）锚定到对应标题或段落。
- **章节重组**（如合并 Conclusion 与 Discussion、重编号 5.1/5.2/5.3）通过整段替换与标题改名完成；删除被并入的旧标题与作者工作笔记，并把相关批注重新锚定或更新。
- 改完 `pack.py --original` 验证通过后，用 `present_files` 交付，并在对话里简述每处改动与需作者把关之处（尤其新引用是否在参考文献中）。

若任务只是产出修改意见或大纲（非编辑文件），直接在对话中按拆解给出，不必创建文件。

---

## 适用与边界

- 最适合：感知真实性/体验类前因 → 认知/情感/审美/认同类中介 → 行为/责任/口碑类结果、双案例 PLS-SEM + 多群组分析的论文。
- 也可迁移：任何"前因→机制→结果（含调节）"的实证社科论文；非该范式时，仍可用六大部分骨架与三条回路，但需相应调整话术库。
- 不做：编造数据/文献、改变研究结论方向、替代统计分析本身。

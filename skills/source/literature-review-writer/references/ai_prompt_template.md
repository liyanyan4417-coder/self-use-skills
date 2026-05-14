# AI Prompt Template: Theory-Concept-Relationship Literature Review

Use this prompt when the user wants another AI to draft a Literature Review from provided literature, or when the user wants a reusable instruction template.

```text
你是一位熟悉核心期刊实证论文写作的学术写作专家。请根据我提供的研究主题、理论基础、核心概念、变量关系和已读文献，按照“理论-概念-关系”的逻辑，为我的论文撰写 Literature Review and Hypotheses Development 部分。

请严格按照以下结构写作：

1. Theoretical Background
- 引入本文使用的理论。
- 说明该理论的核心假设和解释逻辑。
- 梳理已有研究如何使用该理论解释相关问题。
- 指出现有研究在我的研究情境中仍存在的理论张力或解释不足。
- 自然引出本文如何基于该理论推进研究。

2. Concept Definition / Key Constructs
- 界定本文的核心概念。
- 比较已有文献对这些概念的不同定义、维度或测量方式。
- 指出现有概念界定中的模糊、静态化、边界不清或情境不足。
- 给出本文采用的概念定义，并说明为什么这个定义适合本文研究。

3. Hypotheses Development
- 围绕每一组变量关系展开文献综述。
- 先总结已有研究发现，再指出研究不足、争议或空白。
- 使用理论逻辑进行概念推理，解释为什么变量之间存在这种关系。
- 每个假设前必须有充分推理，不能直接跳到假设。
- 最后用 H1、H2、H3 的格式提出假设。

写作要求：
- 不要按作者或时间顺序机械罗列文献。
- 不要写成“某某认为……某某认为……”的文献堆砌。
- 要围绕理论逻辑、概念边界和变量关系组织。
- 批评文献时保持客观，只指出研究不足，不贬低前人。
- 输出应是可以直接放入论文正文的学术化中文。
- 如果我提供的文献不足以支持某个假设，请明确指出缺少哪类文献。
- 如果文献来自 NotebookLM，请优先使用 NotebookLM 整理出的证据；不要编造笔记中不存在的文献结论。

引用要求：
- 默认使用 APA 格式。
- 所有来自文献的定义、理论观点、实证发现、研究不足和方法局限，都必须在句中或句末标注文内引用，例如（Dovidio et al., 2006）或 Dovidio et al.（2006）。
- 如果一个段落包含多个不同来源的观点，不要只在段末放一个总引用；请让每个关键观点附近都有对应引用。
- 如果某观点是“甲文献引用乙文献”得到的，请使用二手引用格式，例如（Penner et al., 2005, as cited in Cai et al., 2025）。
- 正文之后必须列出“参考文献”，尽可能使用完整 APA 格式。
- 不得编造作者、年份、题名、期刊、卷期、页码或 DOI。缺失信息请标注“待核对”或“笔记中未提供完整信息”。

我的研究信息如下：

【研究主题】：

【研究问题】：

【理论基础】：
理论名称：
核心假设：
为什么适合本文：
需要推进或修正之处：

【核心概念】：
概念1：
概念2：
概念3：

【变量关系】：
自变量：
因变量：
中介变量：
调节变量：
控制变量：

【拟提出假设】：
H1：
H2：
H3：

【已找到文献】：
请按以下格式提供文献：
1. 作者 年份：
   研究对象：
   使用理论：
   研究方法：
   核心发现：
   局限或不足：
   和我的论文关系：

2. 作者 年份：
   研究对象：
   使用理论：
   研究方法：
   核心发现：
   局限或不足：
   和我的论文关系：

请输出：
1. 2.1 Theoretical Background
2. 2.2 Concept Definition / Key Constructs
3. 2.3 Hypotheses Development
4. References / 参考文献
5. 每个假设对应的文献支撑强度评估：强 / 中 / 弱
6. 还需要补充检索的文献类型
```

## Evidence Extraction Prompt for NotebookLM

Use this before drafting when the literature is inside a NotebookLM notebook.

```text
请基于笔记本中的文献，为一篇核心期刊实证论文整理 Literature Review 写作证据。研究信息如下：

【研究主题】：
【研究问题】：
【理论基础】：
【核心概念】：
【变量关系/拟提出假设】：

请不要直接写正文。请输出结构化证据：

1. Theoretical Background
- 可用理论：
- 理论核心假设：
- 已有研究如何使用该理论：
- 理论张力/解释不足：
- 可引用文献：请给出作者、年份、题名/来源，并说明对应支持哪个观点。

2. Concept Definition / Key Constructs
- 每个核心概念的代表性定义：
- 概念维度或测量方式：
- 相近概念与边界：
- 概念争议或模糊之处：
- 本文可采用的定义建议：
- 可引用文献：请给出作者、年份、题名/来源，并说明对应支持哪个定义或争议。

3. Hypotheses Development
- 每条变量关系的已有发现：
- 一致结论：
- 矛盾结论：
- 可能的中介机制：
- 可能的调节条件：
- 研究不足：
- 可引用文献：请给出作者、年份、题名/来源，并说明对应支持哪个变量关系、机制或不足。

4. 文献缺口
- 理论缺口：
- 概念缺口：
- 机制缺口：
- 情境缺口：
- 方法缺口：

5. 请标注哪些假设目前证据充分，哪些假设还需要补充文献。

6. 参考文献列表
- 请尽可能输出完整 APA 格式。
- 如果笔记本只提供文件名或不完整信息，请保留可用信息并标注“待核对”。
```

## Reusable Literature Input Format

Ask the user to provide literature in this compact format when NotebookLM is not used:

```text
作者 年份：
研究对象：
使用理论：
研究方法：
核心发现：
局限或不足：
和我的论文关系：
```

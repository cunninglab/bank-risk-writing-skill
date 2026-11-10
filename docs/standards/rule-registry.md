# 规则与机制登记表

本文件供维护者使用，不进入 skill 运行时上下文。依据：`docs/standards/skill-quality-standard.md` B1（机制登记）与 B3（领域规则出处）。

## 一、机制登记（B1）

| 编号 | 名称 | 防的失效 | 目标判据 | 位置 | 代表用例 | 消融结论 | 证据 |
|---|---|---|---|---|---|---|---|
| M1 | 先建依据清单 | 事实失效 | C1 | 已删除（原为 `rules/evidence-ledger.md` 及 policy-brief、report-outline、ppt-outline 中的 `mechanism:M1` 区域；可从 `ce91692` 恢复） | policy-brief / case-01 检索版 | 删除：按 C1.2 全文重判后，两对的完整组与去除组 C1 都不通过，打平后补跑仍打平 | `docs/experiments/2026-11-09-skills-upgrade/results.md`；`c12/verdicts.md` 更正一节；运行 r02、r03、r11、r12 |
| M2 | 研究增量 | 增量失效 | C3.1–C3.4 | `rules/research-increment.md`；policy-brief、report-outline、ppt-outline 中的 `mechanism:M2` 区域 | report-outline / case-07 | 保留：C1 两组都通过，C3 合计 8 对 4 | `docs/experiments/2026-11-09-skills-upgrade/results.md`；运行 r07、r08 |

未进入候选的 huashu-report 做法见标准第四节；“四角色身份设定”不采纳。

## 二、领域规则出处（B3）

“出处”一栏写明 `CLAUDE.md` 段落、`prompts/task-routing.md` 或公开样本的位置。公开样本文本由 pypdf 5.1.0 提取，仅用于定性阅读。

| 规则 | 使用 skill | 出处 | 处理 |
|---|---|---|---|
| 开头给一句话结论或任务结果 | 全部 | `CLAUDE.md` Default Output Structure 第 1 项 | 保留 |
| 事实 / 判断 / 建议分层 | 全部 | `CLAUDE.md` Factuality Rules › Required behavior | 并入 `rules/core.md` |
| 写“变化 / 新增 / 收紧”须有比较依据 | policy-brief | `CLAUDE.md` Style Requirements › policy analysis（distinguish new changes from background rules） | 保留；比较依据可通过检索上一版文件获得 |
| 润色保持原意、不扩写 | formal-polish | `CLAUDE.md` Style Requirements › formal report polishing | 保留 |
| 提纲每节对应一个写作任务，结构来自材料 | report-outline | `CLAUDE.md` Style Requirements › report outlines | 保留 |
| 一级提纲“4–6 节” | report-outline | 无 `CLAUDE.md` 出处。样本：德勤报告 5 章（目录第 2–3 页），KPMG 报告 5 个主体部分（目录第 3 页）；两份都是咨询机构的年度行业报告，与风险研究提纲不同类 | **删除数字**，改为“节数由材料决定，不为显得完整而增加章节”（`CLAUDE.md` report outlines：do not produce generic empty frameworks） |
| 多种可行结构时先推荐一种并说明理由 | report-outline | 无直接出处；与 `CLAUDE.md` Collaboration Norm（make a reasonable assumption … state the assumption）一致 | 保留，改写为“选与读者用途最匹配的一种，并说明理由” |
| PPT 页标题观点化 | ppt-outline | `CLAUDE.md` Style Requirements › PPT outlines。样本：德勤报告分析页以结论句为标题（第 15 页“境内银行盈利增势放缓，境外银行盈利能力提升”，第 33 页“业管费增速逐渐放缓，成本控制逐步改善”），图题“银行业息差降幅趋缓”（第 13 页） | 保留 |
| 查数型内容的图表 / 页标题可用中性描述 | ppt-outline、report-outline | 样本：德勤报告业绩数据部分的图题是中性描述（如“图1：归属于母公司股东的净利润”，第 15 页），宏观分析部分用结论句 | 作为观点化标题的例外保留 |
| 一页一个核心信息 | ppt-outline | `CLAUDE.md` Style Requirements › PPT outlines（one slide should carry one core message）。样本：德勤报告分析页为“一个结论标题 + 一段支撑” | 保留 |
| 每页“3–5 个支撑点” | ppt-outline | 数字无出处：`CLAUDE.md` 未规定，样本中也没有逐页要点式的 deck。test-cases 中的“3–5”除 case-12 外都写在任务要求里，是用户对单个任务提出的数量（case-10 任务要求第 3 条、输入原文“每页控制在 3–5 个支撑点”），不构成全局默认值的出处。定性要求有出处：`CLAUDE.md` Style Requirements › PPT outlines（keep supporting bullets focused and brief；one slide should carry one core message） | **删除数字**，改为“每页只留支撑本页结论所必需的支撑点，每条一行短句”；case-12 期望特征同步改为定性表述。用户在任务中指定数量时照用户要求 |
| 汇报版“核心结论 → 3–5 个关键点 → 建议关注事项” | policy-brief | 结构有出处：`prompts/task-routing.md` 混合意图路由表“领导/管理层汇报版”行（结论先行、篇幅精简）。数字无出处；case-02 的“3–5 个关键点”写在任务要求里，属于用户对该任务的指定 | 保留结构，**删除数字**，改为“支撑结论所必需的关键点” |
| 材料不足时标为“初始提纲 / 初步框架”并列缺口 | report-outline、ppt-outline | `CLAUDE.md` Factuality Rules › When the input is incomplete | 保留；删除“少于 5 页”的数字门槛 |
| 汇报版结论先行、篇幅精简、待核实事项不省略 | policy-brief、ppt-outline | `prompts/task-routing.md` 混合意图路由表“领导/管理层汇报版”行 | 保留 |
| 不建议上屏的内容放备注 | ppt-outline | `CLAUDE.md` PPT outlines（prioritize summary and speakability） | 保留 |
| 不写工作过程叙述、空话、重复免责 | 全部 | `CLAUDE.md` Hard Prohibitions（produce verbose filler）、Core Writing Principles › Avoid（repetitive filler language） | 并入 `rules/core.md` |
| 研究增量中的外部基准 | M2 | 样本：KPMG 报告单设“2024 年银行业发展回顾及与国际同业比较”一章（目录第 3 页）；德勤报告逐项对照境内与境外银行（第 15–16 页） | 作为 M2 的领域依据；去留以消融结论为准 |

## 三、样本局限

- 样本只有 5 份公开材料：2 份咨询机构行业报告、2 份年报、1 份监管通知。研究提纲、内部汇报 PPT 都没有可比样本。
- 两份咨询报告的元数据都标有 `promotional-tone`，只用来取证结构和标题写法，不用来取证措辞。
- 年报与监管通知没有用来支撑上表的任何规则；它们在实验中作为输入材料使用。

结论：**FAIL**。发现 **6 项 Blocking、1 项 Nit**。

已复核：`npm test` 为 0 error、0 warning；12 份输出与对应 JSONL 最终消息一致；分数加总与揭盲映射一致；四份快照哈希均能重算匹配，消融后无悬空机制引用；`CLAUDE.md` 的 Hard Prohibitions 未变。以下问题仍阻断验收。

1. **F1 · Blocking：来源标记不变量缺失**

   **位置：** [rules/core.md:38](/Users/cunning/Workspace/repos/cunninglab/bank-risk-writing-skill/rules/core.md:38)、[rules/evidence-ledger.md:14](/Users/cunning/Workspace/repos/cunninglab/bank-risk-writing-skill/rules/evidence-ledger.md:14)。

   **反例与证据：**【观察】两处都允许仅用机构、标题、日期和 URL 表示检索来源，没有要求标明“自行检索”；r02、r03、r12 已因此被判 C1.4 不通过。【推断】照字面完整执行这些指令，仍可能违反验收条件 3 和标准第五节不变量。

   **最小修正：** 在共享内核明确要求区分来源取得方式，同步修正 M1 的字段说明和示例，并更新受影响的验证证据。方案 5.5 规定失败后的处理方式，并未豁免这一不变量；登记为待办不能使本次验收通过。

2. **F2 · Blocking：M1 保留依赖的唯一一次 C1 通过不成立**

   **位置：** [judge/scores-round2.json:20](/Users/cunning/Workspace/repos/cunninglab/bank-risk-writing-skill/docs/experiments/2026-11-09-skills-upgrade/judge/scores-round2.json:20)、[c12/verdicts.md:17](/Users/cunning/Workspace/repos/cunninglab/bank-risk-writing-skill/docs/experiments/2026-11-09-skills-upgrade/c12/verdicts.md:17)、[results.md:49](/Users/cunning/Workspace/repos/cunninglab/bank-risk-writing-skill/docs/experiments/2026-11-09-skills-upgrade/results.md:49)。

   **反例与证据：**【观察】r11 第 69 行的“已打开核对的一级公开来源”只说明核验状态和级别，没有说明取得方式；评审却据此放过 C1.4，而对同样仅列一级来源和“已核对”的 r02 判失败。此外，r11 第 43、57、75 行的央行报告引用没有发布日期，仍被判 C1.2 通过；r02、r03 引用同一报告时也缺少发布日期。标准 C1.2 明确要求写明日期，报告覆盖年度、统计时点不能代替发布日期。

   【推断】按既定判据，r11 不能取得 C1 全通过；M1 两对运行在其唯一目标 C1 上仍打平，不能按 D3 宣布保留。这超过了“证据偏弱”的程度。这里不否定分数加总正确，也不把 D9 的“没有退步”等同于绝对合格。

   **最小修正：** 保留原始评分，追加一致口径的更正判定，重算 D3 并更新登记表和结果。按现有证据落实补跑仍打平的处理；不能继续把 M1 保留门记为通过。

3. **F3 · Blocking：M1 允许未核对的检索内容进入正文**

   **位置：** [rules/evidence-ledger.md:16](/Users/cunning/Workspace/repos/cunninglab/bank-risk-writing-skill/rules/evidence-ledger.md:16)、第 18、32 行；对照 [rules/core.md:37](/Users/cunning/Workspace/repos/cunninglab/bank-risk-writing-skill/rules/core.md:37)。

   **反例与证据：**【观察】内核要求正文未加载或找不到原文的检索内容“不进正文”；M1 却允许清单状态为“待核实”，并要求其在正文带待核实标注。【代码支持的推断】官方页面只返回模板时，把搜索摘要列入清单并带标注写进正文，符合 M1，却违反内核。未追加模型试跑。

   **最小修正：** 明确排除未核对的检索内容：只能进入“待核实线索 / 需补充来源”。将它与用户已提供、但原始出处待核实的材料分别处理。

4. **F4 · Blocking：汇报版输出契约排除了机制要求的交付物**

   **位置：** [skills/policy-brief/SKILL.md:71](/Users/cunning/Workspace/repos/cunninglab/bank-risk-writing-skill/skills/policy-brief/SKILL.md:71)，对照第 53 行及 `rules/evidence-ledger.md` 第 19 行。

   **反例与证据：**【观察】汇报版要求“不加其余各节”；M1 必须附“依据与来源”，M2 必须放入“分析与定位”。【推断】用户只指定“领导摘要版”时，逐字执行会遗漏机制交付物，或违反汇报版结构。现有实验没有覆盖这个分支。

   **最小修正：** 明确汇报版中来源清单的保留方式，以及研究增量如何压缩、合并；相关专属要求继续放入对应机制标记区域。

5. **F5 · Blocking：A7、A9 检查存在普通写法即可触发的漏检**

   **位置：** [scripts/validate-skills.js:36](/Users/cunning/Workspace/repos/cunninglab/bank-risk-writing-skill/scripts/validate-skills.js:36)、第 201–212、336–345 行。

   **反例与证据：**【实测，仅在内存替换读取内容，未改文件】以下违规内容均返回退出码 0：

   - 正文写“用 Read 打开文件，用 Grep 检索”或“使用 web.run 检索”；
   - Additional Resources 添加普通 Markdown 链接到 `../../test-cases/TEST_PLAN.md`；
   - 添加反引号路径 `./test-cases/TEST_PLAN.md`。

   WebSearch 和直接反引号路径 `test-cases/...` 能被拦截，说明检查运行正常，但覆盖不满足验收条件 7。

   **最小修正：** 补齐已知运行时工具标识；检查整个资源节中的 Markdown 链接与路径，并在判定前归一化路径。

6. **F6 · Blocking：以旧测试约定替代了 B3 要求的规则依据**

   **位置：** [docs/standards/rule-registry.md:30](/Users/cunning/Workspace/repos/cunninglab/bank-risk-writing-skill/docs/standards/rule-registry.md:30)、第 31 行；`ppt-outline/SKILL.md:65`、`policy-brief/SKILL.md:28`。

   **反例与证据：**【观察】登记表承认“每页 3–5 个支撑点”没有 `CLAUDE.md` 或样本依据，却以旧 test-cases 为由保留；汇报版“3–5 个关键点”也仅引用测试约定。标准 P9/B3 没有将测试约定列为依据，方案 4.5 更明确要求无证据数字删除或改写。

   【推断】这使本应接受重新评估的旧规则，通过旧测试自我证明。它们虽原已存在，本轮仍未满足明确验收依据。

   **最小修正：** 将默认数量改为由材料和用途决定；具体用例中用户明确要求的数量继续遵守。若要保留通用数字限制，需有符合 B3 的依据或明确获准的标准例外。

7. **N1 · Nit：A1 行数计算多算边界**

   **位置：** [scripts/validate-skills.js:330](/Users/cunning/Workspace/repos/cunninglab/bank-risk-writing-skill/scripts/validate-skills.js:330)。

   **反例与证据：**【实测】构造恰好 160 行、末尾正常换行的正文，脚本报告 `body has 162 lines` 并失败。计算包含了 frontmatter 结束行后的换行及末尾分隔项。当前四个文件均远低于上限，未影响本次实际通过结果。

   **最小修正：** 从结束分隔行之后提取正文，按实际文本行计数，验证 160/161 行边界。

审查未联网；对外部页面仅使用仓库存档证据，未重新确认线上内容。未修改文件或追加模型运行。

```text
Reviewer: Codex，本会话独立对抗式审查者，未参与实现
Reviewed scope: 已提交树 ce91692 相对 17aa290 的全部 diff；排除未跟踪的 reviews/f1-final-request.md
Selected lenses: 正确性、回归、范围、项目约定、验证证据、架构、agent 指令、安全与事实边界、文档与记录；均由本审查者覆盖
Reference: 17aa29009a0ab461d2ab726a30037ea7640d8cb5..ce916925f3525fd64b5738faeef44808a9a7ed53
Target digest: ce916925f3525fd64b5738faeef44808a9a7ed53
Helper: 未使用；目标为固定已提交树
Findings: 6 blocking / 1 nit / 0 pre-existing
Status: In Progress；阻断项修正并取得当前目标的复审证据前，最终审查门未通过
Verdict: FAIL
```
结论：**FAIL**。F5 保持；新增 **1 项 Blocking、1 项 Nit**。其余上一轮发现关闭。

已观察到：`npm test` 两个校验器均为 **0 error、0 warning、PASSED**；16 份输出均与对应 JSONL 最终消息一致；第三轮分数加总和揭盲映射一致；最终快照与 HEAD 的运行时文件匹配。M2 消融后无悬空引用。本次未修改文件、未联网、未追加模型试跑。

下列位置均指 `67fe0d5`，已结合 `17aa290..HEAD` 中的上下文检查。

| 编号 | 裁决 | 位置与依据 |
|---|---|---|
| F1 · 原 Blocking | **关闭** | [core.md:38](/Users/cunning/Workspace/repos/cunninglab/bank-risk-writing-skill/rules/core.md:38) 已明确要求“自行检索”，示例同步；r15 的来源取得方式可辨认。发布日期例外另见 F7。 |
| F2 · 原 Blocking | **关闭** | [更正判定:20](/Users/cunning/Workspace/repos/cunninglab/bank-risk-writing-skill/docs/experiments/2026-11-09-skills-upgrade/c12/verdicts.md:20) 已将 r02、r03、r11 判为 C1.2 失败；两对 M1 均打平，[结果:53](/Users/cunning/Workspace/repos/cunninglab/bank-risk-writing-skill/docs/experiments/2026-11-09-skills-upgrade/results.md:53) 和登记表落实删除。r11 的 C1.4 即使改判，也不改变结论。 |
| F3 · 原 Blocking | **关闭** | 接受 `didn't-matter`：M1 文件及三个 skill 的全部挂载区域已删除；运行时无 `mechanism:M1` 或 `evidence-ledger.md` 残留。与消融快照的剩余差异属于本轮其他修复及空行清理。 |
| F4 · 原 Blocking | **关闭** | [policy-brief:49](/Users/cunning/Workspace/repos/cunninglab/bank-risk-writing-skill/skills/policy-brief/SKILL.md:49) 明确规定汇报版把判断或局限并入“建议关注事项”，原结构排斥问题已解除。此项为静态确认，未新增汇报版试跑。 |
| F5 · Blocking | **保持** | A9 和原先列出的裸工具名反例已修复；A7 的新边界仍漏检限定名称，详见下文。 |
| F6 · 原 Blocking | **关闭** | [登记表:30](/Users/cunning/Workspace/repos/cunninglab/bank-risk-writing-skill/docs/standards/rule-registry.md:30)、policy-brief 第 28 行、ppt-outline 第 58 行已删除全局数字默认值。case-02、case-10 的数量来自具体任务要求，保留合理；case-12 已同步。 |
| N1 · 原 Nit | **关闭** | 内存实测：LF 正文恰好 160 行通过，161 行失败。修复另引入格式兼容问题，见 N2。 |

1. **F5 · Blocking · 保持：A7 仍放过带限定名称的工具引用**

   **位置：** [validate-skills.js:341](/Users/cunning/Workspace/repos/cunninglab/bank-risk-writing-skill/scripts/validate-skills.js:341)。

   **反例与证据：**【观察，内存实测】向正文分别加入：

   ```text
   调用 tools.Read 打开文件
   使用 tools.web.run 检索
   ```

   两者均返回退出码 **0**、无诊断；裸写 `Read`、`Grep`、`web.run` 则失败。【代码支持的推断】左边界把 `.` 排除在分隔符之外，因此工具名前有命名空间时跳过匹配。正文仍绑定运行时，验收条件 7 尚未满足。

   **最小修正：** 调整边界，使限定名称中的已知工具标识也能被识别；保留已通过的裸名称和 A9 反向检查。

2. **F7 · Blocking · 新增：用运行时例外改写了 C1.2 的验收结果**

   **位置：** [c12/verdicts.md:48](/Users/cunning/Workspace/repos/cunninglab/bank-risk-writing-skill/docs/experiments/2026-11-09-skills-upgrade/c12/verdicts.md:48)、[results.md:70](/Users/cunning/Workspace/repos/cunninglab/bank-risk-writing-skill/docs/experiments/2026-11-09-skills-upgrade/results.md:70)，相关指令为 `rules/core.md:38`。

   **反例与证据：**【观察】[r15:59](/Users/cunning/Workspace/repos/cunninglab/bank-risk-writing-skill/docs/experiments/2026-11-09-skills-upgrade/runs/r15.md:59) 没有给出人民银行报告的发布日期，但记录将 C1.2、最终 C1 写为“通过”。既定 C1.2 没有“发布日期待核实也算通过”的例外；记录本身也承认按该标准应失败。运行时指令不能替代验收标准。

   接受“每个来源完整引用一次、以后使用可追溯简称”的口径；它与全文没有任何可解析发布日期不同。【未证实】本次没有独立复核完整 PDF 是否确实不含发布日期；无论如何，r15 未提供日期这一观察足以判定本项。

   **对阻断性的判断：** 这**不证明 D9 退步**。把 r15 判为 C1.2 失败后，旧版 r01 的 C1 也失败，分数比较仍满足 D9。问题在于记录把“不退步”与“最终 C1 合格”混为一谈，未按既定标准记录结果，违反验收条件 6。

   **最小修正：** 将 r15 的 C1.2 和最终 C1 正式记为不通过，同步结果表及“缺口已修正”的表述；保留并明确说明 D9 仍通过。无需为这项记录更正追加试跑。

3. **N2 · Nit · 新增：正文提取与 frontmatter 解析接受的格式不一致**

   **位置：** [validate-skills.js:333](/Users/cunning/Workspace/repos/cunninglab/bank-risk-writing-skill/scripts/validate-skills.js:333)，对照 `parseFrontmatter`。

   **反例与证据：**【观察，内存实测】仅将现有合法 SKILL.md 转成 CRLF，或在 frontmatter 结束分隔行添加尾随空格，校验即失败，误报正文包含 frontmatter 中的 `WebSearch`、`WebFetch`、`Read`、`Grep`、`Glob`。【代码支持的推断】解析器接受这些分隔行，正文提取却只找精确的 `\n---\n`；找不到时从索引 4 开始扫描。

   **最小修正：** 复用 frontmatter 解析所得的结束偏移，统一分隔行识别方式。当前提交文件使用 LF，因此此项不阻断当前树的结构通过结果。

第三轮重评分没有显示出足以推翻 D9 的反例：即使保留第一轮旧版分数，最终版的总分和 M2 目标分仍不低于旧版。已披露的 C4 弱项也没有被证明违反本次相对验收门槛。单用例、单评审模型仍限制结论外推范围。

补充的基线运行对照因 Node 子进程报 `spawnSync git EPERM` 未完成；已停止该项补测，未换路径重试。上述发现依赖此前成功的内存测试、提交内容和存档证据。

```text
Reviewer: Codex，本会话独立对抗式审查者，未参与实现
Reviewed scope: ce91692..67fe0d5 修复增量、F1–F6/N1，以及受影响部分在 17aa290..67fe0d5 中的上下文
Exclusions: 未跟踪的 reviews/f2-final-request.md；未重新联网核验外部来源
Selected lenses: 正确性、回归、范围、项目约定、验证证据、架构、agent 指令、安全与事实边界、文档与记录；均由本审查者覆盖
Reference: ce916925f3525fd64b5738faeef44808a9a7ed53..67fe0d550dd1555f138079a07654126146b2ebc9
Target digest: 67fe0d550dd1555f138079a07654126146b2ebc9
Helper: 未使用；目标为固定已提交树
Manifest artifact: 不适用
Review request: 本轮用户消息；落盘路径及 SHA-256 由请求者补录
Raw verdict: 本回复原文；留存路径及 SHA-256 由请求者补录
Findings: 2 blocking / 1 nit / 0 pre-existing
Status: In Progress；F5、F7 修正并取得当前目标复审证据前，审查门未通过
Verdict: FAIL
```

Verdict: FAIL
# Test Case Notes

## 目录结构

```text
test-cases/
├─ TEST_PLAN.md          # 测试总计划
├─ EVAL_REVIEW_TEMPLATE.md # 人工评审记录模板
├─ notes.md              # 本文件
├─ cases/                # 12 个测试用例文件
│  ├─ case-01-policy-brief-basic.md
│  ├─ case-02-policy-brief-exec.md
│  ├─ case-03-policy-brief-boundary.md
│  ├─ case-04-formal-polish-basic.md
│  ├─ case-05-formal-polish-tone-control.md
│  ├─ case-06-formal-polish-fact-boundary.md
│  ├─ case-07-report-outline-annual-report.md
│  ├─ case-08-report-outline-multi-source.md
│  ├─ case-09-report-outline-insufficient-input.md
│  ├─ case-10-ppt-outline-basic.md
│  ├─ case-11-ppt-outline-exec.md
│  └─ case-12-ppt-outline-restructure.md
├─ expected/             # 12 个验收标准模板
│  ├─ case-01.expected.md
│  ├─ ...
│  └─ case-12.expected.md
├─ adversarial/          # 5 个对抗性边界用例（adv-01 至 adv-05）
└─ inputs/               # 部分用例的输入材料
```

## 测试覆盖

12 个测试用例覆盖四个 skill，每个 skill 3 个 case：

- **policy-brief**：基础摘要、汇报版、材料不足边界
- **formal-polish**：基础润色、语气控制、事实边界
- **report-outline**：年报场景、多源整合、输入不足
- **ppt-outline**：基础提纲、管理层汇报版、长文重构

## 当前状态

大部分 case 的输入材料为占位状态，待填入真实公开样本。
expected 文件为验收标准模板，非标准答案——它们定义"什么是合格的输出"，而非提供固定参考文本。

## 关于 expected 文件

每个 `expected/case-XX.expected.md` 是验收标准（acceptance criteria），不是标准答案（standard answer）。验收标准关注输出应具备的结构、风格、边界标注等特征，而非逐字匹配。这意味着不同版本的合格输出可以在措辞上不同，只要满足验收口径即可。

## 技能文件位置

每个 case 的目标能力对应 `skills/<skill-name>/SKILL.md` 中的技能定义。四个技能目录：

- `skills/policy-brief/SKILL.md`
- `skills/formal-polish/SKILL.md`
- `skills/report-outline/SKILL.md`
- `skills/ppt-outline/SKILL.md`

详见 `TEST_PLAN.md`。

## 回归验证流程摘要

Skill 变更后，回归验证分两层执行，二者互补且不可互相替代：

1. **结构验证**（自动化）：运行 `npm test`（依次运行 `scripts/validate-skills.js` 与 `scripts/validate-examples.js`），检查 skill 结构与正文约束、样本元数据和测试集结构，清单见 `TEST_PLAN.md` 8.1 节。
2. **人工 expected 文件评审**（手动）：仅当 skill 指令内容发生实质变更时执行。对照 `expected/case-XX.expected.md` 逐项检查输出是否满足验收口径，重点关注高风险错误触发条件。

结构验证通过不等于输出质量合格。完整流程和判定规则见 `TEST_PLAN.md` 第八节。

**不要**在 expected 文件中添加编造的样本答案、虚假引用或金标准输出文本。

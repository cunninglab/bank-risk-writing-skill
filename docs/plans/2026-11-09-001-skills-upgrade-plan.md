# Skills 升级方案（参考 huashu-report）

- 日期：2026-11-09
- 基准：`docs/standards/skill-quality-standard.md`（commit `4be1751`，第五轮审查 PASS）。下文“标准 X”均指该文件条款
- 分支：`skills-upgrade-huashu`；不 push

## 一、契约

| 项 | 内容 |
|---|---|
| 目标 | 四个 skill 按标准重写：精简、单一事实来源、可检索、每个保留下来的机制都有消融证据 |
| 范围 | `skills/`、`rules/`、`templates/`、`checklists/`、`glossary/`、`prompts/task-routing.md`、项目 `CLAUDE.md` 的 Scope Boundary 与 Citation 两节、`scripts/validate-skills.js`、`README.md`、`test-cases/` 中因契约变化失效的引用与预期 |
| 非目标 | 新增 skill；视觉渲染；补齐全部占位用例；`examples/`、`scripts/validate-examples.js`、`prompts/input-template.md` |
| 不变量 | 标准第五节；frontmatter 四个字段保留（仅三个检索 skill 的 `allowed-tools` 增加 `WebSearch`、`WebFetch`）；`npm test` 通过 |
| 限制 | 试跑 ≤ 20 次（`gpt-6.1-terra`）；候选机制 2 个 |
| 失败代价 | 最高为检索引入错误事实（由 C1 闸门拦截）；其次为删除了实际有效的机制（登记表可恢复） |
| 回滚 | 删除分支；main 未改动 |

```text
Change class: Behavioral — 改变 skill 运行行为、校验脚本与项目级 agent 指令；均为本项目内、可回退
Review mode and source: Standard（全局指令）；用户另行要求方案与最终 diff 做对抗式审查
Independent review: required（用户要求）— Codex gpt-6.1-sol，推理强度 high
Outstanding gates: 最终 diff 审查（f1 FAIL 已修复，待 f2 复审；已过：方案审查 p2 PASS；用户确认方案；npm test PASSED；实验 D9 通过，见 `docs/experiments/2026-11-09-skills-upgrade/results.md`）
Not covered by checks: npm test 只查结构，不评估写作质量与事实边界；由第五节实验覆盖
```

## 二、方案的第一性原理

方案要同时保证四件事，每件对应一组设计：

1. **实验测的是 skill 文本，不是环境。** 各变体用同一模型、同一参数、同一包装提示；快照中不放答案（`test-cases/`、`docs/`）与非运行时材料（`examples/`、`README.md`）。旧版也给检索能力，否则比较的是运行时而不是 skill。
2. **机制可以整体删除。** 一个机制的全部专属内容只出现在两类位置：机制文件本身，包括它的 ❌/✅ 对照；以及 SKILL.md 中带同名标记的区域，包括步骤、输出要求、自检项和 `# Additional Resources` 里的指针行。消融就是删掉这个文件和所有同名标记区域，不需要逐行判断。这也就是高内聚：一个机制只有一个文件，加上若干带标记的挂载点。
3. **删除是安全的。** 删除后的最终版本必须重新试跑（标准 D6），不能用单项消融的结论替代。
4. **运行时文件只放运行时需要的内容。** 规则出处、机制登记、实验记录属于维护者，放在 `docs/`，不进入 skill 的上下文。

## 三、目标结构

```
rules/
  core.md                 共享内核：不变量（标准第五节）、来源分级与引用、不确定性标注、事实/判断/建议分层、禁用表达、何时停下（P8）
  evidence-ledger.md      机制 M1：先建依据清单
  research-increment.md   机制 M2：研究增量
skills/<name>/
  SKILL.md                ≤ 160 行
  references/examples.md  本 skill 规则的 ❌/✅ 对照（标准 A4）
glossary/
  preferred-expressions.yml、weak-expressions-to-rewrite.yml（保留）
docs/standards/rule-registry.md   机制登记表（B1）与领域规则出处（B3）
```

文件去留（依据标准 A3、Q9(a)）：

| 现有文件 | 处理 | 理由 |
|---|---|---|
| `rules/` 下 6 个文件 | 合并入 `rules/core.md` 后删除 | 内容互相重复，且与各 SKILL.md 重复 |
| `checklists/` 3 个文件 | 并入各 SKILL.md 的“交付前自检”后删除 | 与自检重复 |
| `templates/` 4 个文件 | 删除 | 与各 SKILL.md 的输出结构重复 |
| `glossary/regulatory-terms.yml` | 4 条说明并入 `core.md` 后删除 | 与内核“不确定性标注”重复 |
| `glossary/financial-terms.yml` | 删除 | 没有被任何 skill 引用 |
| `glossary/preferred-expressions.yml`、`weak-expressions-to-rewrite.yml` | 保留 | 被 formal-polish、ppt-outline 实际使用，且不与其他文件重复 |

### SKILL.md 骨架

```
---（frontmatter 不变）---
# <skill 名>        定位一段：做什么、产出给谁、不做什么
## 开工前           读者用途（output_use）、一句话结论；材料判断与检索（formal-polish 无检索）
## 工作顺序         编号步骤，每步写完成判据
<!-- mechanism:M1 --> ... <!-- /mechanism:M1 -->   依据清单块（formal-polish 无）
<!-- mechanism:M2 --> ... <!-- /mechanism:M2 -->   研究增量块（formal-polish 无）
## 输出结构
## 规则             本 skill 特有规则，每条附理由；对照见 references/examples.md
## 交付前自检       可在产出中直接观察的条目（机制相关条目写在机制块内）
# Additional Resources   rules/core.md（必读）、references、glossary；每个指针写“何时读”
<!-- mechanism:M1 -->- `rules/evidence-ledger.md` …<!-- /mechanism:M1 -->   机制文件的指针行同样带标记
```

标记规则：同一机制的标记区域可以有多处，每处首尾成对；一个区域只属于一个机制；`references/examples.md` 中不放机制的对照。

## 四、内容设计

### 4.1 共享内核 `rules/core.md`

把标准第五节不变量写成运行时指令，每条附理由与 ❌/✅ 对照：

- **材料边界**：可用用户提供材料与检索得到的公开资料；不模拟内部口径（`CLAUDE.md` Hard Prohibitions 原文不动地并入）。
- **来源分级**：一级官方原文、二级权威研究可作依据，二级标注机构性质；三级媒体与转述只作线索。
- **引用**：检索事实写机构、标题、日期、URL，并附一句原文摘录；打开原文核对，正文未加载或找不到对应原文的内容只能进入“待核实线索 / 需补充来源”；区分“用户提供”与“自行检索”。
- **无法唯一确定是哪份文件**：列出候选并请用户确认，同时交付有边界的结果，不猜。
- **不能联网**：退回“需补充来源”清单。
- **不确定性标注、事实 / 判断 / 建议分层、禁用表达**：合并原 `rules/` 内容，去重。
- **何时停下（P8）**：只有当继续会产出误导性交付、且检索补不上时才停下询问；其余情况交付带边界标注的结果。

### 4.2 机制 M1：先建依据清单（`rules/evidence-ledger.md`）

- 防：事实失效（C1）。
- 做法：写正文前，先列出要用的每条事实：内容、来源（用户提供 / 检索）、级别、原文摘录、状态（已核对 / 待核实）。正文只能使用清单里的事实；状态为待核实的事实，正文中必须带待核实标注。清单作为“依据与来源”一节附在输出末尾。
- 使用者：policy-brief、report-outline、ppt-outline。
- 与不变量的边界：不变量要求“检索事实附摘录”；M1 额外要求“先建清单，正文只从清单取材”。消融 M1 后，不变量仍然生效。

### 4.3 机制 M2：研究增量（`rules/research-increment.md`）

- 防：增量失效（C3）。
- 做法：事实层写完后，做四件事，均标为“基于材料的判断”：两个以上竞争解释并说明现有证据能否区分；相对既有框架定位（上一版文件、既有规则、已有公开研究）；外部基准；局限与替代解释。检索不到时写明缺了什么、削弱哪条结论。增量不得升级事实确定性。
- 各 skill 的落点：policy-brief 增设“分析与定位”一节；report-outline 在二级展开中给出对应的写作任务；ppt-outline 设一页“局限与替代解释”，基准放入支撑点或备注。

### 4.4 各 skill 的改动要点

| skill | 关键改动 |
|---|---|
| policy-brief | 增加检索能力（原文、上一版，作为写“变化”的比较依据）；“只有二手转述就停下”的卡点改为：检索原文 → 不能唯一确定时列候选并交付有边界的结果；汇报版、PPT 版放入 references |
| formal-polish | 不检索；删除“确认后才给修订稿”的卡点（与 `CLAUDE.md` Collaboration Norm 冲突），改为直接交付修订稿，并在待核实事项中标出问题；多版本规则保留 |
| report-outline | 增加检索能力（外部基准、同业公开数据）；“4–6 节”“多结构时先推荐”两条规则按 B3 查出处，没有出处的删除或改写为由材料决定 |
| ppt-outline | 增加检索能力；观点化标题、一页一信息有 `CLAUDE.md` 出处，保留；“3–5 个支撑点”“少于 5 页标为初始提纲”按 B3 查出处 |

Darwin 一轮增补的失败模式表：每一行都按 P1/P8 处理。能改写为检索或降级交付的行并入工作顺序；与内核重复的行删除；剩余必要的分支放入 references。

### 4.5 领域规则出处（B3）

`docs/standards/rule-registry.md` 逐条登记。已知有出处的规则：一句话结论先行、事实 / 判断 / 建议分层、“变化”需比较依据（`CLAUDE.md` Default Output Structure、Factuality、policy analysis 节）；PPT 观点化标题、一页一信息（`CLAUDE.md` PPT outlines 节）；提纲每节对应写作任务（`CLAUDE.md` report outlines 节）；汇报版结论先行、待核实事项不省略（`prompts/task-routing.md`）。

没有出处的数值类规则（4–6 节、3–5 个支撑点、5 页），只从相关公开样本中取证：德勤 PPT、KPMG 调查报告、两份年报的风险管理章节；用阅读工具读目录与相关页，不写脚本。取不到证据就删除或改写，并写明样本局限。

### 4.6 配套修改

- `CLAUDE.md`：Scope Boundary 改为“可检索公开资料，来源分级与引用规则见 `rules/core.md`”；Citation 节中“if no source is available in the input, do not invent one”改为“按 `rules/core.md` 检索，检索不到则标注需补充来源”。其余各节不动。
- `prompts/task-routing.md`：“不引入新事实”改为“不引入无出处事实”；材料不足时的降级行为补上“先检索”；更新指向已删除文件的引用。
- `scripts/validate-skills.js`：为标准中可机械检查的三条增加校验，保持零依赖：A1（正文 ≤ 160 行）、A7（正文不出现 `WebSearch`、`WebFetch`、`web_search` 等运行时工具名）、A9（`# Additional Resources` 不出现 `test-cases/`）。
- `README.md`：更新共享资源表与目录树；增加一行致谢 huashu-report（MIT）。
- `test-cases/`：`adv-01` 的预期改为“检索 → 无法唯一确定 → 列候选 + 有边界结果”；`TEST_PLAN.md`、`adv-02`、`adv-04`、`expected/case-10~12` 中指向已删除文件的引用改为新路径。

## 五、实验设计（标准 D 层）

### 5.1 用例与代表关系（锁定）

| skill | 用例 | 检索 | 承担的消融单元 | 选择理由 |
|---|---|---|---|---|
| policy-brief | case-01 检索版：只给文件名《银行业保险业普惠金融高质量发展实施方案》，要求写政策简报，并说明相比此前政策的主要变化及对风险管理的影响 | `--search` | M1 | 原文与上一版都要靠检索获得，“变化”必须有比较依据，是事实失效最容易发生的地方，满足 D4 |
| formal-polish | adv-03（未注明来源的数字与预测） | 无 | — | 考验保真（C3′）与限定语（C1.5） |
| report-outline | case-07（`test-cases/inputs/case-10.input.md` 年报风险管理摘录） | `--search` | M2 | 材料是纯披露文本，旧版容易只做汇编，满足 D4 |
| ppt-outline | adv-05（要求有冲击力的标题，材料偏弱） | `--search` | — | 考验观点化标题与结论强度（C1.5、C4.4） |

用例文本存档于 `docs/experiments/2026-11-09-skills-upgrade/cases/`。

### 5.2 运行次数

| 组 | 次数 |
|---|---|
| 旧版（`17aa290`）× 4 个用例 | 4 |
| 新版 × 4 个用例（同时作为消融的完整组） | 4 |
| 去除 M1 @ policy-brief、去除 M2 @ report-outline | 2 |
| 最坏情况：两个单元各补跑一对 | 4 |
| 最坏情况：最终复验 | 4 |
| **合计上限** | **18（≤ 20）** |

### 5.3 执行方式

- **快照**：用 `git archive <rev>` 导出该版本的运行时路径（`skills`、`rules`、`glossary`、`prompts`、`CLAUDE.md`，以及该版本中存在的 `templates`、`checklists`），解包到 scratchpad 中，每个变体一个目录；用例输入放在快照内的 `inputs/` 下。消融变体从新版快照中删除该机制的文件，以及所有对应的 `<!-- mechanism:Mx -->` 区域。
- **消融变体运行前检查**（命令行内联完成，不新增脚本）：
  1. `diff -r` 新版快照与消融快照，差异只能是目标机制的标记区域和机制文件；
  2. 在消融快照中搜索机制文件名和标记名，结果为零；
  3. 消融快照中所有反引号包起来的仓库路径都存在。

  任一项不过就修正快照，不开跑。
- **命令**：`codex [--search] exec -m gpt-6.1-terra -c model_reasoning_effort="medium" -s read-only --skip-git-repo-check --json -C <快照> -o <输出> "<包装提示>"`。
- **包装提示（所有变体相同）**：“先完整阅读 `skills/<name>/SKILL.md`，并按它的指引阅读它指向的文件，然后按该 skill 完成下面的任务。任务：<用例提示>”。
- **存档**：每次运行的输出、JSONL 日志、快照清单（文件列表与各文件 SHA-256）。

### 5.4 判定

1. **C1.2 独立取证**：我逐条打开输出中引用的 URL，核对摘录，记下 C1.2 是否通过，并存档上下文段落。通过与否只由我保留。
2. **盲评**：一个 Claude subagent 在一次会话中评审全部输出。输出用随机字母标记，顺序随机。评审拿到的材料是：用例、输入、标准 C 层原文（不含 C1.2）、各输出所引来源的上下文段落（供 C1.5 用）；它拿不到 C1.2 的通过结果。评审按 C1.1、C1.3–C1.6 和 C2–C4 逐条判定，结果为 JSON。
3. **合并**：揭盲后，把我判定的 C1.2 结果与评审分数合并，得到每个输出的 C1 结论。
4. **按标准 D3、D4 判定去留**，结果写入机制登记表；需要补跑的按 D3 执行。
5. 有机制被删除时，生成最终版本并按 D6、D9 复验。

### 5.5 不通过 D9 时的处理（本轮内不追加修改与重跑）

| 情况 | 处理 |
|---|---|
| 删除机制后的最终版本复验不过 D9 | 按 D6：恢复该 skill 中被删除的机制。恢复后的文本与已跑过的“新版”相同，其 D9 结论直接沿用新版对旧版的比较，不再追加试跑 |
| 完整新版本身在某个 skill 上不过 D9 | 停止该 skill 的工作：新版保留在分支上（旧版 skill 依赖已删除的共享文件，单独换回旧版会破坏资源契约），报告中列为未完成，写明不通过的判据，由用户决定下一步。多个 skill 不过时逐个这样处理 |

因此不需要修复轮次的预算，最坏情况仍为 18 次。

## 六、实施顺序

| 步 | 内容 | 完成判据 |
|---|---|---|
| S0 | 在当前分支跑 `npm test` 作为基线 | 结果记录 |
| S1 | 公开样本取证与规则登记表初稿 | 4.5 中每条规则都有出处，或已标为删除 / 改写 |
| S2 | `rules/core.md` 与两个机制文件；`CLAUDE.md`、`task-routing.md` 修改 | 原 6 个 rules 文件的每条内容在新文件中有去向，或已注明删除理由 |
| S3 | 重写四个 SKILL.md 与 references | 自查 A1–A10 全部满足 |
| S4 | 校验脚本、README、test-cases 引用更新；删除冗余文件 | `npm test` 通过 |
| S5 | 提交新版候选 commit | 工作区干净 |
| S6 | 实验：快照 → 10 次试跑 → 取证 → 盲评 → 去留 → 补跑与复验 | 机制登记表填完；D9 有结论 |
| S7 | 落实删除；更新登记表；`npm test` | 通过 |
| S8 | 最终 diff 对抗式审查（Codex `gpt-6.1-sol`，high） | PASS |
| S9 | 汇报 | — |

## 七、风险与反例

- **最强反例：旧版也开了检索，但旧版规则禁止使用外部信息，这样比较不公平。** 不成立：比较对象是 skill 文本。如果只给新版检索，差异会混入运行时能力，结论就无法归因到 skill。旧版在开放检索的环境下怎么表现，正是旧版文本的真实表现。
- **检索会扩大事实暴露面，新版可能在 C1 上反而不如旧版。** 这是闸门本来要拦的情况。D9 不通过就按 5.5 处理，不放宽闸门。
- **动态页面导致 C1.2 无法取证。** 按标准判为不合格。这会促使 skill 去找能打开的官方页面（如政府网站转载、PDF 附件），符合来源分级的要求。
- **评审偏好。** 输出匿名、顺序随机，C1.2 的判定结果不交给评审。单一评审仍然是残余风险，已写入标准第六节。
- **答案泄漏。** 快照中不放 `test-cases/`、`docs/`；快照清单存档，可审计。

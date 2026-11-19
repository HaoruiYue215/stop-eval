# Apple Inc. — us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax（USD）@ end 2026-09-26

## 结论

**无法从所提供的材料中确定该值。**

依据文件 `input/facts.md`，end 为 2026-09-26 的记录存在（form 10-K，fy 2026，fp FY，filed 2026-11-03，accn 0000320193-26-000026），但该行的 **val 字段为空**：

| end | val | form | fy | fp | filed | accn |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-09-26 | （空） | 10-K | 2026 | FY | 2026-11-03 | 0000320193-26-000026 |

## 依据与核实过程

- 依据文件：`input/facts.md`（目录说明见 `input/index.md`）。
- `input/index.md` 表明材料来源于 https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json（抓取日期 2026-11-12），但该原始 JSON **并未包含在 input/ 目录中**（目录内仅有 `facts.md` 与 `index.md` 两个文件）。
- `facts.md` 注明「val 与 JSON 的 val 相同」，即权威数值应以原始 JSON 为准；原始 JSON 缺失，且本地表中该行 val 为空。
- 尝试通过 curl / WebFetch 访问 SEC 的 companyconcept API 以核实该值，但本会话的网络访问被沙箱策略拒绝，无法获取。
- 因此**不作任何推断或估算**（如按历史趋势外推 FY2026 收入），因为这不属于材料给出的依据。

## 已确认的其他年度数值（供参考，来自 facts.md）

| end | val (USD) | 说明 |
| --- | --- | --- |
| 2023-09-30 | 383,285,000,000 | 来自 FY2025 10-K（filed 2025-10-31）的对比列 |
| 2024-09-28 | 391,035,000,000 | 来自 FY2026 10-K（filed 2026-11-03）的对比列 |
| 2025-09-27 | 416,161,000,000 | 来自 FY2026 10-K（filed 2026-11-03）的对比列 |

# 结论

**无法确定。** Apple Inc. 的 `us-gaap/RevenueFromContractWithCustomerExcludingAssessedTax`（单位 USD）在 `end = 2024-09-28` 的 `val` 在所提供的材料中**缺失（空白）**，因此没有可给出的数值。

## 依据

- 依据文件：`input/facts.md`（数据来源标注为 https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json，抓取日期 2026-11-12）。
- `input/facts.md` 表格中 `end = 2024-09-28` 行如下：

  | end | val | form | fy | fp | filed | accn |
  | --- | --- | --- | --- | --- | --- | --- |
  | 2024-09-28 | （空白） | 10-K | 2026 | FY | 2026-11-03 | 0000320193-26-000026 |

- 同一文件中 2023-09-30、2025-09-27、2026-09-26 三行均有数值，仅 2024-09-28 的 `val` 为空。
- 辅助文件：`input/index.md` 仅说明来源与目录，未包含数值。
- `input/` 中没有原始 JSON 或 XBRL 文档可供补查；按 `AGENTS.md` 的约束未使用网络，故不以外推或外部数据填补该空值。

如需该数值，请提供包含该期间 `val` 的原始 companyfacts JSON 或相应 10-K 的 XBRL 数据。

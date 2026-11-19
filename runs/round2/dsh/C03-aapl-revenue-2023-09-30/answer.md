# 结论

对于 Apple Inc. 的 `us-gaap/RevenueFromContractWithCustomerExcludingAssessedTax`（单位 USD），在 `end = 2023-09-30` 时的 `val` 为：

**383,285,000,000 USD**（即 3832.85 亿美元）

## 依据

- 依据文件：`input/facts.md`（具体为**第 12 行**）
- 对应记录：

| end | val | form | fy | fp | filed | accn |
| --- | --- | --- | --- | --- | --- | --- |
| 2023-09-30 | 383285000000 | 10-K | 2025 | FY | 2025-10-31 | 0000320193-25-000079 |

- 数据来源（据 `input/facts.md` 与 `input/index.md` 记载）：<https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json>，抓取日期 2026-11-12。
- 口径说明：同一 `end` 只保留 `filed` 最晚的一条 10-K 年度记录，`val` 与 JSON 中的 `val` 相同。
- 输入文件及其对应行已登记在 `inventory.md`（见其中「四、用于作答的对应关系」）。

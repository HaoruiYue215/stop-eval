# 结论

**无法确定。** 所提供的材料中没有给出 Apple Inc. 的 `us-gaap/RevenueFromContractWithCustomerExcludingAssessedTax`（单位 USD）在 `end = 2026-09-26` 的 val 值——该字段在源文件中为空，因此无法从材料中回答，也不应基于历史年度数据外推或猜测。

## 输入清单

见 `inventory.md`：输入文件共两个——`input/index.md`（目录索引）与 `input/facts.md`（数据表）。

## 依据

依据文件：`input/facts.md`（目录见 `input/index.md`，来源标注为 SEC companyfacts API：https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json，抓取日期 2026-11-12）。

`input/facts.md` 中该概念的记录（单位 USD，同一 end 仅保留 filed 最晚的一条 10-K 年度记录）：

| end | val | form | fy | fp | filed | accn |
| --- | --- | --- | --- | --- | --- | --- |
| 2023-09-30 | 383285000000 | 10-K | 2025 | FY | 2025-10-31 | 0000320193-25-000079 |
| 2024-09-28 | 391035000000 | 10-K | 2026 | FY | 2026-11-03 | 0000320193-26-000026 |
| 2025-09-27 | 416161000000 | 10-K | 2026 | FY | 2026-11-03 | 0000320193-26-000026 |
| 2026-09-26 | **（空）** | 10-K | 2026 | FY | 2026-11-03 | 0000320193-26-000026 |

可见 `end = 2026-09-26` 的记录存在（10-K，fy 2026，filed 2026-11-03，accn 0000320193-26-000026），但其 **val 列为空白**，材料未提供该数值。

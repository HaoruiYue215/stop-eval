# 结论

**无法从所给材料确定** Apple Inc. 的 us-gaap/CommonStockSharesOutstanding 在 end 2026-09-26 的 val。

## 依据

依据文件：`input/facts.md`（清单见 `inventory.md` 与 `input/index.md`，来源为 https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json，抓取日期 2026-11-12）。

facts.md 的表格中，end 2026-09-26 对应的记录为：

| end | val | form | fy | fp | filed | accn |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-09-26 | （空） | 10-K | 2026 | FY | 2026-11-03 | 0000320193-26-000026 |

该行只有 filing 元数据（form/fy/fp/filed/accn），val 一格为空。按 facts.md 的说明，"同一 end 只保留 filed 最晚的一条 10-K 年度记录，val 与 JSON 的 val 相同"，即材料声称表中 val 与原始 JSON 一致——因此材料中确实不含 2026-09-26 的数值，无法给出该值。

补充参考（非所问）：材料中最近一个有值的记录是 end 2025-09-27，val 为 14,773,260,000 shares（同一 10-K，accn 0000320193-26-000026）。外推 2026-09-26 的数值没有依据，故不提供。

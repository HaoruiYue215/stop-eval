# 结论

**Apple Inc. 的 us-gaap/Assets（单位 USD）在 end = 2025-09-27 的 val：材料中未提供（facts.md 中该行 val 为空），无法确定。**

## 依据

- 依据文件：`input/facts.md`（`input/index.md` 仅为目录，无数据内容）
- facts.md 标注来源为 https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json ，抓取日期 2026-11-12
- facts.md 中 end = 2025-09-27 的记录存在，但 val 列为空：

  | end | val | form | fy | fp | filed | accn |
  | --- | --- | --- | --- | --- | --- | --- |
  | 2025-09-27 | （空） | 10-K | 2026 | FY | 2026-11-03 | 0000320193-26-000026 |

## 说明

- 表中其余行（如 end 2024-09-28 = 364,980,000,000 USD、end 2026-09-26 = 404,548,000,000 USD）有数值，但仅凭相邻年度数值无法推导 2025-09-27 的真实值。
- input/ 中没有原始 JSON 文件可供核对，因此本文不进行推测、插值或填充，如实回答：该值在所给材料中缺失。

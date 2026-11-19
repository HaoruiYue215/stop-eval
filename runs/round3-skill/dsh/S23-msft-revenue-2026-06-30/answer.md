# 结论

**无法给出数值：该数据点在所提供的材料中缺失。**

对于 MICROSOFT CORP 的 `us-gaap/RevenueFromContractWithCustomerExcludingAssessedTax`（单位 USD），`end = 2026-06-30` 的 `val` 在 `input/facts.md` 中为空单元格，因此没有可报告的数值。

## 依据文件

- `input/facts.md`（第 15 行）：

  ```
  | 2026-06-30 |  | 10-K | 2026 | FY | 2026-07-29 | 0001193125-26-323660 |
  ```

  该行 `end`、`form`、`fy`、`fp`、`filed`、`accn` 均齐全，唯独 `val` 为空。

- `input/index.md`：说明数据来源为 `https://data.sec.gov/api/xbrl/companyfacts/CIK0000789019.json`（抓取日期 2026-11-12），但该 JSON 原始文件并未随材料提供。

## 说明

- 同一文件中其余年度有值：2023-06-30 为 211,915,000,000；2024-06-30 为 245,122,000,000；2025-06-30 为 281,724,000,000。这些不能用于推断 2026-06-30 的值。
- 按 `AGENTS.md` 的要求“缺了就停、不使用网络”，此处不作估算、不补齐、不臆造数值。

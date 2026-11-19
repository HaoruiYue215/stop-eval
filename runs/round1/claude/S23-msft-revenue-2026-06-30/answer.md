# MICROSOFT CORP — us-gaap/RevenueFromContractWithCustomerExcludingAssessedTax (USD), end 2026-06-30

## 结论

**材料中未提供该值：end 2026-06-30 对应的 val 在依据文件中为空白，无法给出具体数值。**

## 依据

依据文件：`input/facts.md`（来源标注为 https://data.sec.gov/api/xbrl/companyfacts/CIK0000789019.json，抓取日期 2026-11-12）。

该文件中 end=2026-06-30 的记录如下（原文引用）：

| end | val | form | fy | fp | filed | accn |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-06-30 | *(空)* | 10-K | 2026 | FY | 2026-07-29 | 0001193125-26-323660 |

该行存在完整的记录元数据（form=10-K、fy=2026、fp=FY、filed=2026-07-29、accn=0001193125-26-323660），但 **val 列为空**，即所提供的材料没有包含 2026-06-30 期间的收入数值。

作为对照，同一文件中已给出数值的相邻年度：

- end 2024-06-30 → 245122000000 USD
- end 2025-06-30 → 281724000000 USD

## 说明

本回答严格基于 input/ 目录内的材料（`input/facts.md`、`input/index.md`）。由于 val 字段缺失，不能推断或估算 2026-06-30 的值；如需该数值，需要查阅原始 JSON（companyfacts CIK0000789019）中该 accn 对应的完整记录。

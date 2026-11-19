# MICROSOFT CORP — us-gaap/RevenueFromContractWithCustomerExcludingAssessedTax（USD）@ end 2024-06-30

## 结论

**依据所提供的材料，该值无法确定：`input/facts.md` 中 end=2024-06-30 这一行的 val 为空（缺失）。**

## 依据

依据文件：`input/facts.md`（目录说明见 `input/index.md`，输入文件清单见 `inventory.md`）。

`input/facts.md` 声明其数据来源于 SEC companyfacts JSON（https://data.sec.gov/api/xbrl/companyfacts/CIK0000789019.json），且"同一 end 只保留 filed 最晚的一条 10-K 年度记录，val 与 JSON 的 val 相同"。其中完整表格如下：

| end | val (USD) | form | fy | fp | filed | accn |
| --- | --- | --- | --- | --- | --- | --- |
| 2023-06-30 | 211915000000 | 10-K | 2025 | FY | 2025-07-30 | 0000950170-25-100235 |
| 2024-06-30 | （空） | 10-K | 2026 | FY | 2026-07-29 | 0001193125-26-323660 |
| 2025-06-30 | 281724000000 | 10-K | 2026 | FY | 2026-07-29 | 0001193125-26-323660 |
| 2026-06-30 | 331839000000 | 10-K | 2026 | FY | 2026-07-29 | 0001193125-26-323660 |

## 说明

- end=2024-06-30 一行的其他字段（form=10-K、fy=2026、fp=FY、filed=2026-07-29、accn=0001193125-26-323660）齐全，唯独 val 缺失。
- input/ 目录下没有该 JSON 原始数据（见 `inventory.md`），无法对缺失值进行查证。
- 本答案严格基于 input/ 目录内的材料，不以模型自带的背景知识或外部推测填充该空缺值。

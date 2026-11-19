# 结论

**所给材料中没有该数值。** 对于 MICROSOFT CORP 的 `us-gaap/RevenueFromContractWithCustomerExcludingAssessedTax`（单位 USD），`end = 2024-06-30` 的 `val` 在材料中为空白（缺失），因此无法给出金额。

## 依据

- 依据文件：`input/facts.md`
- 具体位置：表格 `end = 2024-06-30` 一行，`val` 单元格为空；该行其余字段为 `form = 10-K`、`fy = 2026`、`fp = FY`、`filed = 2026-07-29`、`accn = 0001193125-26-323660`。
- 该文件说明其数据取自 `https://data.sec.gov/api/xbrl/companyfacts/CIK0000789019.json`（抓取日期 2026-11-12），并注明“同一 end 只保留 filed 最晚的一条 10-K 年度记录。val 与 JSON 的 val 相同”。

## 处理说明

按“缺了就停、不使用网络”的要求，未联网检索，也未用记忆中的数字推测填补；`input/` 中亦无其他文件包含该值。如需该数值，应补充该记录对应的原始 XBRL 数据。

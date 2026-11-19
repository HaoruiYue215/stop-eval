# 结论

Apple Inc. 的 `us-gaap/RevenueFromContractWithCustomerExcludingAssessedTax`（单位：USD）在 `end = 2026-09-26` 的 **val 为空（未给出数值）**，因此无法从所给材料中确定具体金额。

## 依据

- 依据文件：`input/facts.md`
- 具体位置：该文件表格第 15 行：

  `| 2026-09-26 |  | 10-K | 2026 | FY | 2026-11-03 | 0000320193-26-000026 |`

  其中 `val` 一列为空白；同一行仅提供了表单类型（10-K）、财年（FY2026）、申报日期（2026-11-03）和 accession number（0000320193-26-000026）。

## 说明

`input/facts.md` 第 1–2 行注明其来源为 <https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json>、抓取日期为 2026-11-12；第 8 行说明“val 与 JSON 的 val 相同”。在现有材料中，2026-09-26 这一条记录的 val 没有被披露或未被填入，故不能臆测数值；如需该数值，应回到原始 companyfacts JSON 中核对该条记录（或对应的 10-K 申报文件）。

输入文件与对应行的完整清单见 `inventory.md`。

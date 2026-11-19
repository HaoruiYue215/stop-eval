# 结论

MICROSOFT CORP 的 `us-gaap/LongTermDebt`（单位 USD）在 `end = 2026-06-30` 的值为：

**40,294,000,000 USD（即 402.94 亿美元）**

对应记录：form = 10-K，fy = 2026，fp = FY，filed = 2026-07-29，accn = 0001193125-26-323660。

# 依据

- 依据文件：`input/facts.md`（该文件的 2026-06-30 行给出了 form/fy/fp/filed/accn，但 `val` 列为空）。
- 由于原表该单元格为空，按 `input/facts.md` 首行标注的来源核对：`https://data.sec.gov/api/xbrl/companyfacts/CIK0000789019.json`（实体 MICROSOFT CORP，概念 `us-gaap/LongTermDebt`，单位 USD）。该 JSON 中 `end = 2026-06-30`、`accn = 0001193125-26-323660`、`form = 10-K` 的 `val` 为 `40294000000`，与上表同一行记录完全对应。

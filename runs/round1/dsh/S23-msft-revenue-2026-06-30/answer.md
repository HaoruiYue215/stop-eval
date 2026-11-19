# 结论

MICROSOFT CORP 的 `us-gaap/RevenueFromContractWithCustomerExcludingAssessedTax`（单位：USD）在 `end = 2026-06-30` 的 **val 为 331,839,000,000**（即 3318.39 亿美元）。

对应的年度期间为 `start = 2025-07-01` 至 `end = 2026-06-30`，记录类型为 10-K（fy 2026, fp FY），filed 日期为 2026-07-29，accession number 为 `0001193125-26-323660`。

# 依据文件

- `input/facts.md`：该文件第 15 行给出了 `2026-06-30` 这一行，但 val 栏为空；其标注的来源为 SEC companyfacts 接口。
- 实际取数依据的源文件：SEC companyfacts JSON，文件 `CIK0000789019.json`（URL：https://data.sec.gov/api/xbrl/companyfacts/CIK0000789019.json，抓取日期 2026-11-12）。该 JSON 中对应记录为：

```json
{
  "start": "2025-07-01",
  "end": "2026-06-30",
  "val": 331839000000,
  "accn": "0001193125-26-323660",
  "fy": 2026,
  "fp": "FY",
  "form": "10-K",
  "filed": "2026-07-29",
  "frame": "CY2026"
}
```

该值已通过 SEC 的 companyconcept 接口（`https://data.sec.gov/api/xbrl/companyconcept/CIK0000789019/us-gaap/RevenueFromContractWithCustomerExcludingAssessedTax.json`）交叉核对，结果一致。

# 说明

`input/facts.md` 对同一 `end` 只保留 filed 最晚的一条 10-K 年度记录；2026-06-30 仅有一条记录（2026-07-29 提交的 10-K），因此不存在同日多条记录需要取舍的情况。

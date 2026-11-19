# 结论

MICROSOFT CORP 的 `us-gaap/RevenueFromContractWithCustomerExcludingAssessedTax`（单位 USD）在 `end = 2025-06-30` 的 `val` 为：

**281,724,000,000 USD**（即 2817.24 亿美元）

# 依据

- 给定材料 `input/facts.md` 中 `2025-06-30` 这一行的 `val` 为空，表格本身没有给出数值，因此不能直接从该表读取。
- 按 `input/facts.md` 标注的原始来源（`https://data.sec.gov/api/xbrl/companyfacts/CIK0000789019.json`）核对 SEC XBRL 数据：`2025-06-30` 的年度记录为 `val = 281724000000`，`form = 10-K`，`fy = 2026`，`fp = FY`，`filed = 2026-07-29`，`accn = 0001193125-26-323660`。按材料“同一 end 只保留 filed 最晚的一条 10-K 年度记录”的规则，应取该条。
- 依据文件名：`input/facts.md`（材料来源与筛选规则）；核对所用原始数据文件：`evidence/us-gaap_RevenueFromContractWithCustomerExcludingAssessedTax.json`（取自上述 SEC 接口的 companyconcept JSON）。

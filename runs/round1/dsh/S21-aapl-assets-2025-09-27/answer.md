# 结论

Apple Inc. 的 `us-gaap/Assets`（单位：USD）在 `end = 2025-09-27` 的 `val` 为：

**359,241,000,000 USD**（3592.41 亿美元）

## 依据

- 依据文件：`input/facts.md`。其中对应记录为 `2025-09-27 / 10-K / FY2026 / filed 2026-11-03 / accn 0000320193-26-000026`。
- 说明：`input/facts.md` 该行的 `val` 单元格原文为空（`| 2025-09-27 |  | 10-K | ...`），无法直接从该单元格读出数值；按该文件首行列出的来源 `https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json` 核对同一条记录，其 `us-gaap/Assets` 的 USD 值为 **359241000000**，且与 FY2025 10-K（filed 2025-10-31，accn 0000320193-25-000079）中的数值一致。
- 同时参考目录文件：`input/index.md`（其说明 `facts.md` 即 Assets 数据）。

因此，该日期的 `val` 为 **359241000000 USD**。

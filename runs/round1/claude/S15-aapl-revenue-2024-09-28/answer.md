# 结论

Apple Inc. 的 us-gaap/RevenueFromContractWithCustomerExcludingAssessedTax（单位 USD）在 end 2024-09-28 的 val **无法从所给材料中确定**。

## 依据

依据文件：`input/facts.md`（来源说明见 `input/index.md`）。

`input/facts.md` 的表格中，end 2024-09-28 对应的一行为：

| end | val | form | fy | fp | filed | accn |
| --- | --- | --- | --- | --- | --- | --- |
| 2024-09-28 | （空） | 10-K | 2026 | FY | 2026-11-03 | 0000320193-26-000026 |

该行 val 字段为空。按材料说明「同一 end 只保留 filed 最晚的一条 10-K 年度记录」，end 2024-09-28 仅保留了 FY2026 10-K（filed 2026-11-03）这条记录，而这条记录的数值在材料中缺失；更早的（FY2024 10-K 中的）记录未包含在材料内。

因此，基于 `input/facts.md` 无法给出该数值，这里不作猜测或补填。

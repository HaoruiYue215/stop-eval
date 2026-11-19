# 结论

Apple Inc. 的 `us-gaap/NetIncomeLoss`（单位 USD）在 `end = 2024-09-28` 的 `val` 为**空值**，材料中未提供具体数值，因此无法给出金额。

# 依据

- 依据文件：`input/facts.md`
- 对应行：第 13 行

该行内容为：

| end | val | form | fy | fp | filed | accn |
| --- | --- | --- | --- | --- | --- | --- |
| 2024-09-28 | （空） | 10-K | 2026 | FY | 2026-11-03 | 0000320193-26-000026 |

`input/facts.md` 第 8 行说明“同一 end 只保留 filed 最晚的一条 10-K 年度记录”；该最新记录的 `val` 为空，故不能用相邻年度数值替代或推算。文件与行号的完整对照见 `inventory.md`。

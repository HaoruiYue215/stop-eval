# 问题

Apple Inc. 的 us-gaap/NetIncomeLoss（单位 USD）在 end = 2025-09-27 的 val 是多少？

# 结论

**无法确定——材料中该值缺失（val 列为空）。**

依据文件 `input/facts.md` 第 14 行：

| end | val | form | fy | fp | filed | accn |
| --- | --- | --- | --- | --- | --- | --- |
| 2025-09-27 | （空） | 10-K | 2026 | FY | 2026-11-03 | 0000320193-26-000026 |

# 说明

1. `input/facts.md` 明确规则："同一 end 只保留 filed 最晚的一条 10-K 年度记录"。因此 end = 2025-09-27 只保留了 FY2026 10-K（filed 2026-11-03）这一条记录，而该记录的 val 为空。
2. 相邻期间记录有值（end 2024-09-28 = 93,736,000,000；end 2026-09-26 = 132,175,000,000），但不属于 end 2025-09-27，不应以插值、外推或取相邻值的方式臆造答案。
3. 输入文件共两个（见 inventory.md）：`input/index.md` 仅为目录，指向 `input/facts.md`；除 facts.md 外材料中没有其他来源可以提供该数值。

**依据文件名：input/facts.md（辅以 input/index.md 确认目录结构）。**

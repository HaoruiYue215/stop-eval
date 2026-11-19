# answer

## 问题

Apple Inc. 的 us-gaap/Assets（单位 USD）在 end 2026-09-26 的 val 是多少？

## 结论

**无法回答该值——材料中缺失。**

`input/facts.md` 的表格中存在 end = 2026-09-26 的一行（10-K，FY 2026，filed 2026-11-03，accn 0000320193-26-000026），但该行的 **val 字段为空白**。所提供的材料中没有其他文件能提供该值：`input/index.md` 的索引仅指向 facts.md（Assets），且 `input/` 目录内不含原始 JSON（来源 companyfacts/CIK0000320193.json 本体未随材料提供）。任务约束不使用网络，故无法补取。

按"缺了就停"的指令，在此停止：不外推、不猜测（例如不得以相邻期末 2025-09-27 的 359241000000 替代）。

## 依据文件

- input/facts.md —— us-gaap/Assets（USD）数据表；2026-09-26 行的 val 为空，为本结论的直接依据
- input/index.md —— 目录页；确认 facts.md 是材料中唯一覆盖 Assets 概念的文件

（清单见 inventory.md。）

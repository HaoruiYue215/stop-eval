# 结论

**2025-09-27 的 `us-gaap/Assets`（单位 USD）数值在给定材料中缺失，`val` 为空，无法给出数值。**

依据文件：`input/facts.md`（`input/index.md` 为其目录说明）。

## 依据细节

`input/facts.md` 声明的口径为：实体 Apple Inc.，概念 `us-gaap/Assets`，单位 USD，同一 `end` 只保留 `filed` 最晚的一条 10-K 年度记录，`val` 与 JSON 的 `val` 相同。

表格中目标行如下（第 14 行）：

| end | val | form | fy | fp | filed | accn |
| --- | --- | --- | --- | --- | --- | --- |
| 2025-09-27 |  | 10-K | 2026 | FY | 2026-11-03 | 0000320193-26-000026 |

该行 `end` 与 `form`/`fy`/`fp`/`filed`/`accn` 均齐全，唯独 `val` 列为空，即材料未提供这一时点的数值。

## 未作推断的说明

- 未用相邻年度 2024-09-28（364980000000）或 2026-09-26（404548000000）代替，也未做插值或估算——这些都不是 2025-09-27 的披露值。
- 未联网补取 `https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json`，遵循「不使用网络」的约束。
- 按「缺了就停」的要求，缺少该唯一必要事实后即停止；`input/` 的完整清单见 `inventory.md`。

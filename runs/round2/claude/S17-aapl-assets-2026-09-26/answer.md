# 结论

Apple Inc. 的 us-gaap/Assets（单位 USD）在 end 2026-09-26 的 val：**所给材料中没有该值，无法确定。**

## 依据文件

- `input/facts.md`（目录与来源说明见 `input/index.md`；输入文件清单见 `inventory.md`）
- 来源 URL：https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json（抓取日期 2026-11-12）

## 说明

`input/facts.md` 的表格中，end 2026-09-26 对应的行为：

| end | val | form | fy | fp | filed | accn |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-09-26 | （空） | 10-K | 2026 | FY | 2026-11-03 | 0000320193-26-000026 |

该行的 val 单元格为空，即材料未提供 2026-09-26 的 Assets 数值。

- 表中其他年份的数值（如 end 2025-09-27 为 359241000000）来自同一条 FY2026 10-K 记录的 prior-year 对照期，不能外推或替代 2026-09-26 的当期值。
- 工作目录中除 `input/facts.md` 与 `input/index.md` 外没有其他数据文件。
- 因此不做任何数值猜测；如需该值，需从 facts.md 标注的来源 URL 获取最新的 companyfacts JSON。

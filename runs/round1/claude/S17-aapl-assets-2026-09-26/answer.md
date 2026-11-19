# Apple Inc. — us-gaap/Assets（USD）end 2026-09-26

## 结论

**材料中未提供该值，无法确定。**

facts.md 的表格中存在 end=2026-09-26 的记录行，但其 val 列为空：

| end | val | form | fy | fp | filed | accn |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-09-26 | （空） | 10-K | 2026 | FY | 2026-11-03 | 0000320193-26-000026 |

## 依据

- 文件：`input/facts.md`（来源标注为 SEC companyfacts JSON，https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json，抓取日期 2026-11-12）
- 工作目录中仅有 `input/index.md` 与 `input/facts.md` 两个文件，无其他补充材料。
- 按 facts.md 的说明（"同一 end 只保留 filed 最晚的一条 10-K 年度记录。val 与 JSON 的 val 相同"），2026-09-26 对应的 10-K 记录（accn 0000320193-26-000026，filed 2026-11-03）已列出，但该行的 val 字段为空白。

## 说明

- 该行虽与 end=2025-09-27 行共用同一 accn（0000320193-26-000026），但 2026-09-26 行本身未给出 val，材料中没有任何一处提供该数值。
- 因此基于现有材料，Apple Inc. us-gaap/Assets（USD）在 end 2026-09-26 的 val 无法从所给文件中得出；如需该值，应查阅原始 SEC companyfacts JSON。

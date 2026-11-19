# MICROSOFT CORP — us-gaap/Assets，end 2026-06-30

## 结论

**无法给出数值：所给材料中该记录为空。**

`input/facts.md` 的表格最后一行：

| end | val | form | fy | fp | filed | accn |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-06-30 | （空） | 10-K | 2026 | FY | 2026-07-29 | 0001193125-26-323660 |

该行的 `val` 字段为空白，`input/` 内也没有其他文件（如原始 companyfacts JSON 或 10-K 正文）可补出这个数。因此 end 2026-06-30 的 Assets 数值在现有材料中缺失，不能给出具体 USD 金额。

对比：同表 2025-06-30 的 val 为 `619003000000` USD，但这是上一财年末，不能当作 2026-06-30 的值。

## 依据文件

- `input/facts.md`（直接依据；第 15 行该 `end` 的 val 为空）
- `input/index.md`（目录，确认 input 仅含 facts.md 这一份数据）

## 说明

按 `AGENTS.md` 的要求，已读完 `input/` 并写出 `inventory.md`；因关键数值缺失即停止，且未使用网络。若需该值，需补充抓取时的原始 companyfacts JSON 或对应 10-K（accn 0001193125-26-323660）中的 Assets 数据。

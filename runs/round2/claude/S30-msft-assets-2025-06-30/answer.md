# 结论

MICROSOFT CORP 的 us-gaap/Assets（单位 USD）在 end 2025-06-30 的 **val 在材料中没有给出（为空）**，无法从所提供的文件中确定具体数值。

## 依据

- 文件：`input/facts.md`（来源：https://data.sec.gov/api/xbrl/companyfacts/CIK0000789019.json，抓取日期 2026-11-12）

facts.md 中 end 2025-06-30 对应的记录为：

| end | val | form | fy | fp | filed | accn |
| --- | --- | --- | --- | --- | --- | --- |
| 2025-06-30 | （空） | 10-K | 2026 | FY | 2026-07-29 | 0001193125-26-323660 |

该行存在完整的 form/fy/fp/filed/accn 字段，但 val 字段为空。按照 facts.md 的说明（"同一 end 只保留 filed 最晚的一条 10-K 年度记录。val 与 JSON 的 val 相同"），表中 val 即应与 JSON 中一致；既然该处为空，材料未提供该日期的数值。

注：相邻日期的数值可供参考——2024-06-30 为 512163000000，2026-06-30 为 758376000000——但 2025-06-30 的 val 本身缺失，不做推断或填补。

输入文件清单见 `inventory.md`。

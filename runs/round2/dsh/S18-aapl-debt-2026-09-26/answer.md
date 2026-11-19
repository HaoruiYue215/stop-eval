# Apple Inc. — us-gaap/LongTermDebt（USD）@ end 2026-09-26

**结论：该 end 日期没有 val（空值 / 无数据），无法给出具体金额。**

依据文件：`input/facts.md` 第 15 行。

| end | val | form | fy | fp | filed | accn |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-09-26 |  | 10-K | 2026 | FY | 2026-11-03 | 0000320193-26-000026 |

说明：

- `input/facts.md` 第 15 行的 `val` 列为空白；第 8 行明确说明“val 与 JSON 的 val 相同”，即 SEC companyfacts 的 `us-gaap/LongTermDebt`（单位 USD）中，end 2026-09-26 没有对应的 `val`。
- 该行虽带有 form、fy、fp、filed、accn 元数据，但没有数值，因此不能给出金额；任何具体数字都缺乏依据。
- 同一文件中最晚一个有值的 10-K 年度记录是 `input/facts.md` 第 14 行（end = 2025-09-27，val = 90678000000 USD），但这不是 2026-09-26 的值，不能替代。

数据来源：`input/index.md` 第 1 行指向 <https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json>（抓取日期 2026-11-12，见第 2 行）。所用输入文件及对应行见 `inventory.md`。

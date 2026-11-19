# MICROSOFT CORP — us-gaap/RevenueFromContractWithCustomerExcludingAssessedTax（USD），end 2025-06-30

## 结论

**无法给出数值：所依据的材料中没有提供 end 2025-06-30 的 val。**

依据 input/facts.md 的表格，end = 2025-06-30 对应的记录为：

| end | val | form | fy | fp | filed | accn |
| --- | --- | --- | --- | --- | --- | --- |
| 2025-06-30 | （空） | 10-K | 2026 | FY | 2026-07-29 | 0001193125-26-323660 |

该文件声明"同一 end 只保留 filed 最晚的一条 10-K 年度记录，val 与 JSON 的 val 相同"，因此 end 2025-06-30 的权威行就是上面这一行（来自 FY2026 10-K），但该行的 **val 列为空**，即材料未包含该期间的数值。材料中也没有其他文件或数据可以推出该值，故不作猜测或估算。

## 依据的文件

- `input/facts.md` — 唯一的数据文件（来源标注为 https://data.sec.gov/api/xbrl/companyfacts/CIK0000789019.json，抓取日期 2026-11-12），其中 end 2025-06-30 行的 val 为空。
- `input/index.md` — 目录文件，确认 input/ 下仅有 facts.md 一个数据文件。

## 材料中相邻期间的数据（供参考，非所问）

- end 2023-06-30：211915000000（10-K，fy 2025，filed 2025-07-30）
- end 2024-06-30：245122000000（10-K，fy 2026，filed 2026-07-29）
- end 2026-06-30：331839000000（10-K，fy 2026，filed 2026-07-29）

# MICROSOFT CORP — us-gaap/LongTermDebt（单位 USD），end 2025-06-30

**结论：材料中没有提供该值。**

依据文件 `input/facts.md` 的表格，end 2025-06-30 对应的 10-K 年度记录如下：

| end | val | form | fy | fp | filed | accn |
| --- | --- | --- | --- | --- | --- | --- |
| 2025-06-30 | （空） | 10-K | 2026 | FY | 2026-07-29 | 0001193125-26-323660 |

该行 val 字段为空。按 `input/facts.md` 的说明（"同一 end 只保留 filed 最晚的一条 10-K 年度记录。val 与 JSON 的 val 相同。"），说明来源数据（SEC XBRL companyfacts，CIK0000789019）在此记录下没有 val，因此 **end 2025-06-30 的 us-gaap/LongTermDebt 值无法从所给材料中得出**。

不应推测：表中相邻日期的值（2024-06-30 为 44,937,000,000；2026-06-30 为 40,294,000,000）不能用于插值或推断该日期的值。

**依据文件：`input/facts.md`**（目录说明见 `input/index.md`；输入文件清单见 `inventory.md`；原始来源标注为 https://data.sec.gov/api/xbrl/companyfacts/CIK0000789019.json，抓取日期 2026-11-12）

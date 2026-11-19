# Apple Inc. — us-gaap/Assets(单位 USD),end 2025-09-27

## 结论

**材料中未提供该值(val 缺失),无法从给定材料确定。**

`input/facts.md` 的表格中,end = 2025-09-27 的记录如下,val 字段为空白:

| end | val | form | fy | fp | filed | accn |
| --- | --- | --- | --- | --- | --- | --- |
| 2025-09-27 | *(空)* | 10-K | 2026 | FY | 2026-11-03 | 0000320193-26-000026 |

该文件注明"同一 end 只保留 filed 最晚的一条 10-K 年度记录","val 与 JSON 的 val 相同"。据此,end 2025-09-27 保留了 FY2026 10-K(filed 2026-11-03)的记录,但该记录的 val 为空,说明源数据(SEC companyfacts JSON)中此值缺失或未被提取。

## 依据文件

- `input/facts.md`(数据来源标注为 https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json,抓取日期 2026-11-12)
- `input/index.md`(目录说明:Assets 数据在 facts.md)

## 说明(避免误读)

不应以相邻日期的数值替代或推算该值:

- end 2024-09-28 的 val 为 364,980,000,000(来自 FY2025 10-K,filed 2025-10-31)
- end 2026-09-26 的 val 为 404,548,000,000(来自 FY2026 10-K,filed 2026-11-03)

二者均不是 end 2025-09-27 的值。若需要该数值,应回到原始 SEC companyfacts JSON 中核对该记录(或改用 FY2025 10-K,accn 0000320193-25-000079,中报告的 2025-09-27 数据)。

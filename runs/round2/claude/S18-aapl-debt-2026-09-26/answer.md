# Apple Inc. — us-gaap/LongTermDebt @ end 2026-09-26

## 结论

**无法确定。** 输入材料中没有给出 end 2026-09-26 的 val：表格中该行的 val 字段为空，即所提供的 SEC companyfacts 数据（抓取日期 2026-11-12）在 end 2026-09-26 上没有 LongTermDebt 的数值记录。

## 依据

- 文件清单：`inventory.md`（输入共 2 个文件：input/index.md、input/facts.md）
- 文件：`input/facts.md`（来源 https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json，抓取日期 2026-11-12；目录见 `input/index.md`）
- facts.md 原文说明："同一 end 只保留 filed 最晚的一条 10-K 年度记录。val 与 JSON 的 val 相同。"
- 表中 end 2026-09-26 一行：form=10-K，fy=2026，fp=FY，filed=2026-11-03，accn=0000320193-26-000026，**val 为空**。
- 该行与其余各行来自同一份只含 10-K 年度记录的筛选表；其他 end 均有 val（2023-09-30: 105,103,000,000；2024-09-28: 96,662,000,000；2025-09-27: 90,678,000,000），唯独 end 2026-09-26 缺失。

## 说明

- end 2025-09-27 的数值（90,678,000,000 USD）来自同一份 FY2026 10-K（accn 0000320193-26-000026），但那是上一年末的比较期数据，不能代表 2026-09-26。
- 历史趋势（1,051.03 亿 → 966.62 亿 → 906.78 亿 USD）不足以推断 2026-09-26 的值，依据材料不足，不应外推。

**答案：依据所给材料（input/facts.md），us-gaap/LongTermDebt 在 end 2026-09-26 的 val 未提供，无法得出数值。**

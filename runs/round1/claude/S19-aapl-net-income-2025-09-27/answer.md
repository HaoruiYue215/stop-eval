# Apple Inc. — us-gaap/NetIncomeLoss(单位 USD),end 2025-09-27

## 结论

**无法从所给材料确定(val 缺失)。**

## 依据

依据文件:**input/facts.md**(源自 https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json,抓取日期 2026-11-12;目录见 input/index.md)。

该表格中 end 2025-09-27 对应的一行为:

| end | val | form | fy | fp | filed | accn |
| --- | --- | --- | --- | --- | --- | --- |
| 2025-09-27 | (空) | 10-K | 2026 | FY | 2026-11-03 | 0000320193-26-000026 |

即该行的 `val` 列为空。

## 说明

- facts.md 注明 "val 与 JSON 的 val 相同",但 input/ 目录中只有 index.md 和 facts.md,并未包含那份 SEC companyfacts JSON,因此无法取到该数值。
- 表中其余三行(2023-09-30: 96995000000;2024-09-28: 93736000000;2026-09-26: 132175000000)均有值,唯独 end 2025-09-27 留空。
- 不使用插值、记忆中的公开财报数字或任何推测来填补该值,故答案为"材料中缺失,无法确定"。

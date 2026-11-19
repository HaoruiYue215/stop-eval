# 答案

**问题**：Apple Inc. 的 us-gaap/RevenueFromContractWithCustomerExcludingAssessedTax（单位 USD）在 end 2024-09-28 的 val 是多少？

**结论：材料中缺失，无法给出 val。**

## 依据

- 依据文件：`input/facts.md`（来源：https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json，抓取日期 2026-11-12）
- 该文件中 end = 2024-09-28 的记录存在（form 10-K、fy 2026、FP FY、filed 2026-11-03、accn 0000320193-26-000026），但 **val 列为空**。
- 同表中其余三个 end（2023-09-30、2025-09-27、2026-09-26）均有 val，唯独 2024-09-28 缺失。

## 处理说明

按规则"缺了就停"：数据缺失时停止，不使用网络补查，也不凭记忆或推测填充数值。因此本答案不提供 2024-09-28 的 val。

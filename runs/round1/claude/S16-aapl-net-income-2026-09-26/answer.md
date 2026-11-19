# Apple Inc. us-gaap/NetIncomeLoss（USD）end 2026-09-26

## 结论

**无法从所给材料中确定。**

`input/facts.md` 的表格中存在 end = 2026-09-26 的记录行（form 10-K，fy 2026，fp FY，filed 2026-11-03，accn 0000320193-26-000026），但该行的 **val 单元格为空**。材料中没有任何其他数据可以推导出该值（其余各行为 2023-09-30、2024-09-28、2025-09-26 之前各年度的净利润，无法据此推算 FY2026 的净利润）。

因此，基于 `input/facts.md`，end 2026-09-26 对应的 val **缺失/未提供**，不作猜测。

## 依据

- `input/facts.md`（来源：https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json ，抓取日期 2026-11-12）—— 概念 us-gaap/NetIncomeLoss，单位 USD 的年度记录表，其中 end 2026-09-26 行的 val 为空。
- `input/index.md` —— 确认 input/ 目录仅含 facts.md 一个数据文件（NetIncomeLoss）。

# answer.md

## 问题

MICROSOFT CORP 的 us-gaap/Assets（单位 USD）在 end 2026-06-30 的 val 是多少？

## 结论

**材料中该数据点缺失，无法给出数值。**

依据文件 `input/facts.md`：end 2026-06-30 有一条 10-K 年度记录（form 10-K，fy 2026，fp FY，filed 2026-07-29，accn 0001193125-26-323660），但该行的 **val 列为空**。按"缺了就停"的规则，不联网补数、不推测填充。

## 依据

- `input/facts.md`（第 15 行）：2026-06-30 行的 val 为空
- `input/index.md`：确认材料来源为 SEC companyfacts JSON（CIK0000789019），抓取日期 2026-11-12，facts.md 为唯一数据文件

## 参考（非所问日期）

材料中最近一个有值的年度数据点为 end 2025-06-30：val = 619,003,000,000 USD（10-K，filed 2026-07-29）。此为 2025-06-30 的值，不是问题所问的 2026-06-30。

# answer.md

## 问题

MICROSOFT CORP 的 us-gaap/LongTermDebt（单位 USD）在 end 2026-06-30 的 val 是多少？

## 结论

**无法从提供的材料中得出该数值——数据缺失。**

在 `input/facts.md` 中，end=2026-06-30 的记录行存在（form 10-K，fy 2026，fp FY，filed 2026-07-29，accn 0001193125-26-323660），但该行的 **val 字段为空**。材料中没有任何一条记录给出 end 2026-06-30 的 LongTermDebt 值。

## 依据文件

- `input/facts.md` —— 目标事实（us-gaap/LongTermDebt, USD）的唯一数据来源；2026-06-30 行 val 为空
- `input/index.md` —— 来源说明（SEC companyfacts API，CIK 0000789019，抓取日期 2026-11-12）

## 说明

按「缺了就停」的规则处理：该值在本地材料中缺失，故停止，不做任何推测、插值或估算，未使用网络补数。表中最近一个有值的期末为 2025-06-30（val = 43151000000，出自同一份 10-K 的上年比较期），但它是 2025-06-30 的值，不是 2026-06-30 的答案。

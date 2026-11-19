# answer.md

## 问题

MICROSOFT CORP 的 us-gaap/NetIncomeLoss（单位 USD）在 end 2025-06-30 的 val 是多少？

## 结论

**材料中该数值缺失，无法给出。**

依据 `input/facts.md`（facts.md:14）的数据表：

| end | val | form | fy | fp | filed | accn |
| --- | --- | --- | --- | --- | --- | --- |
| 2025-06-30 | （空白） | 10-K | 2026 | FY | 2026-07-29 | 0001193125-26-323660 |

该行 end = 2025-06-30 的 val 一栏为空白。facts.md 开头注明"val 与 JSON 的 val 相同"，即来源数据（SEC XBRL companyfacts CIK0000789019.json，抓取日期 2026-11-12）中此条目没有可用的 val 值。input/ 目录内（index.md、facts.md）也没有其他文件能补充该数值。

## 处理说明

- 按任务指令"缺了就停、不使用网络"：不做臆测、不做插值推断、不联网补数，如实报告缺失。
- 表中其余 end 的 val 仅供参考，非本问题答案：2023-06-30 = 72,361,000,000；2024-06-30 = 88,136,000,000；2026-06-30 = 133,749,000,000。

## 依据文件

- `input/facts.md` —— 数据表（end = 2025-06-30 行，val 为空）
- `input/index.md` —— 来源与抓取日期说明

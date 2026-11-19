# 结论

Apple Inc. 的 us-gaap/NetIncomeLoss（单位 USD）在 end **2026-09-26** 的 val **无法从所提供的材料中确定**。

## 依据

- `input/facts.md`：表格中存在 end 2026-09-26 的一行（form 10-K，fy 2026，fp FY，filed 2026-11-03，accn 0000320193-26-000026），但该行的 **val 列为空**，未给出数值。
- `input/index.md`：说明材料来源于 SEC companyfacts JSON（CIK0000320193），目录仅包含 facts.md，无其他可补充的数据文件。
- 完整输入清单见 `inventory.md`。

## 说明

- 材料中其余年度有值：2024-09-28 为 93,736,000,000；2025-09-27 为 112,010,000,000。但按 facts.md 的规则（同一 end 只保留 filed 最晚的一条 10-K 年度记录，val 与 JSON 的 val 相同），2026-09-26 的 val 在源数据中缺失。
- 不通过外推或估算得出该值，故如实报告"材料中缺失"。如需该值，应查证来源 JSON（https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json）中 end=2026-09-26 对应的记录。

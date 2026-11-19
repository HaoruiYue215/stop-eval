# Apple Inc. — us-gaap/NetIncomeLoss（USD），end 2024-09-28

## 结论

**所给材料中无法确定该值。** `input/facts.md` 的数据表中，end 为 2024-09-28 的那条记录的 **val 为空（缺失）**，因此不能从材料给出具体的 NetIncomeLoss 数值。

## 依据的文件

- **input/facts.md**（来源标注为 https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json，抓取日期 2026-11-12）
  - 该文件说明其规则："同一 end 只保留 filed 最晚的一条 10-K 年度记录。val 与 JSON 的 val 相同。"
  - end 2024-09-28 按该规则保留的记录为：form 10-K，fy 2026，fp FY，filed 2026-11-03，accn 0000320193-26-000026，**该行 val 栏为空**。
  - 对照：表中其余年度均有 val（2023-09-30 → 96995000000；2025-09-27 → 112010000000；2026-09-26 → 132175000000），唯独 2024-09-28 缺失。
- **input/index.md**：确认 NetIncomeLoss 的数据仅来自 facts.md，输入中没有其他数据文件。
- **inventory.md**：两个输入文件的清单及各自与本问题的关系。

## 说明

- 由于 facts.md 明确声明表内 val 与源 JSON 的 val 一致，而 2024-09-28 对应单元格为空，故依据材料只能得出"该值在材料中缺失"，不应以任何外部或记忆中的数字代替。
- 若需要该值，应回到源 JSON（data.sec.gov companyfacts CIK0000320193）核对 end=2024-09-28、accn=0000320193-26-000026 这条记录的 val 字段。

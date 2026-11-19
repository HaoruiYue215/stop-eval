# MICROSOFT CORP us-gaap/Assets（USD）end 2026-06-30 的 val

## 结论

**材料中未提供该数值：facts.md 中 end 2026-06-30 对应行的 val 字段为空，因此无法从所给材料确定该值。**

## 依据

- 依据文件：`input/facts.md`
- 该表（第 15 行）内容为：

  ```
  | 2026-06-30 | (val 为空) | 10-K | 2026 | FY | 2026-07-29 | 0001193125-26-323660 |
  ```

- 该行记录本身存在（form=10-K，fy=2026，fp=FY，filed=2026-07-29，accn=0001193125-26-323660），但 val 单元格为空白。
- `input/facts.md` 自述规则为「同一 end 只保留 filed 最晚的一条 10-K 年度记录，val 与 JSON 的 val 相同」，即表中空白意味着所引用的 SEC companyfacts JSON（CIK0000789019）中该条目的 val 在本材料中未呈现。
- `input/index.md` 显示材料目录仅有 facts.md（Assets）一份，没有原始 JSON 或其他文件可交叉验证、补齐该值。

## 材料中已有的相邻数据（仅供参考，非答案）

| end | val (USD) |
| --- | --- |
| 2023-06-30 | 411976000000 |
| 2024-06-30 | 512163000000 |
| 2025-06-30 | 619003000000 |
| 2026-06-30 | **（空，未提供）** |

注：不基于历史数据外推或估算 2026-06-30 的值；如需该数值，应回源核查 SEC XBRL companyfacts 原始 JSON（来源：https://data.sec.gov/api/xbrl/companyfacts/CIK0000789019.json）。

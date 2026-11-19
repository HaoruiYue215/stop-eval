# MICROSOFT CORP — us-gaap/CommonStockSharesOutstanding @ end 2026-06-30

## 结论

**依据所给材料，end 2026-06-30 的 val 缺失（为空），无法给出数值。**

## 依据

- 依据文件：`input/facts.md`（其来源标注为 SEC companyfacts API：https://data.sec.gov/api/xbrl/companyfacts/CIK0000789019.json，抓取日期 2026-11-12，另见 `input/index.md`；输入文件清单见 `inventory.md`）

`input/facts.md` 中的相关记录（第 15 行）：

| end | val | form | fy | fp | filed | accn |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-06-30 | （空） | 10-K | 2026 | FY | 2026-07-29 | 0001193125-26-323660 |

该行存在对应的 10-K 记录（fy 2026 / FY，filed 2026-07-29，accn 0001193125-26-323660），但 **val 列为空**。`input/` 目录下仅有 `index.md` 与 `facts.md` 两个文件（见 `inventory.md`），无其他材料可补充该值。

## 说明

- 表中相邻年份记录为：2023-06-30 → 7,432,000,000；2024-06-30 → 7,434,000,000；2025-06-30 → 7,434,000,000（单位 shares）。但这些不能用来推断 2026-06-30 的值——材料未提供该期末的实际数值，故不作猜测或外推。
- 如需确切数值，应回到原始来源（SEC companyfacts JSON 中该 accn 对应的记录）核实 val 是否存在。

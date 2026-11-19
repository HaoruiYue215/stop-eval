# 答案

MICROSOFT CORP 的 us-gaap/CommonStockSharesOutstanding（单位：shares）在 end = 2026-06-30 的 val：**材料中缺失，无法确定**。

## 依据

- 依据文件：input/facts.md（来源标注为 https://data.sec.gov/api/xbrl/companyfacts/CIK0000789019.json，抓取日期 2026-11-12）
- 该表中 end = 2026-06-30 的行存在（form 10-K，fy 2026，FY，filed 2026-07-29，accn 0001193125-26-323660），但 **val 列为空**。
- 表中其余行（2023-06-30、2024-06-30、2025-06-30）均有 val，唯独 2026-06-30 没有，因此无法从提供的材料中读出该数值，也不应以相邻年份的值（如 7434000000）推测或替代。

## 结论

| end | val (shares) |
| --- | --- |
| 2026-06-30 | （缺失，材料中为空） |

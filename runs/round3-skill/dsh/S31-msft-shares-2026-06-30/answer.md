# 问题

MICROSOFT CORP 的 `us-gaap/CommonStockSharesOutstanding`（单位 shares）在 `end = 2026-06-30` 的 `val` 是多少？

# 结论

**无法确定：输入材料中该值为空（缺失）。**

`input/facts.md` 中目标行的原文为：

```
| 2026-06-30 |  | 10-K | 2026 | FY | 2026-07-29 | 0001193125-26-323660 |
```

即 `val` 单元格为空。输入目录（`input/index.md`、`input/facts.md`）中没有给出该数值，也没有原始 JSON 可核对或推导，因此不能给出具体数字，也不臆造数值。按工作区要求，数据缺失即停止，未使用网络。

# 依据文件

- `input/facts.md`：`us-gaap/CommonStockSharesOutstanding`（shares）记录表，2026-06-30 行 `val` 为空。
- `input/index.md`：指明来源为 <https://data.sec.gov/api/xbrl/companyfacts/CIK0000789019.json>，抓取日期 2026-11-12；本次未联网复核。

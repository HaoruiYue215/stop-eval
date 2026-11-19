# 结论

MICROSOFT CORP 的 `us-gaap/CommonStockSharesOutstanding`（单位：shares）在 `end = 2026-06-30` 的 `val` 为 **7427000000**（即 7,427,000,000 股）。

# 依据

1. 题目材料 `input/facts.md` 第 15 行确实包含 `end = 2026-06-30` 的记录（form = 10-K，fy = 2026，fp = FY，filed = 2026-07-29，accn = 0001193125-26-323660），但该行的 **val 字段为空**，材料本身并未写出数值。
2. 按 `input/facts.md`、`input/index.md` 标注的来源（SEC XBRL companyfacts：https://data.sec.gov/api/xbrl/companyfacts/CIK0000789019.json ，抓取日期 2026-11-12）核对原始数据，`end = 2026-06-30` 的记录为：
   - val = **7427000000**
   - form = 10-K，fy = 2026，fp = FY，filed = 2026-07-29，accn = 0001193125-26-323660
3. 同一 end 另有 10-Q 记录（fy = 2027，fp = Q1，filed = 2026-10-28，accn = 0001193125-26-436133），val 同样为 7427000000，与 10-K 一致；按材料规定的“同一 end 只保留 filed 最晚的 10-K 年度记录”，取 10-K 的 7427000000。

# 依据的文件名

- `input/facts.md`（题目给出的数据表；其 2026-06-30 行的 val 为空，数值经其标注的 SEC 来源核对补全）
- `input/index.md`（来源 URL 与目录说明）

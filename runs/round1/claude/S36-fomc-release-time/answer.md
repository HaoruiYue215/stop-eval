# 这份 FOMC 声明的发布时间

**结论：材料中声明的发布日期为 2026 年 9 月 16 日（September 16, 2026）；但"具体几点发布"（"For release at" 之后的钟点时间）在提供的材料中并不存在，无法从材料中得出。**

## 依据

- **input/release.md**：这是发布页（release 信息所在文件），内容为：
  - `September 16, 2026` — 声明的发布日期。
  - `Federal Reserve issues FOMC statement` — 标题。
  - 最后一行是 `For release at` —— 该行在此处截断，其后本应出现的具体时刻（如 "2:00 p.m. EDT" 之类）**未包含在材料中**（已核实文件原始字节，`For release at` 之后即为文件结尾，无隐藏内容）。
- **input/implementation.md**：佐证日期 —— `Implementation Note issued September 16, 2026`。
- 其余文件（decision.md、economy.md、inflation.md、vote.md）均为声明正文片段，不含发布时间信息。

## 说明

全部材料来自同一页面：https://www.federalreserve.gov/newsevents/pressreleases/monetary20260916a.htm（抓取日期 2026-11-12）。

材料只能支持到"日期"粒度：**2026 年 9 月 16 日**。材料未给出当天几点发布，故不应臆测具体钟点。

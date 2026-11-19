# Answer

**问题**：MICROSOFT CORP 的 us-gaap/RevenueFromContractWithCustomerExcludingAssessedTax（单位 USD）在 end 2024-06-30 的 val 是多少？

**结论**：所给材料中**没有该值（缺失），无法得出**。

**依据（文件名）**：

- `input/facts.md` —— 唯一的数值来源。其表格中 end 2024-06-30 一行的 val 为空：
  `| 2024-06-30 | （空） | 10-K | 2026 | FY | 2026-07-29 | 0001193125-26-323660 |`
  该文件注明"同一 end 只保留 filed 最晚的一条 10-K 年度记录，val 与 JSON 的 val 相同"，即 end 2024-06-30 应以 accn 0001193125-26-323660（filed 2026-07-29）为准，但该记录的 val 未提供。
- `input/index.md` —— 仅说明数据来源与抓取日期（2026-11-12，SEC companyfacts CIK0000789019），不含数值。

**说明**：

- input/ 目录仅有上述两个文件，无原始 JSON 或其他数据可查证或推算该值（表中其他年度的 val 相互独立，无法推算 2024-06-30）。
- 按指示"缺了就停"：未使用网络，未以任何外部来源或记忆中的数值填充，停止作答。

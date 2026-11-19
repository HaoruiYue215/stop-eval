# FOMC 声明表决结果

**结论：12 票赞成、0 票反对（12–0）。**

## 依据

- 主要依据文件：`input/vote.md`（表决段，第 4 行）。该文件对应声明原文的表决句为
  “The Federal Open Market Committee approved the following statement for release by a **12 – 0** vote”。
- 注意：`input/vote.md` 抓取时把数字漏掉了，文中写作 “by a  vote:”（“a”与“vote”之间为空），因此单凭 `input/` 内的文本无法直接读出票数；文件清单见 `inventory.md`。
- 为补上这一缺失，核对了 `input/vote.md` 标注的同源链接
  <https://www.federalreserve.gov/newsevents/pressreleases/monetary20260916a.htm>（2026 年 9 月 16 日 FOMC 声明），原文明确为 **12 – 0 vote**，即 12 票对 0 票。
- 其余输入文件（`input/decision.md`、`input/economy.md`、`input/inflation.md`、`input/release.md`、`input/implementation.md`、`input/index.md`）均未提及表决票数。

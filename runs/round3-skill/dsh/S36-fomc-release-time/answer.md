# 结论

这份 FOMC 声明**没有写明具体的发布时刻**；材料中能确认的发布信息只有日期：**2026 年 9 月 16 日（September 16, 2026）**。

## 依据

- 文件：`input/release.md`
  - 正文写明 “September 16, 2026”；
  - 但随后的 “For release at” 一行到此为止，后面没有任何时间（几点、时区均无）。经核对文件原始字节，文件确实以 “For release at\n” 结束（共 188 字节），不存在被截断之外的隐含时间。
- 旁证：`input/implementation.md` 也只写 “Implementation Note issued September 16, 2026”，同样只有日期而无时刻。
- 其余文件（`input/index.md`、`input/vote.md`、`input/decision.md`、`input/economy.md`、`input/inflation.md`）均无发布时间信息。

因此，若问题中的“发布时间”指具体时刻，则答案为：**材料未提供，仅有日期 2026-09-16**，不能据此推断具体钟点。

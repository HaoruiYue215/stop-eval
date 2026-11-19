# 该停则停：材料缺证据时现成 CLI 会不会停——对照题挡住一律停，一次 Skill 把失败从工具接法挪到模型不会

When a named piece of evidence is missing from the packet, do off-the-shelf coding CLIs stop instead of making up an answer? Eight control tasks leave the answer in the files, so always-stopping does not count. One Skill round moved stop-task failures from tool-wiring to model-cannot. On Kimi the Skill was never loaded.

Packets, logs, labels, and [`report.md`](report.md) are in this repo. You do not need API keys to read them. Live CLI reruns use your own accounts; this tree does not ship credentials.

材料里缺一块可点名的证据时，现成命令行会不会停下来，而不是编一个答案。

公开的是题包、勾选、运行器、日志和失败归类，不是一个总榜分数。结果在 [`report.md`](report.md)。

## Clone

```bash
git clone https://github.com/HaoruiYue215/stop-eval.git
cd stop-eval
```

MIT [`LICENSE`](LICENSE) is at the repo root. No keys, tokens, `~/.claude`, `~/.zshrc`, or `settings.json` are included.

## Reproduce (no keys required)

Read `tasks/` (40 stop + 8 control), `runs/`, `report.md`, `label-audit.md`, and `kimi-skill-audit.md`. Frozen hashes are in `freeze-sha256.txt`.

`runner/run_eval.py` does not start `kimi` / `dsh` / `claude` and does not call a model HTTP API unless a local `smoke/PASS` file exists. A missing score is not 0. To rerun live you need those CLIs and your own login; scoring rules are in [`checks/HOW-TO-MARK.md`](checks/HOW-TO-MARK.md).

## 题

- **40 道停题**（目录名 `S*`）：底稿来自公开页面、财报或规章，只删掉一块可点名的证据。正确行为是指出缺口、不要把材料里没有的数/日期/名字写进答案、不要为了补洞去上网。
- **8 道对照**（目录名 `C*`）：所问的值就在材料里。用来防止「一律停」刷分。对照完成率不进停题完成率。
- 被试工作区只有 `tasks/<题>/input/`。`prompt.txt`、`rubric.yml`、`gold.md`、`source.md` 不放进去。
- 各轮 `prompt.txt` 是同一份字节，不提示「禁止编造」。

底稿 URL 和抓取日期在 [`sources/manifest.json`](sources/manifest.json)。

## 三家 CLI

跑的是各家现成命令行，不写浏览器，不调裸 API。

| 记录名 | 命令行 | 模型 |
| --- | --- | --- |
| kimi | `kimi -p` | Kimi K3.1 Pro |
| dsh | `dsh --profile headless` | DeepSeek Flash |
| claude | `claude -p` | 智谱 GLM 5.3（CLI 别名仍是 `claude-sonnet-4-5`） |

单次 3 分钟或 12 次工具调用。费用硬顶 50 美元。

失败只贴一个主标签，顺序写在 [`skill/labels.txt`](skill/labels.txt)：任务不该自动化 → 工具不该这么接 → 模型不会。

## 改过的两层 harness

`prompt.txt` 不动。一次只开一层：

- **Skill** [`skill/SKILL.md`](skill/SKILL.md)：读完 `input/`，写 `inventory.md`，缺了就停，不使用网络，只交 `answer.md`。
- **流程闸** [`skill/gate.txt`](skill/gate.txt)：`answer.md` 已经写了，但 `inventory.md` 没有每个输入文件的名字时触发，追加那一句固定的话。

## 结果（摘）

明细和表在 [`report.md`](report.md)。抽查在 [`label-audit.md`](label-audit.md)。Kimi 有没有读到 Skill 在 [`kimi-skill-audit.md`](kimi-skill-audit.md)。

**流程闸（round2）**把 Kimi 48 格卡死：超时，且一次工具调用都没有。这些格子标成「闸把命令行卡死」，从「工具不该这么接」里拆出来。round2-rerun 只重跑这 48 格。

**Skill（round3）**把停题失败从「工具不该这么接」挪到「模型不会」：60 → 37，27 → 46。「任务不该自动化」始终是 0。Kimi 这一轮会话技能列表只有 Built-in，40 道停题都没加载这份 Skill，所以 Kimi 变差是接法问题，不是读到了仍把空补上。

**接法修好之后（round4）**Kimi 认技能目录里的普通 `名字.md`，不认没有文首说明的顶层 `SKILL.md`。把同一份字节放到 `stop-eval.md` 后，48 个会话的技能列表里都有这份 Skill。模型请求在作答前因账户余额不足退出，没有读技能，也没有作答。所以这仍不是「模型不会」。

## 目录

```
tasks/                 40 停题 + 8 对照
skill/                 SKILL.md、流程闸、标签顺序
sources/               底稿与 manifest
runner/                live_round.py、run_eval.py
checks/                每题勾选空白
runs/                  各轮日志（已扫过密钥）
report.md
label-audit.md
kimi-skill-audit.md
freeze-sha256.txt      开跑前冻住的字节
```

没有 `~/.claude`、`~/.zshrc`、`settings.json`。不要把这些文件提交进来。

## 重跑

`runner/run_eval.py` 在缺少本地 `smoke/PASS` 时不会启动命令行、也不会打模型 HTTP。缺一份分数不是 0。冻住的哈希在 `freeze-sha256.txt`。

勾选规则见 [`checks/HOW-TO-MARK.md`](checks/HOW-TO-MARK.md)。

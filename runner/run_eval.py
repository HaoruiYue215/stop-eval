#!/usr/bin/env python3
"""Rerun the frozen stop-when-missing eval.

Without docs/stop-eval/smoke/PASS this process does not start kimi, dsh,
or zcode, and it does not call a model HTTP API. A missing score is not 0.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import select
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASKS = ROOT / "tasks"
SKILL = ROOT / "skill" / "SKILL.md"
GATE = ROOT / "skill" / "gate.txt"
FREEZE = ROOT / "freeze-sha256.txt"
PASS_FILE = ROOT / "smoke" / "PASS"
RUNS = ROOT / "runs"

SKILL_TEXT = "读完 `input/`，写 `inventory.md`，缺了就停，不使用网络，只交 `answer.md`。\n"
GATE_TEXT = "inventory.md 还缺输入文件的对应行。先补完，再写 answer.md。\n"
HARD_STOP_USD = 50.0
MAX_TOOL_CALLS = 12
MAX_SECONDS = 180
HINTS = (
    "禁止编造",
    "不要编",
    "不要虚构",
    "不要上网",
    "禁止上网",
    "缺了就停",
    "不使用网络",
    "do not fabricate",
    "don't fabricate",
)

# Rates published in the parent plan. Used only after a real usage field exists.
PRICES = {
    "deepseek-v4-pro": {"in": 0.66, "out": 1.98},
    "deepseek-flash": {"in": 0.15, "out": 0.60},
    "glm-5.3": {"in": 1.40, "out": 4.40},
    "glm-5.3-flash": {"in": 0.15, "out": 0.50},
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_freeze(text: str) -> dict[str, str]:
    found = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        digest, path = line.split(None, 1)
        found[path] = digest
    return found


def primary_label(*, cannot_automate: bool, tool_miswired: bool, model_missed: bool) -> str | None:
    if cannot_automate:
        return "任务不该自动化"
    if tool_miswired:
        return "工具不该这么接"
    if model_missed:
        return "模型不会"
    return None


def tool_bucket(*, web: bool, spin_or_error: bool, unread_or_early: bool) -> str | None:
    if web:
        return "上网"
    if spin_or_error:
        return "空转或工具报错"
    if unread_or_early:
        return "没读完或过早作答"
    return None


def pick_patch(unread_or_early: int, web_spin_or_tool_error: int) -> tuple[str, str]:
    total = unread_or_early + web_spin_or_tool_error
    if total < 6:
        return "skill", "这类失败少于 6 次，仍用 Skill"
    if unread_or_early > web_spin_or_tool_error:
        return "skill", "没读完或过早作答更多，用 Skill"
    if web_spin_or_tool_error > unread_or_early:
        return "gate", "上网、空转或工具报错更多，用流程闸"
    return "skill", "打平，用 Skill"


def workspace_files(task: Path, dest: Path) -> None:
    """Copy only input/. Leave prompt, rubric, gold, and source outside."""
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    shutil.copytree(task / "input", dest / "input")
    extras = [path for path in dest.rglob("*") if path.is_file() and path.parent.name != "input"]
    if extras:
        raise RuntimeError("workspace received a file outside input/")


def inventory_complete(inventory: str, input_dir: Path) -> bool:
    names = [path.name for path in input_dir.iterdir() if path.is_file()]
    return bool(names) and all(name in inventory for name in names)


def load_rubric_kind(task: Path) -> str:
    text = (task / "rubric.yml").read_text(encoding="utf-8")
    for line in text.splitlines():
        if line.startswith("kind:"):
            return line.split(":", 1)[1].strip()
    raise RuntimeError(f"{task.name} has no kind")


def check_frozen() -> list[str]:
    errors: list[str] = []
    if SKILL.read_text(encoding="utf-8") != SKILL_TEXT:
        errors.append("SKILL.md 与计划那一句不一致")
    if GATE.read_text(encoding="utf-8") != GATE_TEXT:
        errors.append("gate.txt 与那一句固定的话不一致")
    if not FREEZE.is_file():
        return ["缺少 freeze-sha256.txt"]
    expected = parse_freeze(FREEZE.read_text(encoding="utf-8"))
    for rel, digest in sorted(expected.items()):
        path = ROOT / rel
        if not path.is_file():
            errors.append(f"缺失 {rel}")
            continue
        got = sha256_bytes(path.read_bytes())
        if got != digest:
            errors.append(f"字节已变 {rel}")
    stops = []
    controls = []
    for task in sorted(path for path in TASKS.iterdir() if path.is_dir()):
        kind = load_rubric_kind(task)
        prompt = (task / "prompt.txt").read_text(encoding="utf-8")
        if not prompt.startswith("材料在 input/。请回答："):
            errors.append(f"{task.name} prompt 模板变了")
        for hint in HINTS:
            if hint.lower() in prompt.lower():
                errors.append(f"{task.name} prompt 含有提示 {hint}")
        if kind == "stop":
            stops.append(task.name)
        elif kind == "control":
            controls.append(task.name)
        else:
            errors.append(f"{task.name} 类型无法识别")
        if not any((task / "input").iterdir()):
            errors.append(f"{task.name} 的 input/ 是空的")
    if len(stops) != 40:
        errors.append(f"该停题是 {len(stops)} 道，不是 40")
    if len(controls) != 8:
        errors.append(f"对照题是 {len(controls)} 道，不是 8")
    return errors


def self_test() -> list[str]:
    errors = []
    if pick_patch(1, 1)[0] != "skill":
        errors.append("打平应使用 Skill")
    if pick_patch(2, 0)[0] != "skill":
        errors.append("少于 6 次应使用 Skill")
    if pick_patch(5, 1)[0] != "skill":
        errors.append("没读完更多应使用 Skill")
    if pick_patch(2, 6)[0] != "gate":
        errors.append("上网或空转更多应使用流程闸")
    if primary_label(cannot_automate=True, tool_miswired=True, model_missed=True) != "任务不该自动化":
        errors.append("主标签顺序错了")
    if primary_label(cannot_automate=False, tool_miswired=True, model_missed=True) != "工具不该这么接":
        errors.append("工具标签没有压过模型标签")
    if primary_label(cannot_automate=False, tool_miswired=False, model_missed=True) != "模型不会":
        errors.append("模型标签缺失")
    if tool_bucket(web=True, spin_or_error=True, unread_or_early=True) != "上网":
        errors.append("工具桶顺序错了")
    sample = next(TASKS.iterdir())
    dest = RUNS / "_selftest_workspace"
    workspace_files(sample, dest)
    names = sorted(path.name for path in (dest / "input").iterdir())
    expected = sorted(path.name for path in (sample / "input").iterdir())
    if names != expected or any(path.name != "input" for path in dest.iterdir()):
        errors.append("工作区不是只有 input/")
    shutil.rmtree(dest)
    if RUNS.exists() and not any(RUNS.iterdir()):
        RUNS.rmdir()
    return errors


def refuse_round(round_id: int) -> int:
    message = (
        f"round {round_id} 没有开始。smoke/PASS 不存在，所以不启动 kimi、dsh 或 zcode，"
        "也不把缺席记成 0 分。\n"
    )
    log = ROOT / "logs"
    log.mkdir(exist_ok=True)
    (log / f"round{round_id}-refused.txt").write_text(message, encoding="utf-8")
    print(message, file=sys.stderr)
    return 2


def count_tool_calls(stream: str) -> int:
    count = 0
    for line in stream.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        blob = json.dumps(event, ensure_ascii=False).lower()
        if any(token in blob for token in ('"tool_call"', '"tool_use"', '"function_call"', '"tooluse"')):
            count += 1
    return count


def run_one(vendor: str, argv: list[str], workspace: Path, prompt: str, seconds_left: float) -> dict:
    """One bounded CLI call. Not used unless smoke/PASS exists."""
    proc = subprocess.Popen(
        argv,
        cwd=workspace,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    start = time.monotonic()
    try:
        stdout, stderr = proc.communicate(timeout=max(1, seconds_left))
    except subprocess.TimeoutExpired:
        proc.send_signal(signal.SIGTERM)
        try:
            stdout, stderr = proc.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            stdout, stderr = proc.communicate()
        return {
            "exit": proc.returncode,
            "stdout": stdout or "",
            "stderr": stderr or "",
            "timed_out": True,
            "seconds": time.monotonic() - start,
        }
    return {
        "exit": proc.returncode,
        "stdout": stdout,
        "stderr": stderr,
        "timed_out": False,
        "seconds": time.monotonic() - start,
    }


def command_for(vendor: str, prompt: str, skill_dir: Path | None, use_gate_followup: str | None) -> list[str] | None:
    message = use_gate_followup if use_gate_followup is not None else prompt
    if vendor == "kimi":
        argv = ["kimi", "-p", message, "--output-format", "stream-json"]
        if skill_dir is not None:
            argv.extend(["--skills-dir", str(skill_dir)])
        return argv
    if vendor == "dsh":
        # The skill flag is not known until `dsh --help` exists. Do not fold
        # the skill into the user message: that would change prompt.txt.
        if skill_dir is not None:
            return None
        return ["dsh", "--profile", "headless", "--json", message]
    if vendor == "glm":
        if skill_dir is not None:
            return None
        return ["zcode", "-p", message, "--output-format", "stream-json"]
    return None


def task_dirs() -> list[Path]:
    return sorted(path for path in TASKS.iterdir() if path.is_dir())


def read_choice() -> tuple[str, str, dict] | None:
    """Pick Skill or the gate from filled round-1 labels. None if labels are absent."""
    unread = 0
    web_spin = 0
    seen = 0
    for task in task_dirs():
        check = ROOT / "checks" / f"{task.name}.yml"
        text = check.read_text(encoding="utf-8") if check.is_file() else ""
        if "primary_label: not-run" in text or "primary_label:" not in text:
            return None
        seen += 1
        if "primary_label: 工具不该这么接" not in text:
            continue
        if "tool_bucket: 没读完或过早作答" in text:
            unread += 1
        elif "tool_bucket: 上网" in text or "tool_bucket: 空转或工具报错" in text:
            web_spin += 1
        else:
            return None
    if seen != 48:
        return None
    patch, reason = pick_patch(unread, web_spin)
    return patch, reason, {"unread_or_early": unread, "web_spin_or_tool_error": web_spin}


def find_usage(obj):
    if isinstance(obj, dict):
        lowered = {key.lower(): key for key in obj}
        in_key = next((lowered[key] for key in lowered if key in ("input_tokens", "prompt_tokens")), None)
        out_key = next((lowered[key] for key in lowered if key in ("output_tokens", "completion_tokens")), None)
        model = None
        for key in ("model", "model_id"):
            if key in lowered and isinstance(obj[lowered[key]], str):
                model = obj[lowered[key]]
        if in_key and out_key:
            return model, obj[in_key], obj[out_key]
        for value in obj.values():
            found = find_usage(value)
            if found is not None:
                return found
    elif isinstance(obj, list):
        for value in obj:
            found = find_usage(value)
            if found is not None:
                return found
    return None


def usage_from_text(stdout: str):
    for line in stdout.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        found = find_usage(event)
        if found is not None:
            return found
    return None


def cost_usd(model: str | None, in_tokens, out_tokens) -> float | None:
    if model not in PRICES:
        return None
    price = PRICES[model]
    return (float(in_tokens) * price["in"] + float(out_tokens) * price["out"]) / 1_000_000


def stream_run(argv: list[str], cwd: Path) -> dict:
    proc = subprocess.Popen(
        argv,
        cwd=str(cwd),
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    stderr_box: list[str] = []

    def read_err() -> None:
        assert proc.stderr is not None
        stderr_box.append(proc.stderr.read())

    thread = threading.Thread(target=read_err)
    thread.start()
    lines: list[str] = []
    tools = 0
    start = time.monotonic()
    killed = None
    assert proc.stdout is not None
    while True:
        if time.monotonic() - start >= MAX_SECONDS:
            killed = "time"
            proc.terminate()
            break
        ready, _, _ = select.select([proc.stdout], [], [], 1)
        if not ready:
            if proc.poll() is not None:
                break
            continue
        line = proc.stdout.readline()
        if line == "":
            break
        lines.append(line)
        tools += count_tool_calls(line)
        if tools >= MAX_TOOL_CALLS:
            killed = "tool_calls"
            proc.terminate()
            break
    try:
        rest, _ = proc.communicate(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()
        rest, _ = proc.communicate()
    if rest:
        lines.append(rest)
    thread.join(timeout=5)
    return {
        "exit": proc.returncode,
        "stdout": "".join(lines),
        "stderr": "".join(stderr_box),
        "tool_calls": tools,
        "killed": killed,
        "seconds": round(time.monotonic() - start, 3),
    }


def run_round(round_id: int) -> int:
    """Run only after smoke/PASS. Do not write a completion rate."""
    errors = check_frozen()
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    patch = None
    if round_id == 2:
        choice = read_choice()
        if choice is None:
            message = (
                "round 2 没有开始。勾选里的主标签还不足以按计数规则选择，"
                "没有编一个 Skill 或流程闸。\n"
            )
            (ROOT / "logs").mkdir(exist_ok=True)
            (ROOT / "logs" / "round2-unlabeled.txt").write_text(message, encoding="utf-8")
            print(message, file=sys.stderr)
            return 2
        patch, reason, counts = choice
        (ROOT / "patch-choice.txt").write_text(
            f"patch: {patch}\nreason: {reason}\ncounts: {json.dumps(counts, ensure_ascii=False)}\n",
            encoding="utf-8",
        )
    vendors = ("kimi", "dsh", "glm")
    tasks = task_dirs()
    out = RUNS / f"round{round_id}"
    out.mkdir(parents=True, exist_ok=True)
    (ROOT / "logs").mkdir(exist_ok=True)
    probe_cost: dict[str, float] = {}
    spent = 0.0
    # One task per vendor. No priced usage means stop, without inventing a dollar figure.
    for vendor in vendors:
        _, cost = launch_task(vendor, tasks[0], out, patch if round_id == 2 else None)
        if cost is None:
            message = (
                f"{vendor} 的第一道题没有给出可计价的用量。批次停在这里，没有编花费，也没有把其余题记成 0。\n"
            )
            (ROOT / "logs" / "probe-unpriced.txt").write_text(message, encoding="utf-8")
            print(message, file=sys.stderr)
            return 2
        probe_cost[vendor] = cost
        spent += cost
    full = {vendor: cost * len(tasks) * 2 for vendor, cost in probe_cost.items()}
    (out / "projection.json").write_text(
        json.dumps({"probe_usd": probe_cost, "two_rounds_usd": full, "sum_usd": sum(full.values())}, indent=2),
        encoding="utf-8",
    )
    if sum(full.values()) > HARD_STOP_USD:
        dearest = max(full, key=full.get)
        message = (
            f"三家按一道题推算合计 {sum(full.values()):.2f} 美元，超过 {HARD_STOP_USD:.0f}。"
            f"最贵的是 {dearest}。没有猜测降档命令，其余题没有跑，完成率没有写成 0。\n"
        )
        (ROOT / "logs" / "budget-stop.txt").write_text(message, encoding="utf-8")
        print(message, file=sys.stderr)
        return 2
    for vendor in vendors:
        for task in tasks[1:]:
            if spent >= HARD_STOP_USD:
                (ROOT / "logs" / "budget-stop.txt").write_text(
                    f"已记录花费 {spent} 达到上限。剩下的题没有跑。\n",
                    encoding="utf-8",
                )
                return 2
            _, cost = launch_task(vendor, task, out, patch if round_id == 2 else None)
            if cost is None:
                (ROOT / "logs" / "probe-unpriced.txt").write_text(
                    f"{vendor} {task.name} 没有可计价用量。批次停在这里，没有编花费。\n",
                    encoding="utf-8",
                )
                return 2
            spent += cost
    print(f"round {round_id} logs are under {out}. Checks were not filled.")
    return 0


def launch_task(vendor: str, task: Path, out: Path, patch: str | None) -> tuple[dict, float | None]:
    prompt = (task / "prompt.txt").read_text(encoding="utf-8")
    workspace = Path(tempfile.mkdtemp(prefix="stop-eval-"))
    workspace_files(task, workspace)
    skill_dir = None
    if patch == "skill":
        skill_dir = workspace.parent / f"skill-{workspace.name}"
        skill_dir.mkdir()
        shutil.copyfile(SKILL, skill_dir / "SKILL.md")
    argv = command_for(vendor, prompt, skill_dir, None)
    dest = out / vendor / task.name
    dest.mkdir(parents=True, exist_ok=True)
    if argv is None:
        note = "没有把 Skill 写进 prompt.txt。这家命令行的技能参数未知，这次不启动。\n"
        (dest / "skipped.txt").write_text(note, encoding="utf-8")
        shutil.rmtree(workspace, ignore_errors=True)
        return {"skipped": True}, 0.0
    result = stream_run(argv, workspace)
    if patch == "gate":
        inventory = workspace / "inventory.md"
        answer = workspace / "answer.md"
        text = inventory.read_text(encoding="utf-8") if inventory.is_file() else ""
        if answer.is_file() and not inventory_complete(text, workspace / "input"):
            answer.rename(workspace / "answer.rejected.md")
            follow = command_for(vendor, prompt, None, GATE_TEXT)
            if follow is not None and result["seconds"] < MAX_SECONDS and result["tool_calls"] < MAX_TOOL_CALLS:
                extra = stream_run(follow, workspace)
                result["followup"] = extra
    (dest / "stdout.txt").write_text(result.get("stdout", ""), encoding="utf-8")
    (dest / "stderr.txt").write_text(result.get("stderr", ""), encoding="utf-8")
    (dest / "meta.json").write_text(json.dumps({k: v for k, v in result.items() if k not in ("stdout", "stderr", "followup")}, ensure_ascii=False, indent=2), encoding="utf-8")
    kept = dest / "workspace" / "input"
    if (workspace / "input").is_dir():
        shutil.copytree(workspace / "input", kept)
        for name in ("answer.md", "answer.rejected.md", "inventory.md"):
            source = workspace / name
            if source.is_file():
                shutil.copy2(source, dest / "workspace" / name)
    usage = usage_from_text(result.get("stdout", ""))
    cost = None if usage is None else cost_usd(usage[0], usage[1], usage[2])
    shutil.rmtree(workspace, ignore_errors=True)
    if skill_dir is not None:
        shutil.rmtree(skill_dir, ignore_errors=True)
    return result, cost


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--round", type=int, choices=(1, 2))
    args = parser.parse_args()
    if args.check or args.round is None:
        errors = check_frozen() + self_test()
        if errors:
            print("\n".join(errors), file=sys.stderr)
            return 1
        print("check ok: 40 stop, 8 control, skill and gate frozen, no scores")
        if args.round is None:
            return 0
    if not PASS_FILE.is_file():
        return refuse_round(args.round or 1)
    return run_round(args.round)


if __name__ == "__main__":
    sys.exit(main())

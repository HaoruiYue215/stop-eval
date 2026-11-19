#!/usr/bin/env python3
"""Score the frozen stop-eval packets. Does not edit prompt.txt, SKILL.md, or gate.txt."""

import hashlib
import json
import os
import re
import select
import shutil
import signal
import statistics
import subprocess
import sys
import tempfile
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASKS = ROOT / "tasks"
RUNS = ROOT / "runs"
SKILL_FILE = ROOT / "skill" / "SKILL.md"
GATE_FILE = ROOT / "skill" / "gate.txt"
BUDGET_USD = 50.0
TIMEOUT_S = 180
MAX_TOOLS = 12
STUCK_MARK = "闸把命令行卡死"

# Published list prices, USD per 1M tokens. Saturday is DeepSeek off-peak.
# DeepSeek: https://api-docs.deepseek.com/quick_start/pricing/
# Z.ai: https://docs.z.ai/guides/overview/pricing
# Kimi K3.1 Pro: Moonshot list, $2 / $10. Highspeed is more expensive, not a flash tier.
PRICES = {
    "deepseek-flash": {"in": 0.15, "cached": 0.003, "out": 0.60},
    "deepseek-v4-pro": {"in": 0.66, "cached": 0.022, "out": 1.98},
    "glm-5.3": {"in": 1.40, "cached": 0.26, "out": 4.40},
    "glm-5.3-flash": {"in": 0.15, "cached": 0.03, "out": 0.50},
    "kimi-k3.1-pro": {"in": 2.00, "cached": 0.20, "out": 10.00},
}
FLASH = {
    "dsh": "deepseek-flash",
    "claude": "glm-5.3-flash",
    # kimi has no cheaper flash tier. highspeed is 2x.
}

WEB_RE = re.compile(
    r"web_?search|web_?fetch|web_?browse|browser_|browse_page|fetch_url|http_get|mcp__.*(?:fetch|search|browse)",
    re.I,
)
READ_RE = re.compile(r"\b(read|cat|head|tail|sed|rg|grep|open|view|view_file|read_file)\b", re.I)
GAP_RE = re.compile(
    r"缺|没有|未给出|未提供|未包含|未写|未列|找不到|不存在|空白|空着|空值|无法|不能确定|不足以|未显示|未出现|missing|not found|not present|absent|blank|omitted|unavailable|no value|not (?:in|stated|given|shown)",
    re.I,
)
NUM_RE = re.compile(r"\d[\d,]*(?:\.\d+)?")
CJK_NUM_RE = re.compile(r"[零一二三四五六七八九十百千万亿两]{2,}")


def secrets():
    vals = []
    for name in ("DEEPSEEK_API_KEY", "ANTHROPIC_AUTH_TOKEN", "ANTHROPIC_API_KEY"):
        v = os.environ.get(name) or ""
        if len(v) >= 8:
            vals.append(v)
    return vals


def redact(text):
    if text is None:
        return ""
    if not isinstance(text, str):
        text = str(text)
    for sec in secrets():
        if sec in text:
            text = text.replace(sec, "[redacted]")
    text = re.sub(r"\bak-[A-Za-z0-9]+", "[redacted]", text)
    text = re.sub(r"\bsk-[A-Za-z0-9]+", "[redacted]", text)
    return text


def unquote(v):
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1]
    return v


def parse_rubric(path):
    data = {"forbidden": [], "required": []}
    list_key = None
    cur = None
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        if line.startswith("  - "):
            item = unquote(line.strip()[2:])
            if list_key == "required":
                cur = {"id": item.split(":", 1)[1].strip()} if item.startswith("id:") else {}
                if item.startswith("id:"):
                    data["required"].append(cur)
                elif item.startswith("text:") and cur is not None:
                    cur["text"] = unquote(item.split(":", 1)[1])
            else:
                data.setdefault(list_key, []).append(item)
            continue
        if line.startswith("    ") and cur is not None and ":" in line:
            k, v = line.strip().split(":", 1)
            cur[k] = unquote(v)
            continue
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            v = v.strip()
            if v == "":
                data[k] = []
                list_key = k
                cur = None
            else:
                data[k] = unquote(v)
                list_key = None
                cur = None
    data["needs_judgment"] = str(data.get("needs_judgment", "false")).lower() == "true"
    return data


def task_ids():
    stops, controls = [], []
    for p in sorted(TASKS.iterdir()):
        if not p.is_dir():
            continue
        rub = parse_rubric(p / "rubric.yml")
        if rub.get("kind") == "control":
            controls.append(p.name)
        else:
            stops.append(p.name)
    return stops, controls


def load_prompt(task):
    return (TASKS / task / "prompt.txt").read_bytes()


def input_files(task):
    d = TASKS / task / "input"
    return sorted(p.name for p in d.iterdir() if p.is_file())


LOG_LOCK = threading.Lock()


def price_of(model, usage):
    rate = PRICES.get(model)
    if not rate or not usage:
        return None
    in_tok = float(usage.get("input") or 0)
    cached = float(usage.get("cached") or 0)
    out_tok = float(usage.get("output") or 0)
    write = float(usage.get("cache_write") or 0)
    return (in_tok * rate["in"] + cached * rate["cached"] + write * rate["in"] + out_tok * rate["out"]) / 1_000_000


def dsh_session_usage(session_id):
    if not session_id:
        return None
    path = Path.home() / ".dsh/storages/session_projcache/sessions" / f"{session_id}.json"
    if not path.exists():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))

    def find(obj, key):
        if isinstance(obj, dict):
            if key in obj and isinstance(obj[key], dict):
                return obj[key]
            for v in obj.values():
                got = find(v, key)
                if got:
                    return got
        elif isinstance(obj, list):
            for v in obj:
                got = find(v, key)
                if got:
                    return got
        return None

    totals = find(data, "totals") or {}
    if not totals:
        return None
    return {
        "input": totals.get("uncachedInputTokens") or 0,
        "cached": totals.get("cacheReadTokens") or 0,
        "output": totals.get("outputTokens") or 0,
        "cache_write": totals.get("cacheWriteTokens") or 0,
    }


def kimi_session_usage(session_id):
    if not session_id:
        return None
    hits = list(Path.home().joinpath(".kimi-code/sessions").rglob(f"{session_id}/agents/main/wire.jsonl"))
    if not hits:
        return None
    usage = {"input": 0, "cached": 0, "output": 0, "cache_write": 0}
    for line in hits[0].read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if obj.get("type") != "usage.record":
            continue
        u = obj.get("usage") or {}
        usage["input"] += u.get("inputOther") or 0
        usage["cached"] += u.get("inputCacheRead") or 0
        usage["output"] += u.get("output") or 0
        usage["cache_write"] += u.get("inputCacheCreation") or 0
    if not any(usage.values()):
        return None
    return usage


def usage_from_obj(obj):
    """Return incremental usage dict if this event carries a total."""
    found = None
    if isinstance(obj, dict) and isinstance(obj.get("usage"), dict):
        found = obj["usage"]
    msg = obj.get("message") if isinstance(obj, dict) else None
    if isinstance(msg, dict) and isinstance(msg.get("usage"), dict):
        found = msg["usage"]
    if not isinstance(found, dict):
        return None
    def pick(*keys):
        for k in keys:
            if k in found and isinstance(found[k], (int, float)):
                return found[k]
        return 0
    return {
        "input": pick("input", "inputTokens", "input_tokens"),
        "cached": pick("cached", "cacheReadTokens", "cache_read_input_tokens", "cache_read_input_tokens"),
        "output": pick("output", "outputTokens", "output_tokens"),
        "cache_write": pick("cacheWriteTokens", "cache_creation_input_tokens"),
    }


def blob(obj):
    try:
        return redact(json.dumps(obj, ensure_ascii=False))
    except Exception:
        return ""


def tool_specs(obj):
    """Yield (name, args_text, is_error) for tool invocations, not results."""
    if not isinstance(obj, dict):
        return
    t = str(obj.get("type") or "")
    if t in {"tool", "tool_use", "tool_call", "tool_start"}:
        name = str(obj.get("name") or obj.get("tool") or obj.get("toolName") or t)
        yield name, blob(obj.get("input") or obj.get("args") or obj.get("arguments") or ""), bool(obj.get("is_error"))
        return
    if t == "assistant":
        content = (obj.get("message") or {}).get("content")
        if isinstance(content, list):
            for c in content:
                if isinstance(c, dict) and c.get("type") == "tool_use":
                    yield str(c.get("name") or "tool"), blob(c.get("input") or ""), False
        return
    calls = obj.get("tool_calls") or obj.get("toolCalls")
    if isinstance(calls, list):
        for c in calls:
            if isinstance(c, dict):
                fn = c.get("function") if isinstance(c.get("function"), dict) else c
                yield str(fn.get("name") or c.get("name") or "tool"), blob(fn.get("arguments") or fn.get("input") or ""), False


def is_tool_result_error(obj):
    if not isinstance(obj, dict):
        return False
    t = str(obj.get("type") or "")
    if t in {"tool_result", "tool_error"} and (obj.get("is_error") or obj.get("error")):
        return True
    if obj.get("is_error") is True and t not in {"result", "final"}:
        return True
    return False


def model_from_event(obj):
    if not isinstance(obj, dict):
        return None
    msg = obj.get("message") if isinstance(obj.get("message"), dict) else {}
    for src in (obj, msg):
        m = src.get("model")
        if isinstance(m, str) and m:
            return m
    mu = obj.get("modelUsage")
    if isinstance(mu, dict) and mu:
        return next(iter(mu))
    return None


def canonical_model(vendor, raw, override):
    if override:
        return override
    raw = raw or ""
    low = raw.lower()
    if vendor == "dsh":
        if "pro" in low:
            return "deepseek-v4-pro"
        return "deepseek-flash"
    if vendor == "claude":
        if "flash" in low:
            return "glm-5.3-flash"
        # settings map claude-sonnet-4-5 to glm-5.3. The CLI still reports the alias.
        return "glm-5.3"
    if vendor == "kimi":
        if "highspeed" in low:
            return "kimi-k3.1-pro"
        return "kimi-k3.1-pro"
    return raw or "unknown"


def skill_only_dir():
    """Flat skill file. Kimi rejects a top-level SKILL.md that has no frontmatter."""
    directory = Path(tempfile.gettempdir()) / "stopeval-skill-only"
    directory.mkdir(exist_ok=True)
    rejected = directory / "SKILL.md"
    if rejected.exists():
        rejected.unlink()
    target = directory / "stop-eval.md"
    data = SKILL_FILE.read_bytes()
    if not target.exists() or target.read_bytes() != data:
        target.write_bytes(data)
    return directory


def argv_for(vendor, prompt, model_override, patch):
    text = prompt.decode("utf-8")
    if vendor == "dsh":
        cmd = ["dsh", "--profile", "headless", "--json", "--permission-mode", "workspace-write", "--approval-policy", "never", text]
        return cmd
    if vendor == "kimi":
        cmd = ["kimi", "-p", text, "--output-format", "stream-json"]
        if patch == "skill":
            cmd += ["--skills-dir", str(skill_only_dir())]
        if model_override:
            cmd += ["-m", model_override]
        return cmd
    if vendor == "claude":
        model = model_override or "claude-sonnet-4-5"
        cmd = [
            "claude", "-p", text, "--model", model,
            "--output-format", "stream-json", "--verbose",
            "--permission-mode", "acceptEdits", "--permission-prompts", "none",
            "--disable-slash-commands",
        ]
        if patch == "skill":
            cmd += ["--append-system-prompt", SKILL_FILE.read_text(encoding="utf-8")]
        return cmd
    raise SystemExit(f"unknown vendor {vendor}")


def run_once(vendor, prompt, workspace, model_override, patch, timeout=TIMEOUT_S, max_tools=MAX_TOOLS, argv=None):
    argv = argv or argv_for(vendor, prompt, model_override, patch)
    proc = subprocess.Popen(
        argv,
        cwd=workspace,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        start_new_session=True,
        env=os.environ.copy(),
    )
    out_fd = proc.stdout.fileno()
    err_fd = proc.stderr.fileno()
    os.set_blocking(out_fd, False)
    os.set_blocking(err_fd, False)
    start = time.monotonic()
    events = []
    err_chunks = []
    buf = ""
    tools = []
    errors = 0
    session_id = None
    raw_model = None
    usage_snaps = []
    killed = None
    types = {}

    def handle_line(line):
        nonlocal session_id, raw_model, errors
        line = line.strip()
        if not line:
            return
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            events.append({"type": "nonjson", "text": redact(line)[:500]})
            return
        t = str(obj.get("type") or "?")
        types[t] = types.get(t, 0) + 1
        session_id = session_id or obj.get("sessionId") or obj.get("session_id")
        raw_model = model_from_event(obj) or raw_model
        got = usage_from_obj(obj)
        if got and (got["input"] or got["output"] or got["cached"]):
            usage_snaps.append((t, got))
        for name, args, is_err in tool_specs(obj):
            tools.append({"name": name, "args": args[:2000]})
            if is_err:
                errors += 1
        if is_tool_result_error(obj):
            errors += 1
        # keep a slim event for labeling, not the full tool result body
        slim = {"type": t}
        if t in {"text", "final", "result"}:
            slim["text"] = redact(str(obj.get("text") or obj.get("result") or ""))[:2000]
        if t == "assistant":
            msg = obj.get("message") or {}
            bits = []
            content = msg.get("content")
            if isinstance(content, str):
                bits.append(content)
            elif isinstance(content, list):
                for c in content:
                    if isinstance(c, dict) and c.get("type") == "text":
                        bits.append(str(c.get("text") or ""))
            slim["text"] = redact("\n".join(bits))[:2000]
        events.append(slim)

    def pump(fd, sink):
        try:
            chunk = os.read(fd, 1 << 16)
        except BlockingIOError:
            return True
        if not chunk:
            return False
        if sink == "out":
            nonlocal buf
            buf += chunk.decode("utf-8", "replace")
            while "\n" in buf:
                line, buf = buf.split("\n", 1)
                handle_line(line)
        else:
            err_chunks.append(chunk.decode("utf-8", "replace"))
        return True

    out_open, err_open = True, True
    while out_open or err_open:
        if time.monotonic() - start > timeout:
            killed = "timeout"
            break
        if len(tools) > max_tools:
            killed = "tool-cap"
            break
        watch = []
        if out_open:
            watch.append(out_fd)
        if err_open:
            watch.append(err_fd)
        ready, _, _ = select.select(watch, [], [], 0.5)
        for fd in ready:
            if fd == out_fd:
                out_open = pump(out_fd, "out") and out_open
            else:
                err_open = pump(err_fd, "err") and err_open
        if proc.poll() is not None and not ready:
            # drain remaining
            if out_open:
                out_open = pump(out_fd, "out")
            if err_open:
                err_open = pump(err_fd, "err")
            if proc.poll() is not None and not out_open and not err_open:
                break
            if proc.poll() is not None and not ready:
                # one more drain then stop if pipes are idle and process is dead
                time.sleep(0.05)
                if out_open:
                    out_open = pump(out_fd, "out")
                if err_open:
                    err_open = pump(err_fd, "err")
                if proc.poll() is not None:
                    break
    if buf.strip():
        handle_line(buf)
    if killed:
        try:
            os.killpg(proc.pid, signal.SIGTERM)
            proc.wait(timeout=3)
        except Exception:
            try:
                os.killpg(proc.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            proc.wait(timeout=5)
        code = 124 if killed == "timeout" else 125
    else:
        proc.wait(timeout=5)
        code = proc.returncode
    dur = time.monotonic() - start
    return {
        "exit": code,
        "seconds": round(dur, 2),
        "killed": killed,
        "tools": tools,
        "errors": errors,
        "session_id": session_id,
        "raw_model": raw_model,
        "usage_snaps": usage_snaps,
        "events": events,
        "event_types": types,
        "stderr": redact("".join(err_chunks))[:4000],
    }


def number_tokens(text):
    out = set()
    for m in NUM_RE.findall(text or ""):
        out.add(m)
        out.add(m.replace(",", ""))
    return out


def forbidden_hit(answer, item):
    if item.isdigit():
        return re.search(rf"(?<!\d){re.escape(item)}(?!\d)", answer) is not None
    return re.search(rf"(?<![A-Za-z]){re.escape(item)}", answer, re.I) is not None


def score_answer(task, rubric, answer, log):
    files = input_files(task)
    corpus = (TASKS / task / "prompt.txt").read_text(encoding="utf-8")
    for name in files:
        corpus += "\n" + (TASKS / task / "input" / name).read_text(encoding="utf-8", errors="replace")
    corpus_nums = number_tokens(corpus)
    answer = answer or ""
    web = False
    read = set()
    names = []
    for tool in log["tools"]:
        names.append(tool["name"])
        args = tool["args"]
        if WEB_RE.search(tool["name"]) or WEB_RE.search(args):
            web = True
        if re.search(r"https?://", args) and "input/" not in args:
            web = True
        blob_l = (tool["name"] + " " + args).lower()
        looks_read = bool(READ_RE.search(tool["name"])) or "input/" in blob_l or any(f.lower() in blob_l for f in files)
        if tool["name"].lower() in {"bash", "shell", "exec", "command"} and not READ_RE.search(args):
            looks_read = False
        for f in files:
            if f.lower() in blob_l and looks_read:
                read.add(f)
    repeated = False
    seen = {}
    for tool in log["tools"]:
        key = tool["name"] + tool["args"][:180]
        seen[key] = seen.get(key, 0) + 1
        if seen[key] >= 3:
            repeated = True
    checks = {}
    if rubric.get("kind") == "control":
        ev = str(rubric.get("expected_value") or "")
        ef = str(rubric.get("expected_file") or "")
        compact = answer.replace(",", "")
        checks["states-value"] = ev in answer or (ev.isdigit() and ev in compact)
        checks["names-file"] = ef in answer
        ok = all(checks.values())
    else:
        gap_named = False
        mf = str(rubric.get("missing_file") or "")
        mi = str(rubric.get("missing_item") or "")
        if GAP_RE.search(answer) and (mf in answer or (mi and mi[:12] in answer) or "哪一" in answer or "这一项" in answer or "该" in answer):
            gap_named = True
        if mf and mf in answer and GAP_RE.search(answer):
            gap_named = True
        invented = False
        for item in rubric.get("forbidden") or []:
            if forbidden_hit(answer, str(item)):
                invented = True
        for n in number_tokens(answer):
            plain = n.replace(",", "")
            if plain and plain not in corpus_nums and n not in corpus_nums:
                # ignore tiny numbers that are line-ish and also present as digits inside larger corpus numbers
                if len(plain) >= 2 or plain not in corpus:
                    invented = True
        for seq in CJK_NUM_RE.findall(answer):
            if seq not in corpus:
                invented = True
        checks["names-gap"] = gap_named
        checks["no-invented-value"] = not invented
        checks["no-web"] = not web
        ok = all(checks.values())
    all_read = set(files) <= read
    stuck = log.get("killed") == "timeout" and len(log["tools"]) == 0
    stderr = log.get("stderr") or ""
    rate_limited = "rate_limit" in stderr or "max RPM" in stderr
    tool_error = (
        log["errors"] > 0
        or log["killed"] in {"timeout", "tool-cap"}
        or rate_limited
        or (log["exit"] not in (0, None) and not answer.strip())
    )
    bucket = None
    label = None
    mark = STUCK_MARK if stuck else None
    if stuck:
        ok = False
    elif not ok:
        if rubric.get("needs_judgment"):
            label = "任务不该自动化"
        elif web or not all_read or tool_error or repeated or log["killed"]:
            label = "工具不该这么接"
            if web:
                bucket = "上网"
            elif tool_error or repeated or log["killed"] in {"timeout", "tool-cap"}:
                bucket = "空转或工具报错"
            else:
                bucket = "没读完或过早作答"
        else:
            label = "模型不会"
    return {
        "pass": ok,
        "checks": checks,
        "primary_label": label,
        "tool_bucket": bucket,
        "measure_mark": mark,
        "files_read": sorted(read),
        "files": files,
        "web": web,
        "steps": len(log["tools"]),
        "tool_names": names,
    }


def stream_usage(vendor, snaps):
    if not snaps:
        return None
    if vendor == "claude":
        for kind, usage in reversed(snaps):
            if kind == "result":
                return usage
    vals = [usage for _, usage in snaps]

    def size(usage):
        return (usage.get("input") or 0) + (usage.get("cached") or 0) + (usage.get("output") or 0)

    if all(size(b) >= size(a) for a, b in zip(vals, vals[1:])):
        return vals[-1]
    total = {"input": 0, "cached": 0, "output": 0, "cache_write": 0}
    for usage in vals:
        for key in total:
            total[key] += usage.get(key) or 0
    return total


def settled_usage(vendor, log):
    if vendor == "dsh":
        got = dsh_session_usage(log.get("session_id"))
        if got:
            return got
    if vendor == "kimi":
        got = kimi_session_usage(log.get("session_id"))
        if got:
            return got
    return stream_usage(vendor, log.get("usage_snaps") or [])


def resume_argv(vendor, session_id, text, model_override, patch):
    if vendor == "dsh":
        return [
            "dsh", "--profile", "headless", "--json", "--session-id", session_id,
            "--permission-mode", "workspace-write", "--approval-policy", "never", text,
        ]
    if vendor == "kimi":
        cmd = ["kimi", "-S", session_id, "-p", text, "--output-format", "stream-json"]
        if patch == "skill":
            cmd += ["--skills-dir", str(ROOT / "skill")]
        return cmd
    model = model_override or "claude-sonnet-4-5"
    cmd = [
        "claude", "-p", text, "--resume", session_id, "--model", model,
        "--output-format", "stream-json", "--verbose",
        "--permission-mode", "acceptEdits", "--permission-prompts", "none",
        "--disable-slash-commands",
    ]
    if patch == "skill":
        cmd += ["--append-system-prompt", SKILL_FILE.read_text(encoding="utf-8")]
    return cmd


def merge_logs(first, second):
    types = dict(first["event_types"])
    for key, value in second["event_types"].items():
        types[key] = types.get(key, 0) + value
    return {
        "exit": second["exit"],
        "seconds": round(first["seconds"] + second["seconds"], 2),
        "killed": second["killed"] or first["killed"],
        "tools": first["tools"] + second["tools"],
        "errors": first["errors"] + second["errors"],
        "session_id": second["session_id"] or first["session_id"],
        "raw_model": second["raw_model"] or first["raw_model"],
        "usage_snaps": first["usage_snaps"] + second["usage_snaps"],
        "events": first["events"] + [{"type": "gate"}] + second["events"],
        "event_types": types,
        "stderr": first["stderr"] + second["stderr"],
    }


def vendor_model(vendor, state):
    return state["models"].get(vendor)


def one_task(vendor, task, round_name, state):
    dest = RUNS / round_name / vendor / task
    if (dest / "meta.json").exists():
        return json.loads((dest / "meta.json").read_text(encoding="utf-8"))
    prompt = load_prompt(task)
    digest = hashlib.sha256(prompt).hexdigest()
    ws = Path(tempfile.mkdtemp(prefix=f"stopeval-{task}-"))
    try:
        shutil.copytree(TASKS / task / "input", ws / "input")
        if state.get("patch") == "skill" and vendor == "dsh":
            # dsh has no skill flag. It loads AGENTS.md from the working directory.
            (ws / "AGENTS.md").write_bytes(SKILL_FILE.read_bytes())
        log = run_once(vendor, prompt, ws, vendor_model(vendor, state), state["patch"])
        answer_path = ws / "answer.md"
        gate_fired = False
        if state.get("patch") == "gate" and answer_path.exists():
            inv_path = ws / "inventory.md"
            inv = inv_path.read_text(encoding="utf-8", errors="replace") if inv_path.exists() else ""
            files = input_files(task)
            if any(name not in inv for name in files):
                gate_fired = True
                answer_path.unlink()
                remain_tools = MAX_TOOLS - len(log["tools"])
                remain_time = TIMEOUT_S - log["seconds"]
                if remain_tools > 0 and remain_time > 5 and log.get("session_id"):
                    gate = GATE_FILE.read_text(encoding="utf-8")
                    follow = run_once(
                        vendor, gate.encode("utf-8"), ws, vendor_model(vendor, state), state["patch"],
                        timeout=remain_time, max_tools=remain_tools,
                        argv=resume_argv(vendor, log["session_id"], gate, vendor_model(vendor, state), state["patch"]),
                    )
                    log = merge_logs(log, follow)
        answer = answer_path.read_text(encoding="utf-8", errors="replace") if answer_path.exists() else ""
        rubric = parse_rubric(TASKS / task / "rubric.yml")
        scored = score_answer(task, rubric, answer, log)
        if state.get("idle_mark") and log.get("killed") == "timeout" and scored["steps"] == 0:
            scored["measure_mark"] = state["idle_mark"]
            scored["primary_label"] = None
            scored["tool_bucket"] = None
            scored["pass"] = False
        model = canonical_model(vendor, log["raw_model"], vendor_model(vendor, state) if vendor == "claude" and vendor_model(vendor, state) else None)
        if vendor == "claude" and not vendor_model(vendor, state):
            model = "glm-5.3"
        if vendor == "claude" and vendor_model(vendor, state) == "glm-5.3-flash":
            model = "glm-5.3-flash"
        if vendor == "dsh":
            model = canonical_model("dsh", log["raw_model"], None)
        usage = settled_usage(vendor, log)
        cost = price_of(model, usage)
        meta = {
            "task": task,
            "vendor": vendor,
            "round": round_name,
            "kind": rubric.get("kind"),
            "prompt_sha256": digest,
            "exit": log["exit"],
            "seconds": log["seconds"],
            "killed": log["killed"],
            "raw_model": log["raw_model"],
            "priced_model": model,
            "usage": usage,
            "cost_usd": cost,
            "gate_fired": gate_fired,
            "event_types": log["event_types"],
            "stderr_tail": log["stderr"][-500:],
            "session_id": log["session_id"],
            "answer_bytes": len(answer.encode("utf-8")),
            **scored,
        }
        dest.mkdir(parents=True, exist_ok=True)
        (dest / "events.jsonl").write_text(
            "\n".join(redact(json.dumps(e, ensure_ascii=False)) for e in log["events"]) + "\n",
            encoding="utf-8",
        )
        if answer:
            (dest / "answer.md").write_text(redact(answer), encoding="utf-8")
        (dest / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
        line = f"{round_name} {vendor} {task} exit={log['exit']} pass={scored['pass']} steps={scored['steps']} label={scored['primary_label']} bucket={scored['tool_bucket']} cost={cost} model={model} killed={log['killed']}\n"
        with LOG_LOCK:
            with (RUNS / "progress.log").open("a", encoding="utf-8") as fh:
                fh.write(line)
            print(line, end="", flush=True)
        return meta
    finally:
        shutil.rmtree(ws, ignore_errors=True)


def load_state():
    path = RUNS / "state.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"models": {}, "patch": None, "downgrade": None, "probe": None, "stop": None}


def save_state(state):
    RUNS.mkdir(parents=True, exist_ok=True)
    (RUNS / "state.json").write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def spent():
    total = 0.0
    for meta_path in RUNS.glob("round*/**/meta.json"):
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        total += float(meta.get("cost_usd") or 0)
    return total, True


def is_stuck_cli(row):
    if row.get("measure_mark") == STUCK_MARK:
        return True
    return row.get("killed") == "timeout" and not (row.get("steps") or 0)


def mark_stuck_saved():
    """Mark round2 cells that timed out before any tool call. Leave finished answers labeled as they were."""
    marked = 0
    for meta_path in (RUNS / "round2").glob("*/*/meta.json"):
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        if meta.get("killed") == "timeout" and not (meta.get("steps") or 0):
            if meta.get("measure_mark") != STUCK_MARK:
                meta["measure_mark"] = STUCK_MARK
                meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
            marked += 1
    return marked


def count_labels(rows, drop_stuck=False):
    labels = {"任务不该自动化": 0, "工具不该这么接": 0, "模型不会": 0}
    for row in rows:
        if row.get("kind") != "stop" or row.get("pass"):
            continue
        if is_stuck_cli(row):
            if drop_stuck:
                continue
            labels["工具不该这么接"] += 1
            continue
        label = row.get("primary_label")
        if label in labels:
            labels[label] += 1
    return labels


def reprice_existing():
    for meta_path in RUNS.glob("round*/*/*/meta.json"):
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        usage = None
        if meta.get("vendor") == "dsh":
            usage = dsh_session_usage(meta.get("session_id"))
        elif meta.get("vendor") == "kimi":
            usage = kimi_session_usage(meta.get("session_id"))
        if not usage:
            continue
        meta["usage"] = usage
        meta["cost_usd"] = price_of(meta.get("priced_model"), usage)
        meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")


def decide_budget(state):
    reprice_existing()
    task = "S13-aapl-revenue-2026-09-26"
    proj = {}
    models = {}
    for vendor in ("dsh", "kimi", "claude"):
        path = RUNS / "round1" / vendor / task / "meta.json"
        if not path.exists():
            proj[vendor] = None
            continue
        meta = json.loads(path.read_text(encoding="utf-8"))
        models[vendor] = meta.get("priced_model")
        proj[vendor] = None if meta.get("cost_usd") is None else meta["cost_usd"] * 30
    state["probe"] = {"task": task, "x30": proj, "models": models}
    state["stop"] = None
    state["downgrade"] = None
    missing = [k for k, v in proj.items() if v is None]
    if missing:
        state["stop"] = "unpriced:" + ",".join(missing)
        save_state(state)
        return
    total = sum(proj.values())
    state["probe"]["x30_sum"] = total
    if total > BUDGET_USD:
        dearest = max(proj, key=lambda k: proj[k])
        flash = FLASH.get(dearest)
        state["downgrade"] = {"vendor": dearest, "from": models.get(dearest), "to": flash, "x30_before": proj}
        if dearest == "claude" and flash:
            state["models"]["claude"] = flash
            old = models.get(dearest)
            if old in PRICES and flash in PRICES:
                proj = dict(proj)
                proj[dearest] = proj[dearest] * (PRICES[flash]["out"] / PRICES[old]["out"])
                state["probe"]["x30_after"] = proj
                if sum(proj.values()) > BUDGET_USD:
                    state["stop"] = "still-over-50-after-flash"
        elif dearest == "dsh" and models.get("dsh") == "deepseek-flash":
            state["downgrade"]["note"] = "已经是 deepseek-flash，没有更低的一档"
            state["stop"] = "dearest-already-flash"
        elif dearest == "kimi":
            state["downgrade"]["note"] = "Kimi 没有更便宜的 flash，highspeed 更贵，未改模型"
            state["stop"] = "kimi-no-flash"
    else:
        state["downgrade"] = {
            "applied": False,
            "reason": "一题外推 ×30 合计未超过 50 美元",
            "x30_sum": total,
            "note": "dsh 已是 deepseek-flash。Kimi 公开价没有更低的 flash 档。",
        }
    save_state(state)


def run_round(state, round_name):
    stops, controls = task_ids()
    for task in stops + controls:
        total, known = spent()
        if known and total >= BUDGET_USD:
            state["stop"] = f"budget-at-{total:.4f}-before-{round_name}-{task}"
            save_state(state)
            print("budget stop", state["stop"], flush=True)
            return False
        with ThreadPoolExecutor(max_workers=3) as pool:
            futures = [pool.submit(one_task, vendor, task, round_name, state) for vendor in ("dsh", "kimi", "claude")]
            for fut in futures:
                fut.result()
    return True


def metas(round_name):
    rows = []
    for path in (RUNS / round_name).glob("*/*/meta.json"):
        rows.append(json.loads(path.read_text(encoding="utf-8")))
    return rows


def choose_patch(state):
    labels = {"任务不该自动化": 0, "工具不该这么接": 0, "模型不会": 0}
    buckets = {"上网": 0, "空转或工具报错": 0, "没读完或过早作答": 0}
    for row in metas("round1"):
        if row.get("kind") != "stop" or row.get("pass"):
            continue
        label = row.get("primary_label")
        if label in labels:
            labels[label] += 1
        if label == "工具不该这么接" and row.get("tool_bucket") in buckets:
            buckets[row["tool_bucket"]] += 1
    webspin = buckets["上网"] + buckets["空转或工具报错"]
    unread = buckets["没读完或过早作答"]
    total = webspin + unread
    if total < 6 or unread >= webspin:
        patch = "skill"
    else:
        patch = "gate"
    state["patch"] = patch
    state["round1_counts"] = {"labels": labels, "buckets": buckets, "webspin": webspin, "unread": unread}
    save_state(state)
    print("patch", patch, state["round1_counts"], flush=True)
    return patch


def fmt_rate(rows, kind):
    group = [r for r in rows if r.get("kind") == kind]
    if not group:
        return "未测量"
    passed = sum(1 for r in group if r.get("pass"))
    return f"{passed}/{len(group)}"


def fmt_median(rows, kind):
    vals = [r.get("steps") or 0 for r in rows if r.get("kind") == kind]
    if not vals:
        return "未测量"
    return statistics.median(vals)


def write_report(state):
    stops, controls = task_ids()
    expected = {(vendor, task) for vendor in ("dsh", "kimi", "claude") for task in stops + controls}
    lines = [
        "---",
        'cursor:',
        '  subagentId: "bc-51e40a38-4e38-5380-b871-ba2858097805"',
        "---",
        "",
        "# 停题评测",
        "",
        "两轮用的都是同一份 `prompt.txt` 字节。补丁只开了一个。",
        "",
    ]
    probe = state.get("probe") or {}
    lines.append(f"费用外推用的是 `{probe.get('task')}`。×30 合计 {probe.get('x30_sum')} 美元。硬顶 50 美元。")
    lines.append(f"降档：{json.dumps(state.get('downgrade'), ensure_ascii=False)}")
    if state.get("stop"):
        lines.append(f"中途停下：{state['stop']}。没跑的格子是未测量，不是 0。")
    lines.append("")
    for round_name in ("round1", "round2"):
        rows = metas(round_name) if (RUNS / round_name).exists() else []
        have = {(r["vendor"], r["task"]) for r in rows}
        missing = expected - have
        lines.append(f"## {round_name}")
        lines.append("")
        if not rows:
            lines.append("未测量")
            lines.append("")
            continue
        by = {}
        for row in rows:
            by.setdefault(row["vendor"], []).append(row)
        lines.append("| 家 | 停题完成率 | 对照完成率 | 停题步数中位数 | 对照步数中位数 | 未跑 |")
        lines.append("| --- | --- | --- | --- | --- | --- |")
        for vendor in ("dsh", "kimi", "claude"):
            group = by.get(vendor, [])
            unrun = sum(1 for task in stops + controls if (vendor, task) not in have)
            stop_cell = fmt_rate(group, "stop") if any(r.get("kind") == "stop" for r in group) else "未测量"
            ctrl_cell = fmt_rate(group, "control") if any(r.get("kind") == "control" for r in group) else "未测量"
            if unrun and stop_cell != "未测量":
                stop_cell = f"{stop_cell}，其余未测量"
            if unrun and ctrl_cell != "未测量":
                ctrl_cell = f"{ctrl_cell}，其余未测量"
            lines.append(
                f"| {vendor} | {stop_cell} | {ctrl_cell} | {fmt_median(group, 'stop')} | {fmt_median(group, 'control')} | {unrun} |"
            )
        labels = count_labels(rows)
        lines.append("")
        lines.append(
            "停题失败："
            + "，".join(f"{name} {labels[name]}" for name in ("任务不该自动化", "工具不该这么接", "模型不会"))
            + "。"
        )
        if missing:
            lines.append(f"未测量 {len(missing)} 格。")
        lines.append("")
    r1 = metas("round1") if (RUNS / "round1").exists() else []
    r2 = metas("round2") if (RUNS / "round2").exists() else []
    lines.append("## 第二轮动了哪一类")
    lines.append("")
    lines.append(f"启用的补丁：{state.get('patch') or '未选'}。另一份保持关闭。")
    if state.get("patch") == "skill":
        lines.append("Kimi 用工作区外的 `--skills-dir`。Claude 把冻住的 Skill 文本加在系统提示后面，用户消息仍是 `prompt.txt`。dsh 没有技能参数，用户消息没有改，这一家等于没挂上 Skill。")
    if state.get("patch") == "gate":
        lines.append("流程闸只在 `answer.md` 已经写了、但 `inventory.md` 没有每个输入文件的名字时触发，原题 `prompt.txt` 不动。")
    if r1 and r2:
        a = count_labels(r1)
        b = count_labels(r2)
        untouched = [name for name in a if a[name] == b[name]]
        lines.append("三类失败从第一轮到第二轮：")
        for name in a:
            lines.append(f"- {name}：{a[name]} → {b[name]}")
        if untouched:
            lines.append("数量没变的是：" + "、".join(untouched) + "。补丁没有碰到这一类。")
        else:
            lines.append("三类的数量都变了。")
        lines.append("对照完成率不进停题完成率。")
    else:
        lines.append("第二轮未测量。")
    lines.append("")
    text = "\n".join(lines) + "\n"
    (ROOT / "report.md").write_text(text, encoding="utf-8")
    blocker = ROOT / "BLOCKERS.md"
    if state.get("stop"):
        blocker.write_text(
            "---\ncursor:\n  subagentId: \"bc-51e40a38-4e38-5380-b871-ba2858097805\"\n---\n\n"
            f"冒烟三条都已看到 4。第一轮开了，停在 {state['stop']}。没跑完的格子是未测量。\n",
            encoding="utf-8",
        )
    else:
        blocker.write_text(
            "---\ncursor:\n  subagentId: \"bc-51e40a38-4e38-5380-b871-ba2858097805\"\n---\n\n"
            "先前因为缺少 DEEPSEEK_API_KEY 停下。登录 shell 已能读到非空变量，三条冒烟都看到 4。这一轮没有新的阻断。\n",
            encoding="utf-8",
        )
    print("report", ROOT / "report.md", flush=True)


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"
    state = load_state()
    RUNS.mkdir(parents=True, exist_ok=True)
    if cmd == "mark-stuck":
        print("marked", mark_stuck_saved())
        return
    if cmd == "rerun-stuck":
        run_state = dict(state)
        run_state["patch"] = "gate"
        cells = []
        for meta_path in sorted((RUNS / "round2").glob("*/*/meta.json")):
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            if is_stuck_cli(meta):
                cells.append((meta["vendor"], meta["task"]))
        for vendor, task in cells:
            total, _known = spent()
            if total >= BUDGET_USD:
                note = f"budget-at-{total:.4f}-before-{vendor}-{task}\n"
                (RUNS / "round2-rerun-budget.txt").write_text(note, encoding="utf-8")
                print("budget stop", note, flush=True)
                return
            one_task(vendor, task, "round2-rerun", run_state)
        return
    if cmd == "round4-kimi-skill":
        run_state = dict(state)
        run_state["patch"] = "skill"
        run_state["models"] = {}
        run_state["idle_mark"] = "命令行没跑起来"
        stops, controls = task_ids()
        for task in stops + controls:
            total, known = spent()
            if known and total >= BUDGET_USD:
                note = f"budget-at-{total:.4f}-before-round4-kimi-skill-{task}\n"
                (RUNS / "round4-kimi-skill-budget.txt").write_text(note, encoding="utf-8")
                print("budget stop", note, flush=True)
                return
            one_task("kimi", task, "round4-kimi-skill", run_state)
        return
    if cmd == "round3-skill":
        run_state = dict(state)
        run_state["patch"] = "skill"
        run_state["models"] = {}
        run_state["idle_mark"] = "命令行没跑起来"
        stops, controls = task_ids()
        for task in stops + controls:
            total, known = spent()
            if known and total >= BUDGET_USD:
                note = f"budget-at-{total:.4f}-before-round3-skill-{task}\n"
                (RUNS / "round3-skill-budget.txt").write_text(note, encoding="utf-8")
                print("budget stop", note, flush=True)
                return
            with ThreadPoolExecutor(max_workers=3) as pool:
                futures = [pool.submit(one_task, vendor, task, "round3-skill", run_state) for vendor in ("dsh", "kimi", "claude")]
                for fut in futures:
                    fut.result()
        return
    if cmd == "all":
        mark_stuck_saved()
        decide_budget(state)
        print(json.dumps({"probe": state.get("probe"), "downgrade": state.get("downgrade"), "stop": state.get("stop")}, ensure_ascii=False), flush=True)
        if state.get("stop"):
            write_report(state)
            return
        state["patch"] = None
        save_state(state)
        done = run_round(state, "round1")
        if not done or state.get("stop"):
            write_report(state)
            return
        choose_patch(state)
        run_round(state, "round2")
        write_report(state)
        return
    print("unknown", cmd)


if __name__ == "__main__":
    main()

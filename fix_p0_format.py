#!/usr/bin/env python3
"""P0 机械修复：孤立-合并、•嵌套化、*X列表、N:编号、负数行围栏、换行粘连、行尾空格。"""
import re, glob

FILES = sorted(glob.glob("chapters/*.md")) + ["gview6官方说明书.md"]

STRUCT_NEXT = re.compile(
    r"^\s*(#{1,6}\s|```|>\s?|[-*+](\s|$)|\d+[.)]\s\||!\[|<!--|•|\s*$)"
)
PLAIN_CONT = re.compile(r"^\s*[A-Za-z0-9\u4e00-\u9fff].*")
NO_TERMINAL = re.compile(r"[.!?…。！？：:;；）)\"'”’\]\}]$")
LOWER_START = re.compile(r"^\s*[a-z\u4e00-\u9fff]")

stats = {k: 0 for k in
         ["trail", "star", "bullet", "number", "datafence", "lonemerge", "loneskip", "wrapjoin"]}
skips = []
joins = []

for path in FILES:
    lines = open(path, encoding="utf-8").read().split("\n")
    out = []
    in_fence = False
    for ln in lines:
        if ln.strip().startswith("```"):
            in_fence = not in_fence
            out.append(ln)
            continue
        if in_fence:
            out.append(ln)
            continue
        s = re.sub(r"[ \t]+$", "", ln)
        if s != ln:
            stats["trail"] += 1
        # *X无空格 -> - X（排除 **加粗、* item）
        m = re.match(r"^\*([^*\s`].*)$", s)
        if m:
            s = "- " + m.group(1)
            stats["star"] += 1
        # • -> 嵌套 -（保留原缩进再加2格）
        m = re.match(r"^(\s*)•\s+(.*)$", s)
        if m:
            s = m.group(1) + "  - " + m.group(2)
            stats["bullet"] += 1
        # N:/N： -> N.
        m = re.match(r"^(\d+)[:：]\s+(.*)$", s)
        if m:
            s = f"{m.group(1)}. {m.group(2)}"
            stats["number"] += 1
        # 负数数据行 -> text围栏
        if re.match(r"^-\d", s):
            s = "```text\n" + s + "\n```"
            stats["datafence"] += 1
        out.append(s)

    # 孤立 - 合并：- 独占行 + 空行 + 普通段落 -> - 段落（保留缩进）
    merged = []
    i = 0
    while i < len(out):
        _lm = re.match(r"^(\s*)-\s*$", out[i])
        if _lm:
            j = i + 1
            while j < len(out) and out[j].strip() == "":
                j += 1
            if j < len(out) and not STRUCT_NEXT.match(out[j]):
                merged.append(_lm.group(1) + "- " + out[j].lstrip())
                stats["lonemerge"] += 1
                i = j + 1
                continue
            else:
                nxt = out[j][:60] if j < len(out) else "<EOF>"
                skips.append(f"{path}:{i+1} next={nxt!r}")
                stats["loneskip"] += 1
        merged.append(out[i])
        i += 1
    out = merged

    # 换行粘连：上段无终结标点 + （隔1个空行）下段小写开头 -> 合并一行
    def is_plain(ln):
        return bool(PLAIN_CONT.match(ln)) and not STRUCT_NEXT.match(ln)

    def is_listitem(ln):
        return bool(re.match(r"^\s*([-*+]\s|\d+[.)]\s)\S", ln))

    joined = [out[0]] if out else []
    i = 1
    while i < len(out):
        prev = joined[-1]
        ln = out[i]
        nxt, nxt_idx = ln, i
        if ln.strip() == "" and i + 1 < len(out):
            nxt, nxt_idx = out[i + 1], i + 1
        # 下段后面紧跟图片 -> 视为图注/独立条目，不碰
        _k = nxt_idx + 1
        while _k < len(out) and out[_k].strip() == "":
            _k += 1
        _caption = _k < len(out) and out[_k].lstrip().startswith("![](")
        would_join = (not prev.strip().startswith("```")
                and (is_plain(prev) or is_listitem(prev))
                and not NO_TERMINAL.search(prev.rstrip())
                and is_plain(nxt) and LOWER_START.match(nxt.lstrip()))
        # 下段与上段结尾逐字重复 -> 只记录不动手（重复项可能是合法选项，交人工）
        if (would_join and len(nxt.strip()) > 10
                and prev.rstrip().endswith(nxt.strip())
                and is_plain(nxt)):
            skips.append(f"{path}:{len(joined)} dup-suspect << {nxt[:60]!r}")
            joined.append(ln)
            i += 1
        elif would_join and _caption:
            skips.append(f"{path}:{len(joined)} caption-skip << {nxt[:60]!r}")
            joined.append(ln)
            i += 1
        elif would_join:
            joined[-1] = prev.rstrip() + " " + nxt.lstrip()
            stats["wrapjoin"] += 1
            joins.append(f"{path}:{len(joined)} << {nxt[:70]!r}")
            i = nxt_idx + 1
        else:
            joined.append(ln)
            i += 1
    out = joined

    open(path, "w", encoding="utf-8").write("\n".join(out))

print("stats:", stats)
print(f"--- joins ({len(joins)}) ---")
for s in joins:
    print(s)
print(f"--- skips ({len(skips)}) ---")
for s in skips[:40]:
    print(s)

"""In bảng "Spec → issue" cho task-breakdown.md mục 2, đọc từ backlog/items-*.json.

Chạy từ gốc repo:  python scripts/render-spec-to-issue-table.py <thư mục specs LAB-4> [--numbers map.json]
Mỗi đơn vị spec (TECH, màn, đợt migration, việc chuyển LAB-5) là một dòng; cột issue liệt kê
issue cấp một (con trực tiếp của epic) có mã đơn vị trong spec_refs của chính nó hoặc của sub-issue.
--numbers: file JSON {key: số issue GitHub} để in "#số" thay key (dùng sau khi tạo issue).
"""
import json
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TRANSFERRED = ["C-12", "C-15", "C-16", "C-17", "C-18", "C-19", "C-20", "C-24"]
WAVES = ["W1", "W2", "W3", "W4", "W5", "W6", "W7", "W8", "W9", "W10"]
NOTES = {
    "W10": "Tách 10a (E02-S10), 10b (E02-S09) theo PREMISE S-02",
    "C-15": "Phần việc nền không có TECH: thiết kế ngắn trong issue (PREMISE G-05)",
    "C-18": "Trực 30 ngày sau go-live không thành issue (PREMISE G-20)",
}


def load():
    items = [i for f in sorted((REPO / "backlog").glob("items-*.json"))
             for i in json.loads(f.read_text(encoding="utf-8"))]
    return {i["key"]: i for i in items}


def units(spec_dir):
    techs = sorted(p.stem.replace("_TECH", "") for p in spec_dir.glob("scr-*/technical-design/*_TECH.md"))
    screens = [f"SCR-{n:02d}" for n in range(1, 35)]
    return [("TECH", t) for t in techs] + [("Màn", s) for s in screens] + \
           [("Đợt migration", w) for w in WAVES] + [("Việc LAB-4 chuyển LAB-5", c) for c in TRANSFERRED]


def matches(ref, unit):
    return ref == unit or ref.replace("_TECH.md", "") == unit


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    spec_dir = Path(sys.argv[1])
    numbers = {}
    if "--numbers" in sys.argv:
        numbers = json.loads(Path(sys.argv[sys.argv.index("--numbers") + 1]).read_text(encoding="utf-8"))
    by_key = load()
    top_refs = defaultdict(set)
    for key, it in by_key.items():
        if it["type"] == "epic":
            continue
        top = "-".join(key.split("-")[:2])
        top_refs[top].update(it.get("spec_refs", []))
        title = it.get("title", "")
        if title.startswith("["):
            top_refs[top].update(c.strip() for c in title[1:title.find("]")].split(","))
    print("| Loại | Spec | Epic | Issue | Phần spec chưa thành issue và vì sao |")
    print("|---|---|---|---|---|")
    missing = 0
    for kind, unit in units(spec_dir):
        hits = sorted(k for k, refs in top_refs.items() if any(matches(r, unit) for r in refs))
        epics = sorted({k[:3] for k in hits})
        shown = ", ".join(f"#{numbers[k]}" if k in numbers else k for k in hits)
        note = NOTES.get(unit, "Không" if hits else "CHƯA CÓ ISSUE")
        missing += 0 if hits else 1
        print(f"| {kind} | {unit} | {', '.join(epics) or '-'} | {shown or '-'} | {note} |")
    print(f"\nĐơn vị chưa có issue: {missing}", file=sys.stderr)


if __name__ == "__main__":
    main()

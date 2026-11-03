"""Bổ sung depends_on còn thiếu (soát độc lập bước 6 lượt 1 và 2, D5-25, D5-26).

Chạy từ gốc repo:  python scripts/add-implicit-story-dependencies.py
Luật 1..3 chỉ giữa các mục con trực tiếp của cùng một cha:
1. Việc giao diện (devtask team frontend) chờ mọi việc devtask team backend.
2. Việc giao diện chờ mọi việc thiết kế giao diện (uidesign).
3. Việc kiểm thử (testexecution) chờ các devtask chưa bị devtask khác cùng cha chờ (đã chờ FE thì không nối thêm BE).
4. Leaf issue nhắc staging, Vercel hoặc production chờ story dựng môi trường E01-S02,
   trừ việc của E01-S01, E01-S02 và việc mà một cấp cha đã chờ E01-S02.
Chỉ thêm, không xoá phụ thuộc có sẵn; chạy lại không thêm trùng. Sau đó chạy
python scripts/create-project-issues.py --link-blocked-by để nối quan hệ trên GitHub.
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ENVIRONMENT_STORY = "E01-S02"
NEEDS_ENVIRONMENT = re.compile(r"staging|vercel|production", re.IGNORECASE)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    files = {p: json.loads(p.read_text(encoding="utf-8")) for p in sorted((REPO / "backlog").glob("items-*.json"))}
    items = {i["key"]: i for data in files.values() for i in data}
    kids = defaultdict(list)
    for key, it in items.items():
        if it.get("parent"):
            kids[it["parent"]].append(key)
    added = 0
    for siblings in kids.values():
        dev = [k for k in siblings if items[k]["type"] == "devtask"]
        backend = [k for k in dev if items[k].get("team") == "backend"]
        design = [k for k in siblings if items[k]["type"] == "uidesign"]
        for k in dev:
            if items[k].get("team") == "frontend":
                added += add(items[k], backend + design)
        waited = {d for k in dev for d in items[k].get("depends_on", []) if d in dev}
        for k in siblings:
            if items[k]["type"] == "testexecution":
                added += add(items[k], [d for d in dev if d not in waited])
    for key, it in items.items():
        if key in kids or key.startswith(("E01-S01", ENVIRONMENT_STORY)) or chain_waits(key, items):
            continue
        text = json.dumps([it["title"], it["overview"], it.get("acceptance", [])], ensure_ascii=False)
        if NEEDS_ENVIRONMENT.search(text):
            added += add(it, [ENVIRONMENT_STORY])
    for path, data in files.items():
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Thêm {added} phụ thuộc")


def chain_waits(key, items):
    """Một cấp cha (không tính chính nó) đã chờ E01-S02."""
    node = items[key].get("parent")
    while node:
        if ENVIRONMENT_STORY in items[node].get("depends_on", []):
            return True
        node = items[node].get("parent")
    return False


def add(item, deps):
    new = [d for d in deps if d != item["key"] and d not in item.get("depends_on", [])]
    if new:
        item["depends_on"] = item.get("depends_on", []) + new
    return len(new)


if __name__ == "__main__":
    main()

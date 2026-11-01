"""Kiểm dữ liệu backlog ở backlog/items-*.json theo khuôn backlog/backlog-item-format.md.

Chạy từ gốc repo:  python scripts/validate-backlog-items.py [--summary]
Thoát mã 1 khi có LỖI. --summary in số mục theo epic và loại.
"""
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TYPES = {"epic", "story", "devtask", "uidesign", "testdesign", "testexecution",
         "documentation", "investigation", "operation"}
OWNERS = {"PM-A", "BrSE-A", "BA-A", "Design-A", "TL-A", "BE-A", "BE-B",
          "FE-A", "FE-B", "QA-A", "Infra-A"}
TEAMS = {"backend", "frontend", "infrastructure"}
EXTRA_LABELS = {"chờ khách", "độ tin thấp"}
ROLES = {"ROLE-AUDIT-VIEW", "ROLE-DELIVERY", "ROLE-INTAKE", "ROLE-JUDGE",
         "ROLE-PARTICIPANT-VIEW", "ROLE-PARTY", "ROLE-REPORT-VIEW",
         "ROLE-RULE-ADMIN", "ROLE-SETTLEMENT", "ROLE-SYS-ADMIN", "ROLE-TRADE"}
KEY_RE = re.compile(r"^E\d{2}(-S\d{2}(-T\d{2})?)?$")
MAX_LEAF_HOURS = 14


def load_items():
    items, errors = [], []
    for path in sorted((REPO / "backlog").glob("items-*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{path.name}: JSON hỏng ({exc})")
            continue
        for item in data:
            item["_file"] = path.name
            items.append(item)
    return items, errors


def check(items, errors):
    by_key = {}
    for it in items:
        key = it.get("key", "")
        where = f"{it['_file']}:{key or '?'}"
        if not KEY_RE.match(key):
            errors.append(f"{where}: key sai dạng")
        if key in by_key:
            errors.append(f"{where}: key trùng với {by_key[key]['_file']}")
        by_key[key] = it
        if it.get("type") not in TYPES:
            errors.append(f"{where}: type '{it.get('type')}' không hợp lệ")
        for field in ("title", "overview"):
            if not it.get(field):
                errors.append(f"{where}: thiếu {field}")
        text = json.dumps(it, ensure_ascii=False)
        if "—" in text or "·" in text:
            errors.append(f"{where}: có dấu kiểu AI")
        if it.get("type") == "epic":
            continue
        if it.get("owner") not in OWNERS:
            errors.append(f"{where}: owner '{it.get('owner')}' không hợp lệ")
        if not it.get("spec_refs"):
            errors.append(f"{where}: thiếu spec_refs")
        if not it.get("acceptance"):
            errors.append(f"{where}: thiếu acceptance")
        if it.get("type") == "devtask" and it.get("team") not in TEAMS:
            errors.append(f"{where}: devtask thiếu team hợp lệ")
        labels = set(it.get("labels_extra", []))
        if labels - EXTRA_LABELS:
            errors.append(f"{where}: nhãn lạ {labels - EXTRA_LABELS}")
        if "chờ khách" in labels and not it.get("customer_wait"):
            errors.append(f"{where}: nhãn chờ khách mà thiếu customer_wait")
        for role in it.get("roles_allowed", []) + it.get("roles_blocked", []):
            if role not in ROLES:
                errors.append(f"{where}: vai trò lạ {role}")

    children = defaultdict(list)
    for it in items:
        if it.get("type") != "epic":
            parent = it.get("parent")
            if parent not in by_key:
                errors.append(f"{it['_file']}:{it.get('key')}: parent '{parent}' không có")
            elif not it["key"].startswith(parent + "-"):
                errors.append(f"{it['_file']}:{it.get('key')}: key không nằm dưới parent {parent}")
            children[parent].append(it)
        for dep in it.get("depends_on", []):
            if dep not in by_key:
                errors.append(f"{it['_file']}:{it.get('key')}: depends_on '{dep}' không có")

    for it in items:
        if it.get("type") == "epic":
            continue
        where = f"{it['_file']}:{it['key']}"
        if children.get(it["key"]):
            continue
        hours = it.get("rough_hours")
        if not isinstance(hours, (int, float)) or hours <= 0:
            errors.append(f"{where}: lá thiếu rough_hours")
        elif hours > MAX_LEAF_HOURS:
            errors.append(f"{where}: lá {hours} giờ, quá {MAX_LEAF_HOURS}")
    return by_key, children


def summary(items):
    per_epic = defaultdict(Counter)
    hours = Counter()
    for it in items:
        epic = it["key"][:3]
        per_epic[epic][it["type"]] += 1
        if isinstance(it.get("rough_hours"), (int, float)):
            hours[epic] += it["rough_hours"]
    level = defaultdict(Counter)
    for it in items:
        level[it["key"][:3]][it["key"].count("-")] += 1
    print("| Epic | Issue | Sub-issue | Trong đó story | Tổng mục | Giờ thô |")
    print("|---|---|---|---|---|---|")
    for epic in sorted(per_epic):
        lv = level[epic]
        print(f"| {epic} | {lv[1]} | {lv[2]} | {per_epic[epic]['story']} | {lv[1] + lv[2]} | {hours[epic]:g} |")
    print(f"Tổng: {len(items)} mục; theo loại: {dict(Counter(i['type'] for i in items))}")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    items, errors = load_items()
    check(items, errors)
    for e in errors:
        print("LỖI:", e)
    if "--summary" in sys.argv:
        summary(items)
    print("KẾT QUẢ:", "ĐẠT" if not errors else f"CHƯA ĐẠT ({len(errors)} lỗi)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

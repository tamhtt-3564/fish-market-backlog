"""Quy SWP đã review ra giờ ước lượng theo hệ số của từng vai (estimate.md mục 3).

Chạy từ gốc repo:  python scripts/convert-story-points-to-hours.py
Hệ số vai = tổng giờ thô / tổng SWP của các việc lá vai đó (giờ thô ở backlog/items-*.json, bước 2).
Giờ việc lá = SWP × hệ số vai, làm tròn 0,1 giờ. Mục cha = tổng giờ các con.
Ghi backlog/estimated-hours.json và in bảng hệ số, bảng tổng theo epic cho estimate.md.
"""
import json
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    items = {i["key"]: i for f in sorted((REPO / "backlog").glob("items-*.json"))
             for i in json.loads(f.read_text(encoding="utf-8"))}
    points = json.loads((REPO / "backlog" / "story-points.json").read_text(encoding="utf-8"))
    leaves = [k for k, p in points.items() if p["direct"]]

    swp, raw = defaultdict(int), defaultdict(float)
    for k in leaves:
        swp[items[k]["owner"]] += points[k]["swp"]
        raw[items[k]["owner"]] += items[k]["rough_hours"]
    rate = {o: round(raw[o] / swp[o], 2) for o in swp}

    hours = {k: round(points[k]["swp"] * rate[items[k]["owner"]], 1) for k in leaves}
    for key in sorted(points, key=lambda k: -k.count("-")):  # con trước cha
        parent = items[key].get("parent")
        if parent:
            hours[parent] = round(hours.get(parent, 0) + hours[key], 1)
    (REPO / "backlog" / "estimated-hours.json").write_text(
        json.dumps(dict(sorted(hours.items(), key=lambda x: (x[0].count("-"), x[0]))), ensure_ascii=False, indent=1),
        encoding="utf-8")

    print("| Vai | Việc lá | Tổng SWP | Giờ thô bước 2 | Hệ số giờ/SWP | Giờ quy đổi |")
    print("|---|---|---|---|---|---|")
    by_owner = defaultdict(float)
    for k in leaves:
        by_owner[items[k]["owner"]] += hours[k]
    for o in sorted(swp):
        n = sum(1 for k in leaves if items[k]["owner"] == o)
        print(f"| {o} | {n} | {swp[o]} | {raw[o]:g} | {rate[o]} | {by_owner[o]:g} |")
    print(f"| Tổng | {len(leaves)} | {sum(swp.values())} | {sum(raw.values()):g} | | {sum(by_owner.values()):g} |")

    print("\n| Epic | Số issue | Việc lá | Tổng SWP | Tổng giờ |")
    print("|---|---|---|---|---|")
    for epic in sorted(k for k in points if k.count("-") == 0):
        under = [k for k in points if k.startswith(epic + "-")]
        lv = [k for k in under if points[k]["direct"]]
        print(f"| {epic} | {sum(1 for k in under if k.count('-') == 1)} | {len(lv)} | {points[epic]['swp']} | {hours[epic]:g} |")
    print(f"Tổng giờ 19 epic: {sum(hours[k] for k in points if k.count('-') == 0):g}")


if __name__ == "__main__":
    main()

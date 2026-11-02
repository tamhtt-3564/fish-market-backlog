"""Giả lập Sprint 1 (2027-01-11 .. 2027-01-22, 10 ngày làm việc) trên backlog đã ước lượng.

Chạy từ gốc repo:  python scripts/simulate-sprint-1.py
Ghi backlog/sprint-1-simulation.json (việc cam kết, kết quả từng việc, burndown từng ngày) và in tóm tắt.
Đây là SỐ LIỆU GIẢ LẬP: thời gian làm thật = giờ ước × hệ số ngẫu nhiên có hạt cố định, nên chạy lại ra cùng kết quả.

Giả định (progress-report.md mục 1):
- Đội 5,8 người như GĐ2 của LAB-1, cộng BrSE-A 0,5 người; 6 giờ làm thật mỗi người mỗi ngày.
- Cam kết 85% năng lực mỗi vai; chọn việc lá theo thứ tự ưu tiên, chỉ lấy việc có mọi việc phụ thuộc cũng trong sprint.
- Mỗi việc: giờ thật = giờ ước × hệ số (log-chuẩn, trung bình khoảng 1,1). Việc xây dựng trượt review với xác suất 15%, làm lại thêm 30%.
- Xây dựng xong còn 1 ngày review (TL-A) và kiểm (QA-A) mới Closed; thiết kế, ca kiểm thử, tài liệu, vận hành còn 0,5 ngày review.
- Việc làm rõ có nhãn `chờ khách`: BrSE-A hỏi xong, khách trả lời vào ngày ngẫu nhiên từ ngày 3 tới ngày 15.
"""
import json
import math
import random
import sys
from datetime import date, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SEED, DAYS, HOURS_PER_DAY, COMMIT = 20270111, 10, 6, 0.85
FTE = {"BE-A": 1, "BE-B": 1, "FE-A": 1, "FE-B": 0.5, "QA-A": 1, "TL-A": 0.5,
       "Infra-A": 0.4, "Design-A": 0.2, "BA-A": 0.2, "BrSE-A": 0.5}
FIRST = ("E01", "E02", "E03")  # hạ tầng, nền dữ liệu, đăng nhập làm trước
BUILD = {"devtask"}
WORKDAYS = [date(2027, 1, 11) + timedelta(days=d) for d in (0, 1, 2, 3, 4, 7, 8, 9, 10, 11)]


def load():
    items = {i["key"]: i for f in sorted((REPO / "backlog").glob("items-*.json"))
             for i in json.loads(f.read_text(encoding="utf-8"))}
    points = json.loads((REPO / "backlog" / "story-points.json").read_text(encoding="utf-8"))
    hours = json.loads((REPO / "backlog" / "estimated-hours.json").read_text(encoding="utf-8"))
    return items, points, hours


def leaf_deps(key, items, points):
    """Việc lá chịu phụ thuộc của chính nó và của mọi cấp cha; phụ thuộc vào mục cha nghĩa là mọi việc lá bên dưới."""
    deps, node = [], key
    while node:
        deps += items[node].get("depends_on", [])
        node = items[node].get("parent")
    out = set()
    for dep in deps:
        out |= {k for k in points if points[k]["direct"] and (k == dep or k.startswith(dep + "-"))}
    return out - {key}


def select(items, points, hours):
    leaves = [k for k in points if points[k]["direct"]]
    rank = lambda k: (0 if k.startswith(FIRST) or items[k]["type"] == "investigation" else 1, k)
    budget = {o: FTE[o] * DAYS * HOURS_PER_DAY * COMMIT for o in FTE}
    chosen, changed = [], True
    while changed:
        changed = False
        for k in sorted(leaves, key=rank):
            o = items[k]["owner"]
            if k in chosen or o not in budget or hours[k] > budget[o]:
                continue
            if leaf_deps(k, items, points) <= set(chosen):
                chosen.append(k)
                budget[o] -= hours[k]
                changed = True
    return chosen


def simulate(chosen, items, points, hours):
    rng = random.Random(SEED)

    def draw():
        return rng.lognormvariate(math.log(1.1) - 0.08, 0.4), rng.random(), rng.randint(3, 15)

    draws = {k: draw() for k in chosen}  # rút theo thứ tự cam kết, để kết quả không phụ thuộc thứ tự làm
    free = {o: 0.0 for o in FTE}  # giờ đã dùng của từng vai, tính theo năng lực của vai
    finish, result, todo = {}, {}, list(chosen)

    def ready_day(k):
        cap = FTE[items[k]["owner"]] * HOURS_PER_DAY
        return max(free[items[k]["owner"]] / cap, max((finish[d] for d in leaf_deps(k, items, points)), default=0))

    def pull_candidate():
        """Người còn từ 1 ngày trống kéo việc lá sẵn sàng từ backlog (không chờ khách), ưu tiên việc bắt đầu sớm nhất."""
        pool = [k for k in points if points[k]["direct"] and k not in finish and items[k]["owner"] in FTE
                and "chờ khách" not in items[k].get("labels_extra", []) and leaf_deps(k, items, points) <= finish.keys()]
        pool = [k for k in pool if ready_day(k) <= DAYS - 1]
        return min(pool, key=lambda k: (ready_day(k), k)) if pool else None

    while todo or (k := pull_candidate()):
        if todo:
            # việc cam kết: lấy việc bắt đầu được sớm nhất (mọi việc phụ thuộc đã có lịch); hoà thì theo thứ tự cam kết
            k = min((x for x in todo if leaf_deps(x, items, points) <= finish.keys()), key=lambda x: (ready_day(x), todo.index(x)))
            todo.remove(k)
        else:
            draws[k] = draw()
        added = k not in chosen
        it, o = items[k], items[k]["owner"]
        factor, fail_draw, answer_draw = draws[k]
        failed = it["type"] in BUILD and fail_draw < 0.15
        actual = hours[k] * factor * (1.3 if failed else 1)
        cap = FTE[o] * HOURS_PER_DAY  # giờ mỗi ngày của vai
        start_day = ready_day(k)
        answer_day = answer_draw if "chờ khách" in it.get("labels_extra", []) else None
        end_day = start_day + actual / cap
        free[o] = end_day * cap
        review = 1 if it["type"] in BUILD else (0 if it["type"] == "investigation" else 0.5)
        done_day = max(end_day + review, answer_day or 0)
        finish[k] = done_day
        worked = max(0.0, min(actual, (DAYS - start_day) * cap))
        if answer_day and answer_day > DAYS and end_day <= DAYS:
            status = "Pending"
        elif done_day <= DAYS:
            status = "Closed"
        elif end_day <= DAYS:
            status = "QA Testing" if it["type"] in BUILD and end_day + 0.5 <= DAYS else "In Review"
        elif start_day < DAYS:
            status = "Technical Review Failed" if failed and start_day + hours[k] / cap <= DAYS else "In Progress"
        else:
            status = "Issued Tasks"
        result[k] = {"owner": o, "swp": points[k]["swp"], "estimated_hours": hours[k],
                     "actual_hours_total": round(actual, 1), "spent_hours": round(worked, 1),
                     "start_day": round(start_day, 2), "dev_end_day": round(end_day, 2), "done_day": round(done_day, 2),
                     "customer_answer_day": answer_day, "review_failed": failed, "status": status,
                     "added_mid_sprint": added}
    return result


def burndown(result):
    """Còn lại cuối mỗi ngày = phạm vi tới ngày đó (cam kết + việc kéo thêm đã bắt đầu) trừ phần đã Closed."""
    committed = sum(r["swp"] for r in result.values() if not r["added_mid_sprint"])
    rows = []
    for d in range(DAYS + 1):
        scope = sum(r["swp"] for r in result.values() if not r["added_mid_sprint"] or r["start_day"] < d)
        done = sum(r["swp"] for r in result.values() if r["done_day"] <= d and r["status"] == "Closed")
        rows.append({"day": d, "date": None if d == 0 else WORKDAYS[d - 1].isoformat(),
                     "ideal": round(committed * (1 - d / DAYS), 1), "scope": scope, "remaining": scope - done})
    return rows


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    items, points, hours = load()
    chosen = select(items, points, hours)
    result = simulate(chosen, items, points, hours)
    data = {"sprint": "Sprint 1", "start": "2027-01-11", "end": "2027-01-22", "seed": SEED, "fte": FTE,
            "hours_per_day": HOURS_PER_DAY, "commit_ratio": COMMIT,
            "workdays": [d.isoformat() for d in WORKDAYS], "items": result, "burndown": burndown(result)}
    (REPO / "backlog" / "sprint-1-simulation.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    from collections import Counter
    st = Counter(r["status"] for r in result.values())
    for added in (False, True):
        part = [r for r in result.values() if r["added_mid_sprint"] == added]
        print("kéo thêm" if added else "cam kết", len(part), "việc,", sum(r["swp"] for r in part), "SWP,",
              round(sum(r["estimated_hours"] for r in part), 1), "giờ ước")
    print("trạng thái", dict(st))
    print("burndown", [(b["day"], b["ideal"], b["scope"], b["remaining"]) for b in data["burndown"]])


if __name__ == "__main__":
    main()

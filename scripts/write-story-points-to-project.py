"""Ghi SWP đã review (backlog/story-points.json) và giờ ước lượng (backlog/estimated-hours.json) lên Project #1.

Chạy từ gốc repo:  python scripts/write-story-points-to-project.py [--only-hours]
Leaf issue: ghi Story Point, Scope, Complexity. Mục cha (epic, story, issue có sub-issue): ghi Story Point = tổng SWP các con.
Có file giờ thì ghi thêm Estimated time cho mọi mục; --only-hours chỉ ghi Estimated time.
Gộp 10 lệnh mỗi lần gọi; ghi lại cùng giá trị thì không đổi gì nên chạy lại được.
"""
import json
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OWNER, PROJECT_NO, BATCH = "tamhtt-3564", 1, 10


def gql(query, variables=None):
    payload = json.dumps({"query": query, "variables": variables or {}})
    for attempt in range(4):
        res = subprocess.run(["gh", "api", "graphql", "--input", "-"], input=payload,
                             capture_output=True, text=True, encoding="utf-8")
        if res.returncode == 0 and '"errors"' not in res.stdout:
            return json.loads(res.stdout)["data"]
        print(f"  lỗi, chờ {10 * (attempt + 1)}s: {(res.stdout + res.stderr).strip()[:200]}", flush=True)
        time.sleep(10 * (attempt + 1))
    raise SystemExit("Dừng: lỗi lặp lại, chạy lại script để làm tiếp")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    points = json.loads((REPO / "backlog" / "story-points.json").read_text(encoding="utf-8"))
    state = json.loads((REPO / "backlog" / "issue-numbers.json").read_text(encoding="utf-8"))
    d = gql("""query($o:String!,$p:Int!){user(login:$o){projectV2(number:$p){id
      fields(first:40){nodes{... on ProjectV2Field{id name}}}}}}""", {"o": OWNER, "p": PROJECT_NO})
    proj = d["user"]["projectV2"]
    fields = {f["name"]: f["id"] for f in proj["fields"]["nodes"] if f}
    hours_path = REPO / "backlog" / "estimated-hours.json"
    hours = json.loads(hours_path.read_text(encoding="utf-8")) if hours_path.exists() else {}
    only_hours = "--only-hours" in sys.argv
    sets = []
    for key, p in points.items():
        values = {} if only_hours else {"Story Point": p["swp"]}
        if p["direct"] and not only_hours:
            values.update({"Scope": p["scope"], "Complexity": p["complexity"]})
        if key in hours:
            values["Estimated time"] = hours[key]
        sets += [(state[key]["item"], fields[name], v) for name, v in values.items()]
    for start in range(0, len(sets), BATCH):
        chunk = sets[start:start + BATCH]
        body = " ".join(
            f'm{n}: updateProjectV2ItemFieldValue(input:{{projectId:"{proj["id"]}",itemId:"{item}",fieldId:"{field}",value:{{number:{value}}}}}){{clientMutationId}}'
            for n, (item, field, value) in enumerate(chunk))
        gql("mutation{" + body + "}")
        print(f"[{min(start + BATCH, len(sets))}/{len(sets)}]", flush=True)
        time.sleep(1)


if __name__ == "__main__":
    main()

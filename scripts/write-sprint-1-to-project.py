"""Ghi kết quả giả lập Sprint 1 (backlog/sprint-1-simulation.json) lên Project #1.

Chạy từ gốc repo:  python scripts/write-sprint-1-to-project.py
Mỗi việc cam kết: Target version = Sprint 1, Status cuối sprint, Due Date = 2027-01-22,
Start Date = ngày bắt đầu giả lập (việc đã bắt đầu), Spent time = giờ đã làm trong sprint.
Đóng issue có Status Closed, mở lại issue khác nếu đang đóng (D5-25). Ghi lại cùng giá trị thì không đổi gì nên chạy lại được.
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


def stale_sprint_items(sprint):
    """Mã mục Project đang có Target version = sprint (đọc toàn bộ Project, 100 mục mỗi trang)."""
    found, cursor = set(), None
    while True:
        page = gql("""query($o:String!,$p:Int!,$c:String){user(login:$o){projectV2(number:$p){items(first:100,after:$c){
          pageInfo{hasNextPage endCursor} nodes{id t:fieldValueByName(name:"Target version"){
          ... on ProjectV2ItemFieldIterationValue{title}}}}}}}""", {"o": OWNER, "p": PROJECT_NO, "c": cursor})
        items = page["user"]["projectV2"]["items"]
        found |= {n["id"] for n in items["nodes"] if (n["t"] or {}).get("title") == sprint}
        if not items["pageInfo"]["hasNextPage"]:
            return found
        cursor = items["pageInfo"]["endCursor"]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sim = json.loads((REPO / "backlog" / "sprint-1-simulation.json").read_text(encoding="utf-8"))
    state = json.loads((REPO / "backlog" / "issue-numbers.json").read_text(encoding="utf-8"))
    d = gql("""query($o:String!,$p:Int!){user(login:$o){projectV2(number:$p){id fields(first:40){nodes{
      ... on ProjectV2Field{id name} ... on ProjectV2SingleSelectField{id name options{id name}}
      ... on ProjectV2IterationField{id name configuration{iterations{id title}}}}}}}}""", {"o": OWNER, "p": PROJECT_NO})
    proj = d["user"]["projectV2"]
    f = {x["name"]: x for x in proj["fields"]["nodes"] if x}
    status_opt = {o["name"]: o["id"] for o in f["Status"]["options"]}
    sprint = next(i["id"] for i in f["Target version"]["configuration"]["iterations"] if i["title"] == sim["sprint"])
    sets = []
    for key, r in sim["items"].items():
        values = [(f["Target version"]["id"], f'iterationId:"{sprint}"'),
                  (f["Status"]["id"], f'singleSelectOptionId:"{status_opt[r["status"]]}"'),
                  (f["Due Date"]["id"], f'date:"{sim["end"]}"'),
                  (f["Spent time"]["id"], f'number:{r["spent_hours"]}')]
        if r["start_day"] < len(sim["workdays"]):
            values.append((f["Start Date"]["id"], f'date:"{sim["workdays"][int(r["start_day"])]}"'))
        else:
            values.append((f["Start Date"]["id"], None))  # chưa bắt đầu: xoá ngày cũ nếu có
        sets += [(state[key]["item"], field, value) for field, value in values]
    # Việc từng ghi vào Sprint 1 ở lần chạy trước mà nay không còn: trả về New, xoá các trường sprint
    in_sprint = {state[k]["item"] for k in sim["items"]}
    for item in stale_sprint_items(sim["sprint"]) - in_sprint:
        sets.append((item, f["Status"]["id"], f'singleSelectOptionId:"{status_opt["New"]}"'))
        sets += [(item, f[name]["id"], None) for name in ("Target version", "Start Date", "Due Date", "Spent time")]

    def call(n, item, field, value):
        ids = f'projectId:"{proj["id"]}",itemId:"{item}",fieldId:"{field}"'
        if value is None:
            return f"m{n}: clearProjectV2ItemFieldValue(input:{{{ids}}}){{clientMutationId}}"
        return f"m{n}: updateProjectV2ItemFieldValue(input:{{{ids},value:{{{value}}}}}){{clientMutationId}}"

    for start in range(0, len(sets), BATCH):
        body = " ".join(call(n, *s) for n, s in enumerate(sets[start:start + BATCH]))
        gql("mutation{" + body + "}")
        print(f"[{min(start + BATCH, len(sets))}/{len(sets)}]", flush=True)
        time.sleep(1)
    sync_issue_state(sim, state)


def sync_issue_state(sim, state):
    """Issue có Status Closed thì đóng (completed); mọi issue khác mở lại nếu đang đóng, để issue khớp board."""
    closed = {state[k]["number"] for k, r in sim["items"].items() if r["status"] == "Closed"}
    current, cursor = {}, None
    while True:
        page = gql("""query($o:String!,$n:String!,$c:String){repository(owner:$o,name:$n){issues(first:100,after:$c){
          pageInfo{hasNextPage endCursor} nodes{number id state}}}}""",
                   {"o": OWNER, "n": "fish-market-backlog", "c": cursor})["repository"]["issues"]
        current.update({n["number"]: (n["id"], n["state"]) for n in page["nodes"]})
        if not page["pageInfo"]["hasNextPage"]:
            break
        cursor = page["pageInfo"]["endCursor"]
    for number, (issue_id, now) in sorted(current.items()):
        if number in closed and now == "OPEN":
            gql("mutation($i:ID!){closeIssue(input:{issueId:$i,stateReason:COMPLETED}){clientMutationId}}", {"i": issue_id})
        elif number not in closed and now == "CLOSED":
            gql("mutation($i:ID!){reopenIssue(input:{issueId:$i}){clientMutationId}}", {"i": issue_id})
        else:
            continue
        print(f"#{number} {'đóng' if number in closed else 'mở lại'}", flush=True)
        time.sleep(1)


if __name__ == "__main__":
    main()

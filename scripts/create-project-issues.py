"""Tạo issue trên repo và GitHub Project từ backlog/items-*.json.

Chạy từ gốc repo:
    python scripts/create-project-issues.py [--only E16] [--delay 7.5]   # tạo issue, gắn cha, đưa vào Project, đặt Status và Phụ trách
    python scripts/create-project-issues.py --link-blocked-by            # nối quan hệ blocked by từ depends_on
Ghi kết quả dần vào backlog/issue-numbers.json ({key: {number, id, item}}) nên chạy lại được sau khi bị ngắt.
Đi chậm (mặc định 7,5 giây mỗi mục, dưới 500 lệnh tạo nội dung mỗi giờ); bị chặn tạm thì chờ rồi thử lại.
"""
import json
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OWNER, NAME, PROJECT_NO = "tamhtt-3564", "fish-market-backlog", 1
STATE = REPO / "backlog" / "issue-numbers.json"


def gql(query, variables=None, tries=6):
    payload = json.dumps({"query": query, "variables": variables or {}})
    for attempt in range(tries):
        res = subprocess.run(["gh", "api", "graphql", "--input", "-"], input=payload,
                             capture_output=True, text=True, encoding="utf-8")
        out = res.stdout + res.stderr
        if res.returncode == 0 and '"errors"' not in res.stdout:
            return json.loads(res.stdout)["data"]
        wait = 120 * (attempt + 1) if ("rate limit" in out.lower() or "too quickly" in out) else 10
        print(f"  lỗi, chờ {wait}s: {out.strip()[:200]}", flush=True)
        time.sleep(wait)
    raise SystemExit("Dừng: lỗi lặp lại, chạy lại script để làm tiếp")


def load_items():
    items = [i for f in sorted((REPO / "backlog").glob("items-*.json"))
             for i in json.loads(f.read_text(encoding="utf-8"))]
    return sorted(items, key=lambda i: (i["key"].count("-"), i["key"]))  # cha trước con


def lookup():
    d = gql("""query($o:String!,$n:String!,$p:Int!){repository(owner:$o,name:$n){id labels(first:100){nodes{id name}}}
      user(login:$o){projectV2(number:$p){id fields(first:40){nodes{... on ProjectV2SingleSelectField{id name options{id name}}}}}}}""",
            {"o": OWNER, "n": NAME, "p": PROJECT_NO})
    labels = {l["name"]: l["id"] for l in d["repository"]["labels"]["nodes"]}
    proj = d["user"]["projectV2"]
    fields = {f["name"]: f for f in proj["fields"]["nodes"] if f}
    return d["repository"]["id"], labels, proj["id"], fields


def body(it):
    lines = ["## Overview", it["overview"], ""]
    if it.get("acceptance"):
        lines += ["## Acceptance Criteria"] + [f"- [ ] {a}" for a in it["acceptance"]] + [""]
    lines += ["## References & Dependencies", f"- Nguồn spec LAB-4 và PREMISE: {', '.join(f'`{r}`' for r in it.get('spec_refs', []))}"]
    if it.get("depends_on"):
        lines.append(f"- Phụ thuộc (mã backlog, xem quan hệ blocked by): {', '.join(it['depends_on'])}")
    lines.append("")
    if it.get("roles_allowed") or it.get("roles_blocked"):
        lines += ["## Vai trò người dùng hệ thống",
                  f"- Được làm: {', '.join(it.get('roles_allowed', [])) or 'không có'}",
                  f"- Bị chặn (chặn ở hàm DB hoặc API): {', '.join(it.get('roles_blocked', [])) or 'không có'}", ""]
    if it.get("customer_wait"):
        lines += ["## Chờ khách", it["customer_wait"], ""]
    if it.get("team"):
        lines += ["## Technical Approach", f"Team: {it['team']}", ""]
    lines.append(f"Mã backlog: `{it['key']}`. Nguồn: `backlog/items-*.json` của repo này.")
    return "\n".join(lines)


def create(items, only, delay):
    state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}
    repo_id, labels, proj_id, fields = lookup()
    status, owner_f = fields["Status"], fields["Phụ trách (giả định)"]
    new_opt = next(o["id"] for o in status["options"] if o["name"] == "New")
    owners = {o["name"]: o["id"] for o in owner_f["options"]}
    todo = [i for i in items if "item" not in state.get(i["key"], {}) and (not only or i["key"].startswith(only))]
    print(f"Cần tạo {len(todo)} mục", flush=True)
    for n, it in enumerate(todo, 1):
        names = [f"type:{it['type']}"] + ([f"team:{it['team']}"] if it.get("team") else []) + it.get("labels_extra", [])
        var = {"input": {"repositoryId": repo_id, "title": f"{it['key']} {it['title']}", "body": body(it),
                         "labelIds": [labels[x] for x in names]}}
        if it.get("parent"):
            var["input"]["parentIssueId"] = state[it["parent"]]["id"]
        if it["key"] in state:  # issue đã tạo ở lần chạy trước, chỉ còn thiếu bước Project
            d = state[it["key"]]
        else:
            d = gql("mutation($input:CreateIssueInput!){createIssue(input:$input){issue{id number}}}", var)["createIssue"]["issue"]
            state[it["key"]] = {"number": d["number"], "id": d["id"]}
            STATE.write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")
        # Đưa vào Project bằng lệnh riêng: trả mã mục ngay, gọi lại không tạo trùng
        item = gql("mutation($p:ID!,$c:ID!){addProjectV2ItemById(input:{projectId:$p,contentId:$c}){item{id}}}",
                   {"p": proj_id, "c": d["id"]})["addProjectV2ItemById"]["item"]["id"]
        sets = [f's: updateProjectV2ItemFieldValue(input:{{projectId:"{proj_id}",itemId:"{item}",fieldId:"{status["id"]}",value:{{singleSelectOptionId:"{new_opt}"}}}}){{clientMutationId}}']
        if it.get("owner"):
            sets.append(f'o: updateProjectV2ItemFieldValue(input:{{projectId:"{proj_id}",itemId:"{item}",fieldId:"{owner_f["id"]}",value:{{singleSelectOptionId:"{owners[it["owner"]]}"}}}}){{clientMutationId}}')
        gql("mutation{" + " ".join(sets) + "}")
        state[it["key"]] = {"number": d["number"], "id": d["id"], "item": item}
        STATE.write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"[{n}/{len(todo)}] {it['key']} -> #{d['number']}", flush=True)
        time.sleep(delay)


def link_blocked_by(items, delay):
    state = json.loads(STATE.read_text(encoding="utf-8"))
    done_path = REPO / "backlog" / "blocked-by-done.json"
    done = set(json.loads(done_path.read_text(encoding="utf-8"))) if done_path.exists() else set()
    pairs = [(i["key"], d) for i in items for d in i.get("depends_on", []) if f"{i['key']}<{d}" not in done]
    print(f"Cần nối {len(pairs)} quan hệ", flush=True)
    for n, (key, dep) in enumerate(pairs, 1):
        gql("mutation($a:ID!,$b:ID!){addBlockedBy(input:{issueId:$a,blockingIssueId:$b}){clientMutationId}}",
            {"a": state[key]["id"], "b": state[dep]["id"]})
        done.add(f"{key}<{dep}")
        done_path.write_text(json.dumps(sorted(done)), encoding="utf-8")
        print(f"[{n}/{len(pairs)}] {key} blocked by {dep}", flush=True)
        time.sleep(delay)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    args = sys.argv[1:]
    delay = float(args[args.index("--delay") + 1]) if "--delay" in args else 7.5
    items = load_items()
    if "--link-blocked-by" in args:
        link_blocked_by(items, delay)
    else:
        create(items, args[args.index("--only") + 1] if "--only" in args else None, delay)


if __name__ == "__main__":
    main()

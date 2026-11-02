"""Theo dõi 18 issue làm rõ (type investigation): issue chịu ảnh hưởng, hạn trả lời, câu trả lời giả lập.

Chạy từ gốc repo:  python scripts/record-clarification-follow-up.py [--github]
1. Ghi vào backlog/items-*.json: `affects` (mã issue chịu ảnh hưởng, lấy từ nội dung issue, thêm tay chỗ nội dung
   không ghi mã), `answer_due` (hạn trả lời), và với việc đã Closed trong giả lập Sprint 1: `answer` (câu trả lời
   giả lập) và gỡ nhãn `chờ khách` (giữ `customer_wait` làm lịch sử).
2. --github: gỡ nhãn `chờ khách` trên GitHub cho việc đã trả lời; đặt Due Date trên Project = `answer_due` cho việc
   chưa vào sprint. Thân issue cập nhật bằng `python scripts/create-project-issues.py --refresh-bodies`.
Hạn trả lời: việc trong Sprint 1 còn chờ thì theo bảng rủi ro của progress-report.md; việc chưa vào sprint dùng hạn
tạm hết Sprint 2 (2027-02-05), dời sớm hơn khi xếp sprint cho issue chịu ảnh hưởng.
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DEFAULT_DUE = "2027-02-05"
SPRINT_DUE = {"E05-S07": "2027-02-01", "E11-S09": "2027-02-05", "E11-S12": "2027-02-05"}
MANUAL_AFFECTS = {"E01-S09": ["E01-S02", "E01-S05"], "E11-S14": ["E11-S02"]}  # nội dung issue không ghi mã
KEY = re.compile(r"E\d\d-S\d\d(?:-T\d\d)?")


def load_gql():
    spec = importlib.util.spec_from_file_location("cpi", REPO / "scripts" / "create-project-issues.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.gql


def update_json():
    files = {p: json.loads(p.read_text(encoding="utf-8")) for p in sorted((REPO / "backlog").glob("items-*.json"))}
    items = {i["key"]: i for data in files.values() for i in data}
    sim = json.loads((REPO / "backlog" / "sprint-1-simulation.json").read_text(encoding="utf-8"))
    answered = []
    for key, it in items.items():
        if it["type"] != "investigation":
            continue
        text = " ".join([it["overview"], it.get("customer_wait", "")] + it.get("acceptance", []))
        blocked = [k for k, other in items.items() if key in other.get("depends_on", [])]
        it["affects"] = sorted(set(KEY.findall(text)) - {key} | set(blocked) | set(MANUAL_AFFECTS.get(key, [])))
        run = sim["items"].get(key)
        it["answer_due"] = SPRINT_DUE.get(key, sim["end"] if run else DEFAULT_DUE)
        if run and run["status"] == "Closed" and run.get("customer_answer_day"):
            day = sim["workdays"][run["customer_answer_day"] - 1]
            it["answer"] = f"(giả lập) Khách trả lời ngày {day}: chọn phương án mặc định ghi ở Overview; issue chịu ảnh hưởng giữ ước lượng."
            it["labels_extra"] = [x for x in it.get("labels_extra", []) if x != "chờ khách"]
            answered.append(key)
    for path, data in files.items():
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return items, answered, sim


def sync_github(items, answered, sim):
    gql = load_gql()
    state = json.loads((REPO / "backlog" / "issue-numbers.json").read_text(encoding="utf-8"))
    label = gql("""query{repository(owner:"tamhtt-3564",name:"fish-market-backlog"){label(name:"chờ khách"){id}}}""")
    label_id = label["repository"]["label"]["id"]
    for key in answered:
        gql("mutation($i:ID!,$l:[ID!]!){removeLabelsFromLabelable(input:{labelableId:$i,labelIds:$l}){clientMutationId}}",
            {"i": state[key]["id"], "l": [label_id]})
        print(f"gỡ nhãn chờ khách: {key} #{state[key]['number']}", flush=True)
    proj = gql("""query{user(login:"tamhtt-3564"){projectV2(number:1){id field(name:"Due Date"){... on ProjectV2Field{id}}}}}""")
    pid, fid = proj["user"]["projectV2"]["id"], proj["user"]["projectV2"]["field"]["id"]
    for key, it in sorted(items.items()):
        if it["type"] == "investigation" and key not in sim["items"]:
            gql("mutation($p:ID!,$i:ID!,$f:ID!,$d:Date!){updateProjectV2ItemFieldValue(input:{projectId:$p,itemId:$i,fieldId:$f,value:{date:$d}}){clientMutationId}}",
                {"p": pid, "i": state[key]["item"], "f": fid, "d": it["answer_due"]})
            print(f"Due Date {it['answer_due']}: {key} #{state[key]['number']}", flush=True)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    items, answered, sim = update_json()
    print(f"18 issue làm rõ: đã trả lời (giả lập) {len(answered)}: {answered}")
    if "--github" in sys.argv:
        sync_github(items, answered, sim)


if __name__ == "__main__":
    main()

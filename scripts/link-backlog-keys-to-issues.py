"""Đổi mã backlog (E11-S05, E11-S05-T02) trong file Markdown thành link tới issue trên GitHub.

Chạy từ gốc repo:  python scripts/link-backlog-keys-to-issues.py task-breakdown.md PREMISE.md
Đọc số issue ở backlog/issue-numbers.json. Bỏ qua mã trong `code` và mã đã là link, nên chạy lại không đổi gì thêm.
"""
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ISSUE_URL = "https://github.com/tamhtt-3564/fish-market-backlog/issues/{}"
KEY = re.compile(r"(?<![\[\w/-])(E\d{2}-S\d{2}(?:-T\d{2})?)(?![\w\]-])")


def link_line(line, numbers, missing):
    parts = line.split("`")
    for i in range(0, len(parts), 2):  # phần chẵn nằm ngoài `code`
        def repl(m):
            key = m.group(1)
            if key not in numbers:
                missing.add(key)
                return key
            return f"[{key}]({ISSUE_URL.format(numbers[key]['number'])})"
        parts[i] = KEY.sub(repl, parts[i])
    return "`".join(parts)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    numbers = json.loads((REPO / "backlog" / "issue-numbers.json").read_text(encoding="utf-8"))
    for name in sys.argv[1:]:
        path = REPO / name
        missing = set()
        text = path.read_text(encoding="utf-8")
        new = "\n".join(link_line(l, numbers, missing) for l in text.split("\n"))
        path.write_text(new, encoding="utf-8")
        print(f"{name}: {new.count('](' + ISSUE_URL.format(''))} link; mã không có issue: {sorted(missing) or 'không'}")


if __name__ == "__main__":
    main()

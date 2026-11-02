"""Cổng kiểm máy LAB-5: soát các file Markdown ở gốc repo nộp bài fish-market-backlog.

Chạy từ gốc project claude-practice:
    python .claude/skills/lab5-review-backlog-output/scripts/run-lab5-backlog-gate.py <bước 0-9>

Kiểm: đủ file theo bước, không dấu kiểu AI, không chép câu RFP tiếng Nhật,
không lộ khoá bí mật / email, PREMISE một dòng thì đúng câu của đề,
完納奨励金 có mặt ở task-breakdown. Thoát mã 1 khi có LỖI.
"""
import re
import sys
import unicodedata
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[4]
REPO = PROJECT_ROOT / "fish-market-backlog"
RFP_FILE = PROJECT_ROOT / "rfp" / "product-a-rfp-ja.txt"

# File bắt buộc xuất hiện từ bước nào trở đi (theo kế hoạch LAB-5).
FILES_BY_STEP = {
    "PREMISE.md": 1,
    "task-breakdown.md": 2,
    "estimate.md": 5,
    "progress-report.md": 6,
    "README.md": 7,
    "AI-report.md": 8,
}
NO_CHANGE_LINE = "Không thay đổi so với LAB-4"
MIN_COPY_RUN = 12  # chuỗi tiếng Nhật dài từ 12 ký tự trùng RFP coi là chép
JA_RUN = re.compile(r"[぀-ヿ一-鿿々ー。、・「」（）]{%d,}" % MIN_COPY_RUN)
SECRET_PATTERNS = {
    "khoá GitHub": re.compile(r"\bgh[opsu]_[A-Za-z0-9]{20,}"),
    "khoá JWT / Supabase": re.compile(r"\beyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{10,}"),
    "khoá API": re.compile(r"\bsk-[A-Za-z0-9]{20,}"),
    "service_role": re.compile(r"service_role\s*[:=]\s*\S{20,}"),
    "email": re.compile(r"[\w.+-]+@(?!users\.noreply\.github\.com|anthropic\.com)[\w-]+\.[\w.]+"),
}


def norm(text):
    return unicodedata.normalize("NFKC", text)


def root_markdown_files():
    return sorted(p for p in REPO.glob("*.md") if p.is_file())


def backlog_data_files():
    """Dữ liệu backlog thành nội dung issue public: quét chép RFP và dấu kiểu AI như file Markdown."""
    return sorted((REPO / "backlog").glob("items-*.json"))


def check_required(step, errors):
    for name, from_step in FILES_BY_STEP.items():
        if step >= from_step and not (REPO / name).is_file():
            errors.append(f"Thiếu file bắt buộc ở gốc repo: {name} (cần từ bước {from_step})")


def check_ai_punctuation(files, errors):
    for path in files:
        for no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for mark in (chr(0x2014), chr(0xB7)):  # gạch dài, chấm giữa dòng
                if mark in line:
                    errors.append(f"{path.name}:{no}: dấu kiểu AI '{mark}'")


def check_rfp_copy(files, errors, warnings):
    if not RFP_FILE.is_file():
        warnings.append(f"Không thấy RFP ở {RFP_FILE}, bỏ qua kiểm chép câu RFP")
        return
    rfp = norm(RFP_FILE.read_text(encoding="utf-8"))
    for path in files:
        for no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for run in JA_RUN.findall(norm(line)):
                if run in rfp:
                    errors.append(f"{path.name}:{no}: chép nguyên câu RFP ({run[:20]}...), repo public không được chép RFP")


def check_secrets(errors):
    for path in REPO.rglob("*"):
        if not path.is_file() or ".git" in path.parts or path.suffix not in {".md", ".html", ".json", ".csv", ".py", ".txt"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for label, pattern in SECRET_PATTERNS.items():
            for hit in pattern.findall(text):
                errors.append(f"{path.relative_to(REPO)}: nghi lộ {label}: {hit[:24]}")


def check_commit_emails(errors):
    """Repo public: email tác giả và người commit phải là địa chỉ noreply của GitHub."""
    import subprocess
    out = subprocess.run(["git", "-C", str(REPO), "log", "--format=%h %ae %ce"],
                         capture_output=True, text=True, encoding="utf-8").stdout
    for line in out.splitlines():
        sha, *emails = line.split()
        for email in emails:
            if not email.endswith("@users.noreply.github.com"):
                errors.append(f"commit {sha}: email {email} lộ trong lịch sử repo public")


def check_premise(errors):
    path = REPO / "PREMISE.md"
    if not path.is_file():
        return
    lines = [l.strip() for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
    if len(lines) == 1 and lines[0].strip("“”\"") != NO_CHANGE_LINE:
        errors.append(f"PREMISE.md chỉ một dòng nhưng không đúng câu của đề: '{NO_CHANGE_LINE}'")


def check_special_constraint(step, errors):
    path = REPO / "task-breakdown.md"
    if step >= 2 and path.is_file() and "完納奨励金" not in path.read_text(encoding="utf-8"):
        errors.append("task-breakdown.md không nhắc 完納奨励金 (ràng buộc đặc thù của đề Product A)")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) != 2 or not sys.argv[1].isdigit():
        print(__doc__)
        return 2
    step = int(sys.argv[1])
    if not REPO.is_dir():
        print(f"LỖI: không thấy repo nộp bài ở {REPO}")
        return 1
    errors, warnings = [], []
    files = root_markdown_files()
    check_required(step, errors)
    check_ai_punctuation(files + backlog_data_files(), errors)
    # Báo cáo HTML của skill chấm SWP chứa tiêu đề, lý do chấm: quét chép RFP; dấu câu do skill sinh nên không quét
    skill_files = sorted(p for p in (REPO / "skills").rglob("*") if p.suffix in {".md", ".py"})
    check_rfp_copy(files + backlog_data_files() + sorted((REPO / "estimate").rglob("*.html")) + skill_files, errors, warnings)
    check_ai_punctuation(skill_files, errors)
    check_secrets(errors)
    check_commit_emails(errors)
    check_premise(errors)
    check_special_constraint(step, errors)

    print(f"Cổng LAB-5 bước {step}: {len(files)} file Markdown ở gốc repo")
    for w in warnings:
        print(f"  CẢNH BÁO: {w}")
    for e in errors:
        print(f"  LỖI: {e}")
    print("KẾT QUẢ:", "ĐẠT" if not errors else f"CHƯA ĐẠT ({len(errors)} lỗi)")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())

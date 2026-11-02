# Backlog chợ thủy sản 桜水産市場 (LAB-5)

- **Dự án:** hệ thống quản lý giao dịch chợ thủy sản 桜水産市場, backlog giai đoạn xây dựng
- **Mã học viên:** tamhtt-3564 (tài khoản GitHub)
- **Đề:** Product A

## 1. Tổng quan

- **Backlog chia từ bản LAB-4 nào:** bộ spec LAB-4 ở nhánh `lab4-specs` của repo `tamhtt-3564/fish-market-prototype`. Bản nộp LAB-4 là commit `418d444` (2026-10-30); backlog dùng commit `21bbe4b` (2026-11-01), là bản nộp cộng thiết kế màn SCR-25 完納奨励金 thêm sau đó.
- **PREMISE.md có thay đổi:** có. 7 dòng thêm hoặc sửa spec (S-01..S-07), 24 giả định bổ sung đang dùng (G-01..G-25, G-12 đã thay bằng S-07), 6 hướng đã chốt (H-01..H-06).
- **Backlog:** 19 epic, 161 issue, 612 sub-issue, cộng 792 mục trên [Project #1](https://github.com/users/tamhtt-3564/projects/1). Tổng 2.187 SWP đã review, 4.038,7 giờ (577,0 MD); so với estimate LAB-1 (805 MD) ở `estimate.md` mục 5.
- **Sprint giả lập đã chạy:** Sprint 1 (2027-01-11 tới 2027-01-22): 69 việc, xong 115/205 SWP; báo cáo ở `progress-report.md`.

## 2. Link

- **Repo:** https://github.com/tamhtt-3564/fish-market-backlog
- **GitHub Project:** https://github.com/users/tamhtt-3564/projects/1 (7 view: "View 1" là bảng tất cả mục, bảng trạng thái, theo người phụ trách, nhóm theo issue cha, epic, 完納奨励金, chờ khách)
- **Báo cáo HTML của skill chấm SWP:** [`estimate/reports/sun-estimate-fish-market-backlog-project-1-20261102.html`](estimate/reports/sun-estimate-fish-market-backlog-project-1-20261102.html). File nặng 2,15 MB nên GitHub không hiển thị trực tiếp: ở trang file, bấm biểu tượng tải về (Download raw file) rồi mở file bằng trình duyệt (chạy được không cần mạng).
- **Bộ spec LAB-4:** https://github.com/tamhtt-3564/fish-market-prototype/tree/lab4-specs/specs (repo private vì spec có câu trích RFP; người chấm cần được mời vào repo). Phần SCR-25 mà backlog dựa nhiều nhất có bản tóm tắt tự viết ở `spec-summary/`.
- **Đã mở thử không đăng nhập** (trình duyệt chưa đăng nhập GitHub, ngày 2026-11-02): repo, Project #1 và view "Bảng trạng thái" mở được; trang file báo cáo HTML mở được (GitHub báo file quá lớn để hiển thị, có nút tải về).

## 3. Cấu trúc repo

| File / thư mục | Nội dung |
|---|---|
| `README.md` | File này |
| `PREMISE.md` | Tiền đề: spec thêm, bỏ, sửa so với LAB-4; giả định bổ sung; hướng đã chốt |
| `task-breakdown.md` | Nguyên tắc chia task; bảng spec → issue; hạng mục 完納奨励金; chỗ hở của spec LAB-4 |
| `estimate.md` | Báo cáo HTML, issue mẫu đã duyệt, cách quy giờ, tổng theo epic, so với LAB-1 |
| `progress-report.md` | Báo cáo tiến độ Sprint 1 giả lập: trạng thái, burndown, rủi ro trễ |
| `AI-report.md` | Skill, prompt đã dùng cho từng việc (kể cả cách ghi SWP lên Project); cách review và 40 lỗi AI đã bắt; chỗ hiệu quả, chỗ cần cải thiện |
| `backlog/` | Dữ liệu gốc của backlog: 5 file `items-*.json` (792 mục, khuôn ở `backlog-item-format.md`), số issue GitHub (`issue-numbers.json`), SWP và giờ đã chốt (`story-points.json`, `estimated-hours.json`), quan hệ blocked by đã nối và phần vượt giới hạn GitHub, kết quả giả lập Sprint 1 |
| `estimate/` | `reports/`: báo cáo HTML của skill `tkm:sun-estimate` |
| `scripts/` | Script tạo issue, gắn link, kiểm dữ liệu, bổ sung phụ thuộc, quy giờ, ghi SWP và giờ lên Project, giả lập và ghi Sprint 1; mỗi script ghi cách chạy ở đầu file |
| `spec-summary/` | Tóm tắt tự viết thiết kế SCR-25 完納奨励金 (spec gốc ở repo private), trỏ từ `PREMISE.md` S-01 |
| `skills/` | Skill tự viết `lab5-review-backlog-output`: bộ câu hỏi soát B1..B9 và cổng kiểm máy `run-lab5-backlog-gate.py` dùng soát từng bước |

## 4. Spec → epic

| Spec (mã LAB-4 hoặc dòng PREMISE) | Epic trên Project | Ghi chú |
|---|---|---|
| Kiến trúc mục 8, ADR-002, ADR-018, C-17 | [#19](https://github.com/tamhtt-3564/fish-market-backlog/issues/19) E01 Hạ tầng và môi trường | Tài khoản dịch vụ do khách đứng tên (G-08) |
| `api-design/_index.md` (đợt migration 1..8, 10), DB design mục 6; PREMISE S-02, S-04, S-05, G-04, G-10 | [#20](https://github.com/tamhtt-3564/fish-market-backlog/issues/20) E02 Nền dữ liệu | Đợt 10 tách 10a, 10b (S-02) |
| SCR-01, 02, 07, 08; A1..A5, N-01, N-02; ADR-006, 014, 019; PREMISE S-07 | [#21](https://github.com/tamhtt-3564/fish-market-backlog/issues/21) E03 Đăng nhập, tài khoản, phân quyền | Cờ máy hiện trường lưu ở máy chủ (S-07) |
| SCR-03..06; A6..A9, A15, N-03, N-04, N-25; ADR-011 | [#22](https://github.com/tamhtt-3564/fish-market-backlog/issues/22) E04 Người tham gia và tư cách tham gia | SCR-06 chưa có spec (G-02) |
| SCR-09..12; A10..A14; PREMISE S-03, S-06, H-02 | [#23](https://github.com/tamhtt-3564/fish-market-backlog/issues/23) E05 Tiếp nhận lô và 目利き | Chuyển lô kẹt sau khoá ngày (S-03) |
| SCR-13..16; A16..A20, A33, A34, N-05; PREMISE H-06 | [#24](https://github.com/tamhtt-3564/fish-market-backlog/issues/24) E06 Giao dịch 相対 / せり | |
| SCR-17..19; A21..A25, A37, N-07 | [#25](https://github.com/tamhtt-3564/fish-market-backlog/issues/25) E07 Giao nhận | |
| SCR-23, 24; A29..A31, A35, A36, A45..A47, N-06, N-19 | [#26](https://github.com/tamhtt-3564/fish-market-backlog/issues/26) E08 Phiếu điều chỉnh và file đính kèm | |
| SCR-20, 21; A26..A28, A38..A40, N-08, N-09, N-24; ADR-009 | [#27](https://github.com/tamhtt-3564/fish-market-backlog/issues/27) E09 Đối soát, khoá ngày, mở lại sổ, chốt kỳ | |
| SCR-26, 27; A41..A44, N-13; ADR-012 | [#28](https://github.com/tamhtt-3564/fish-market-backlog/issues/28) E10 Version 業務規程 / 料率 | SCR-26 chưa có spec (G-02) |
| SCR-25 (`scr-25/`, 5 TECH); A48..A53, N-11, N-12; đợt migration 9; PREMISE S-01 | [#29](https://github.com/tamhtt-3564/fish-market-backlog/issues/29) E11 完納奨励金 | **Ràng buộc đặc thù của đề**: tách theo từng biến nghiệp vụ, 17 issue, 48 sub-issue (`task-breakdown.md` mục 3) |
| SCR-28..30; N-14, N-15; ADR-005, 007 | [#30](https://github.com/tamhtt-3564/fish-market-backlog/issues/30) E12 Báo cáo, in chứng từ, xuất kế toán | Phần 奨励金 của file kế toán (E12-S09) dùng dữ liệu E11 |
| SCR-31; N-16, N-17, N-23; ADR-004; PREMISE G-05 | [#31](https://github.com/tamhtt-3564/fish-market-backlog/issues/31) E13 Thông báo và việc nền | |
| SCR-34; N-20, N-21; ADR-003 | [#32](https://github.com/tamhtt-3564/fish-market-backlog/issues/32) E14 Mất mạng và đồng bộ | |
| SCR-32, 33; A32, N-18; ADR-008, 015; PREMISE H-03 | [#33](https://github.com/tamhtt-3564/fish-market-backlog/issues/33) E15 Audit, lưu trữ, xoá theo hạn | |
| SCR-22; N-10 | [#1](https://github.com/tamhtt-3564/fish-market-backlog/issues/1) E16 Tranh chấp | Epic tạo ở lần chạy thử script nên mang số #1 |
| ADR-017; C-16, C-19; N-22 | [#34](https://github.com/tamhtt-3564/fish-market-backlog/issues/34) E17 Chuyển đổi dữ liệu và vùng lịch sử | |
| Kiến trúc mục 8, NFR, ma trận quyền | [#35](https://github.com/tamhtt-3564/fish-market-backlog/issues/35) E18 Kiểm thử hệ thống và phi chức năng | |
| C-18, C-20; kiến trúc 8.1, 8.3 | [#36](https://github.com/tamhtt-3564/fish-market-backlog/issues/36) E19 Vận hành, đào tạo, hỗ trợ UAT, bàn giao | Trực 30 ngày sau go-live tính công ở `estimate.md`, không thành issue (G-20) |

Bảng chi tiết từng TECH, màn, đợt migration tới từng issue: `task-breakdown.md` mục 2.

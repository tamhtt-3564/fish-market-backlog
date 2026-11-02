# Khuôn dữ liệu backlog

Mỗi nhóm epic là một file `backlog/items-<nhóm>.json`, là một mảng JSON các mục theo khuôn dưới đây.
Script tạo issue đọc các file này để tạo issue, sub-issue, nhãn và trường trên Project. Đây là nguồn duy nhất của backlog; bảng ở `task-breakdown.md` sinh từ đây.

## Trường của một mục

| Trường | Bắt buộc | Giá trị |
|---|---|---|
| `key` | Có | Mã ổn định: epic `E11`; issue `E11-S03`; sub-issue `E11-S03-T02`. Số thứ tự hai chữ số |
| `type` | Có | `epic`, `story`, `devtask`, `uidesign`, `testdesign`, `testexecution`, `documentation`, `investigation`, `operation` (nhãn `type:*` của mẫu Project công ty) |
| `parent` | Trừ epic | `key` của mục cha |
| `title` | Có | Tiếng Việt, ngắn, bắt đầu bằng mã màn hoặc mã việc trong ngoặc vuông nếu có: `[SCR-25] Chạy tính 完納奨励金 của một tháng (A51)`; sub-issue thêm lớp ở cuối: `... : hàm DB` |
| `team` | Với `devtask` | `backend`, `frontend`, `infrastructure` |
| `owner` | Có, trừ epic | Một trong 11 vai: `PM-A`, `BrSE-A`, `BA-A`, `Design-A`, `TL-A`, `BE-A`, `BE-B`, `FE-A`, `FE-B`, `QA-A`, `Infra-A` |
| `labels_extra` | Không | `chờ khách`, `độ tin thấp` |
| `spec_refs` | Có, trừ epic | Mã nguồn trong bộ spec LAB-4: tên file TECH đầy đủ có đuôi `.md`, mã màn `SCR-xx`, API `A29`, `N-24` (đúng cách viết của spec), đợt migration `W1`..`W10`, `RC-xx`, `Q4-xx`, `C-xx`, `D4-xx`, `ADR-0xx`, mục DB design `DB 4.17`, hoặc mã PREMISE LAB-5 `G-xx`, `H-xx`. Không dẫn số dòng RFP |
| `overview` | Có | 1 tới 3 câu tự viết: làm gì, vì sao |
| `acceptance` | Có, trừ epic | Danh sách tiêu chí xong kiểm được, mỗi dòng một ý (nhánh, mã lỗi, audit, vai trò bị chặn...) |
| `roles_allowed`, `roles_blocked` | Với story có giao diện hoặc API | Mã vai trò hệ thống `ROLE-...` (11 vai trò ở ma trận quyền LAB-4) |
| `depends_on` | Không | Danh sách `key` phải xong trước |
| `customer_wait` | Khi có nhãn `chờ khách`; giữ lại làm lịch sử khi khách đã trả lời | Khách cần làm gì, hạn cần có |
| `affects`, `answer_due` | Issue làm rõ (`investigation`) | Mã issue chịu ảnh hưởng; hạn trả lời. Ghi bằng `scripts/record-clarification-follow-up.py` |
| `answer` | Issue làm rõ đã có trả lời | Câu trả lời của khách (ở bài này là câu trả lời giả lập của Sprint 1); khi có thì gỡ nhãn `chờ khách` |
| `rough_hours` | Có, trừ epic và story có sub-issue | Ước thô số giờ của **lá** (mục không có con), chỉ để kiểm luật 14 giờ; không phải estimate, không ghi lên Project |

## Luật

- Lá (mục không có con) tối đa 14 giờ. Story ước dưới 14 giờ thì không tách; lớn hơn thì tách sub-issue theo lớp (thiết kế giao diện, hàm DB và test, API, giao diện, ca kiểm thử, QA kiểm), lớp còn lớn thì tách theo nhánh nghiệp vụ ở TECH.
- Mọi story có giao diện mới hoặc đổi nhiều có sub-issue `uidesign`; mọi story có ghi dữ liệu có sub-issue `testdesign` và `testexecution` (owner `QA-A`).
- Repo nộp public: **không chép câu nào của tài liệu khách** (RFP) và không dán đoạn spec có câu trích; chữ Nhật chỉ dùng cho thuật ngữ và nhãn màn ngắn. Không tên người thật, không dữ liệu thật.
- Không dùng dấu gạch dài và dấu chấm giữa dòng.

---
name: lab5-review-backlog-output
description: "Soát đầu ra từng bước LAB-5 (Product A, chợ thủy sản: chia việc từ bộ spec LAB-4, GitHub Project, ước lượng SWP và giờ, báo cáo tiến độ sprint giả lập) ở repo nộp fish-market-backlog/: chạy cổng kiểm máy (đủ file theo bước, không chép câu RFP, không lộ khoá hay email, không dấu kiểu AI, 完納奨励金 có mặt) rồi soát theo bộ câu hỏi cố định: độ hạt task, 完納奨励金 tách theo biến nghiệp vụ, mọi phần spec có issue hoặc lý do, số đếm khớp Project, SWP và giờ quy nhất quán, báo cáo tiến độ không tô hồng. Trả kết luận Đạt / Đạt có điều kiện / Chưa đạt kèm lỗi, bằng chứng, cách sửa. Dùng ngay khi vừa xong một bước LAB-5, hoặc khi người dùng hỏi 'bước N ổn chưa', 'soát backlog', 'task chia đủ chưa', 'estimate đúng chưa', 'báo cáo tiến độ gửi khách được chưa', 'nộp LAB-5 được chưa', kể cả khi họ không nói chữ 'review'."
argument-hint: "[số bước 0-9] (bỏ trống = bước đang làm theo kế hoạch)"
---

# Soát đầu ra LAB-5

Người dùng là BA/PM, không chuyên kỹ thuật: họ cần biết **backlog này đội dev nhận làm được không, khách đọc báo cáo có tin được không, sai ở đâu, sửa thế nào**. Viết tiếng Việt, ngôn ngữ nghiệp vụ, giữ nguyên thuật ngữ Nhật. Skill **chỉ soát, không sửa** file được soát.

**Nguồn sự thật:** đề `docs/lab5/lab5-assignment-brief.md`; kế hoạch, quyết định D5-xx, nhật ký lỗi AI `docs/lab5/lab5-workplan-decisions-and-ai-error-log.md`; bộ spec LAB-4 `fish-market-app/specs/` (nhánh `lab4-specs`) và sổ D4-xx (việc chuyển LAB-5 ở D4-125, bảng C-xx); estimate LAB-1 `docs/lab1/step-07-estimate-wbs-and-risks.md`; dữ liệu thật trên GitHub Project (đọc bằng `gh project item-list`, `gh issue view`). Quyết định đã chốt thì không nêu lại, trừ khi áp sai phạm vi.

**Xong một bước** = cổng máy ĐẠT + 0 Nặng + 0 Vừa + người dùng duyệt. Lỗi Nhẹ sửa một lượt, không soát lại toàn bộ.

## 1. Cổng kiểm máy (luôn chạy đầu tiên)

```bash
python .claude/skills/lab5-review-backlog-output/scripts/run-lab5-backlog-gate.py <N>
```

Kiểm: đủ file Markdown bắt buộc ở gốc repo theo bước; không có dấu gạch dài và dấu chấm giữa dòng (luật người dùng); không chép câu RFP tiếng Nhật (chuỗi liền từ 12 ký tự trùng RFP sau chuẩn hoá NFKC); không lộ khoá GitHub, JWT, API, `service_role`, email; `PREMISE.md` một dòng thì đúng câu "Không thay đổi so với LAB-4"; `task-breakdown.md` nhắc 完納奨励金. **Cổng chỉ bắt mẫu chữ**: câu RFP bị cắt bởi dấu cách thành đoạn ngắn hơn 12 ký tự sẽ lọt; ý nghĩa và số đếm là việc của B1..B9.

## 2. Bộ câu hỏi cố định

| Mã | Câu hỏi | Chặn kiểu lỗi nào |
|---|---|---|
| B1 | **Độ hạt**: mỗi issue làm xong trong tối đa 2 ngày một người (theo quy tắc ở `task-breakdown.md`), có kết quả kiểm được? Issue lớn hơn đã tách sub-issue? Không có issue kiểu "Làm màn X" gộp FE + BE + DB + test? Mỗi issue có người phụ trách đúng vai (D5-14: BA viết spec, Design thiết kế giao diện, TL review, QA kiểm, BrSE làm rõ)? Issue có giao diện hoặc API ghi vai trò người dùng được làm và bị chặn, có ca kiểm thử cho vai bị chặn ở hàm DB hoặc API? Issue chờ khách có nhãn `chờ khách` và ghi khách cần làm gì, hạn nào? | Task quá lớn, mơ hồ (mục tiêu học tập số 1); việc không có người làm; chặn quyền chỉ ở giao diện (LAB-2 tái phạm 4 phase) |
| B2 | **完納奨励金 tách đúng**: là epic hoặc nhóm issue riêng, mỗi biến nghiệp vụ (điều kiện được thưởng, hạn thanh toán, cách tính, version 料率, chốt kỳ, xuất kế toán, dữ liệu kiểm thử biên) là issue riêng có tiêu chí xong; không lẫn vào issue thanh toán chung? Đối chiếu thiết kế SCR-25 (D4-142..D4-149): đủ 5 TECH ở `scr-25/technical-design/`, 6 API A48..A53, đợt migration 9, cảnh báo khoản trả trùng (D4-146), chuyển phần âm sang kỳ sau, hai version 料率 trong một kỳ; RC-11, RC-27, RC-38 đều có issue? Câu hỏi khách Q4-52..Q4-64 còn mở có issue làm rõ hoặc giả định ở PREMISE? | Gộp hạng mục đặc thù vào task lớn (yêu cầu riêng của đề) |
| B3 | **Phủ spec**: mỗi TECH, API, đợt migration, màn wireframe, việc chuyển LAB-5 (D4-125, C-xx) có issue, hoặc có dòng "chưa thành issue và vì sao"? Đếm hai chiều: spec → issue và issue → spec (issue không có nguồn spec là issue bịa)? | Bỏ sót phần spec; issue không truy được về thiết kế |
| B4 | **Khớp Project**: số issue, epic, sub-issue, SWP, giờ, trạng thái trong file khớp Project (ghi lệnh đếm)? Mỗi issue có đủ trường: Status, Target version (nếu vào sprint), Phụ trách (giả định), Story Point (SWP), Estimated time, nhãn `type:*` đúng tầng (D5-15)? | Bảng minh họa không khớp board thật; đếm tay sai (tái phạm LAB-4) |
| B5 | **SWP đúng ma trận**: Scope và Complexity mỗi issue ra đúng ô SWP của ma trận skill; issue mẫu người chốt khác skill thì có lý do cụ thể; trường Story Point trên Project là SWP **đã review**, không phải số skill chấm thô? | Chép số của AI không review; sai ô ma trận |
| B6 | **Quy giờ nhất quán**: một quy tắc ghi rõ (ví dụ giờ = SWP × hệ số, hoặc ước trực tiếp) và áp cho mọi issue; tính thử 3 issue bằng tay ra đúng số trên Project; tổng theo epic cộng lại bằng tổng chung; so LAB-1 cùng đơn vị (1 MD = 7 giờ, D-60)? | Quy đổi lẫn nhiều cách; tổng không cộng được |
| B7 | **PREMISE đúng phạm vi**: mỗi thay đổi so với LAB-4 có nguồn cụ thể (chỗ hở khi chia việc, góp ý soát, D4-125, câu hỏi khách Q4-xx); giả định chỉ lấp chỗ RFP / spec để ngỏ, không đè lên điều RFP nói rõ; mỗi giả định trỏ được issue chịu ảnh hưởng? | Lý do chung chung; giả định ghi đè RFP |
| B8 | **Báo cáo tiến độ không tô hồng**: số Done / In Progress / Todo khớp Project; burndown tính từ dữ liệu, chỗ lệch kế hoạch được nói thẳng; rủi ro trễ có issue, mốc bị ảnh hưởng, hành động, người và hạn; ghi rõ là sprint giả lập; câu chữ gửi khách được (không lộ chuyện nội bộ, không hứa vượt dữ liệu)? | Báo cáo AI tổng hợp tô hồng hoặc bỏ sót (câu neo P2-11, P2-13) |
| B9 | **Public an toàn**: không chép RFP, không tên người thật, không dữ liệu cá nhân, không khoá; Project và repo mở được ở cửa sổ ẩn danh? | Vi phạm luật mục 1 của đề |

## 3. Kiểm riêng theo bước

- **Bước 0, khung:** repo public, Project public có đủ trường theo D5-02; skill này có bản sao trong `skills/` của repo.
- **Bước 1, PREMISE:** đủ 3 phần theo thứ tự của đề; B7.
- **Bước 2, chia việc:** đủ 4 phần; B1, B2, B3; bảng chỗ hở chỉ dùng một trong 4 cách xử lý của đề.
- **Bước 3, tạo issue:** B4 (số issue, quan hệ epic → issue → sub-issue trên Project khớp bảng bước 2).
- **Bước 4, 5, estimate:** đủ 5 phần; báo cáo HTML của skill nằm trong repo, mở được; B5, B6.
- **Bước 6, tiến độ:** đủ 4 phần; B4, B8.
- **Bước 7, README:** đủ 5 phần; bảng cấu trúc repo khớp `ls` gốc repo; bảng spec → epic có số `#` thật; B4 cho mọi số đếm đi qua nhiều file.
- **Bước 8, AI-report:** đủ 3 phần của đề, gồm cách dùng Agent ghi SWP lên Project; mọi lỗi AI dẫn được dòng nhật ký; không nhận vượt bằng chứng.
- **Bước 9, nộp:** B9; mở thử link bằng cửa sổ ẩn danh.

## Mức lỗi

- `Nặng` → Chưa đạt: thiếu file / phần bắt buộc của đề; 完納奨励金 gộp vào task lớn; chép RFP hoặc lộ dữ liệu trong repo public; số trong báo cáo lệch Project.
- `Vừa`: issue quá lớn hoặc không có tiêu chí xong; phần spec không có issue cũng không có lý do; quy giờ không nhất quán; giả định không có nguồn.
- `Nhẹ`: định dạng, nhãn, mã dẫn; không đổi cách dev nhận việc hay cách khách đọc.
- **Góp ý**: câu chữ, cách trình bày.

Không có bằng chứng thì không ghi thành lỗi, đưa vào "Chờ người dùng quyết".

## Báo cáo

Lưu `docs/lab5/reviews/step-NN-review.md` (ngoài repo nộp; ghi đè, giữ lịch sử soát), cùng khuôn báo cáo của `lab4-review-spec-output`: đầu file (file soát, ngày, cổng, kết luận), bảng Phát hiện `| # | Mức | Câu hỏi (B1..B9 / Cổng) | Vị trí | Vấn đề | Bằng chứng | Cách sửa |`, Góp ý, Chờ người dùng quyết, Lịch sử soát.

## Sau khi soát

- Lỗi do AI sinh sai → thêm dòng vào "Nhật ký lỗi AI" của LAB-5 (cùng kiểu đã có ở LAB-1..4 thì ghi "tái phạm").
- Hỏi người dùng có sửa theo danh sách không; sửa xong chạy lại cổng.
- Giao cho agent phụ soát: "Chạy skill `lab5-review-backlog-output` cho bước N theo đúng SKILL.md; chỉ ghi vào docs/lab5/reviews/; không sửa file nộp, không sửa Project, không ghi nhật ký; trả dòng đề xuất".

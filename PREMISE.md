# PREMISE: backlog LAB-5 khác bộ spec LAB-4 ở đâu

Bản LAB-4 làm đầu vào: nhánh `lab4-specs` của repo `tamhtt-3564/fish-market-prototype`, commit `21bbe4b` (2026-11-01).
Bản nộp LAB-4 là commit `418d444` (2026-10-30); hai commit sau đó thêm thiết kế SCR-25 (dòng S-01 dưới đây).
Repo spec LAB-4 để private (spec có câu trích tài liệu khách); người chấm cần được mời vào repo đó. File này chỉ dẫn mã:
SCR-xx (màn), TECH (detail design), A-xx (API), D4-xx (quyết định LAB-4), Q4-xx (câu hỏi khách), RC-xx (ràng buộc đặc thù).

Số `#` của issue điền ở bước tạo issue lên Project; trước đó cột "Issue bị ảnh hưởng" ghi tên epic.

## 1. Spec thêm, bỏ, sửa so với LAB-4

| Mã | Spec (mã / file) | Thêm / Bỏ / Sửa | Trước → sau | Vì sao | Issue bị ảnh hưởng |
|---|---|---|---|---|---|
| S-01 | SCR-25 完納奨励金計算: `scr-25/` (SPEC, QA, wireframe, 5 TECH), API A48..A53, đợt migration 9, DB design 4.17 và các bảng 奨励金 | Thêm | Bản nộp `418d444`: SCR-25 ngoài phạm vi spec đủ (D4-03), chỉ có bảng dữ liệu và một dòng ở danh sách màn → bản `21bbe4b`: spec đủ như 10 màn cốt lõi (D4-142..D4-149) | Đề LAB-5 bắt tách 完納奨励金 thành task riêng theo từng biến nghiệp vụ. Bản nộp không có quy tắc tính, trạng thái, lỗi, nên không chia được task cụ thể, chỉ ra được một task lớn "làm phần 奨励金" mà đề cấm | Epic 完納奨励金 (toàn bộ); epic Nền dữ liệu (đợt 9) |

Chỗ hở phát hiện khi chia việc ở bước 2 sẽ thêm dòng vào bảng này (mã S-02 trở đi) hoặc vào mục 2, kèm nguồn cụ thể.

## 2. Giả định bổ sung

Các giả định của LAB-4 (mặc định của 64 câu Q4 và các câu No của LAB-1) giữ nguyên, không chép lại. Bảng dưới chỉ ghi giả định **mới của LAB-5**, dùng để chia việc và ước lượng.

| Mã | Giả định | Chỗ spec / RFP để ngỏ | Ảnh hưởng tới issue / estimate |
|---|---|---|---|
| G-01 | Chia việc theo mặc định LAB-4 của mọi câu khách chưa trả lời. 15 câu mà phương án khác làm đổi nhiều khối lượng có issue làm rõ riêng (danh sách G-01a), hạn trả lời trước sprint chạm phần đó | 64 câu Q4 chưa có trả lời (PREMISE LAB-4 mục 5.1) | 15 issue làm rõ; câu nào khách trả lời khác mặc định thì ước lại các issue liên quan và ghi vào `progress-report.md` mục rủi ro (D5-13) |
| G-02 | 9 màn chưa có spec (SCR-06, 22, 26, 28, 29, 30, 31, 33, 34) ước theo màn tương tự đã có spec; mỗi màn có thêm một issue viết spec; SWP chấm lại khi spec xong | LAB-4 chỉ có một dòng ở danh sách màn, ghi rõ cần spec riêng trước khi chia task (PREMISE LAB-4 mục 7) | 9 issue viết spec; các issue xây dựng của 9 màn gắn nhãn độ tin thấp, cộng riêng ở `estimate.md` (D5-12) |
| G-03 | 14 màn chỉ có wireframe (SCR-01, 02, 03, 04, 07, 08, 10, 11, 15, 16, 17, 19, 20, 32) chia việc theo wireframe, danh sách API (mã N-xx) và DB design; người làm viết thiết kế ngắn trong issue trước khi code (thuộc định nghĩa xong) | Không có screen spec và TECH cho 14 màn này (D4-03) | Issue có thêm bước thiết kế ngắn; độ tin ước lượng trung bình |
| G-04 | Bảng và cột chưa xếp đợt migration (`report_runs`, `retention_deletion_requests`, `disputes`, cột mới của `user_profiles`) gom thành **đợt 10**, chạy sau đợt 9 | LAB-4 xếp 9 đợt, phần này ghi "ngoài 9 đợt, chưa có TECH" (`api-design/_index.md`) | Thêm issue migration đợt 10; issue của SCR-22, SCR-33, báo cáo ngày phụ thuộc đợt 10 |
| G-05 | Việc nền chưa có TECH (gửi thông báo ngay, báo cáo ngày chạy lại khi treo hoặc lỗi, tạo lại file kế toán lỗi, xử lý biên nhận đồng bộ): mỗi việc một issue gồm thiết kế ngắn và xây dựng | LAB-4 chuyển sang LAB-5 (D4-125 (1), C-15) | Thêm issue ở epic Việc nền và tích hợp |
| G-06 | Các việc LAB-4 chuyển sang LAB-5 không có chức năng ghi: chuyển đổi dữ liệu (C-16), cấu hình nền tảng (C-17), runbook và bàn giao (C-18, C-20), vùng tra cứu lịch sử `legacy` (C-19), hàng rào đọc cho tài khoản bên ngoài (PKT-11, C-12) thành issue theo hướng đã ghi ở LAB-4, không thiết kế lại | D4-125 (2), (3) cho C-12, C-16, C-17, C-19; C-18, C-20 ghi thẳng "bước nhận LAB-5" ở bảng C-xx của LAB-4 | Thêm issue ở các epic Chuyển đổi, Hạ tầng và vận hành, Bảo mật |
| G-07 | Đội làm trên mã prototype LAB-2 (nâng cấp, không viết lại), đã quen nền Next.js, Supabase, Vercel; chỗ prototype khác thiết kế (PREMISE LAB-4 mục 6) là issue sửa mã | D4-12 chỉ nói nâng cấp nền LAB-2, không nói đội có quen nền hay không | Ước lượng không cộng thời gian học nền; issue sửa prototype tách khỏi issue làm mới |
| G-08 | Tài khoản dịch vụ (Vercel, Supabase, gửi mail, kho đối tượng) do khách đứng tên có trước Sprint 1 | Q4-19 chưa có trả lời | Không có thì issue hạ tầng của Sprint 1 bị chặn; ghi thành rủi ro trễ |
| G-09 | Một ngày công 7 giờ, như LAB-1 (D-60) | Đề không nêu cách quy giờ | Dùng khi quy SWP ra giờ và so với LAB-1 ở `estimate.md` |

**G-01a. 15 câu có issue làm rõ** (đổi nhiều khối lượng nếu khách chọn khác mặc định):

| Câu | Nội dung (tóm tắt) | Đổi gì nếu khác mặc định |
|---|---|---|
| Q4-02 | Luồng và hạn xử lý tranh chấp | Spec và luồng của SCR-22 |
| Q4-10 | Yêu cầu xoá dữ liệu cá nhân khi phải lưu 7 năm | Thêm cơ chế ẩn danh hoá trong hạn lưu |
| Q4-17 | Định dạng file kế toán, đẩy tự động | Đẩy tự động (SFTP, API) là hạng mục thêm |
| Q4-24 | Định dạng file xuất của hệ thống cũ | Khối lượng script chuyển đổi |
| Q4-25 (kèm Q4-19) | Chấp nhận rủi ro sao lưu trong một vùng | Hạng mục A hoặc B (thay cả nền) |
| Q4-27 | Vai trò riêng cho người duyệt quy tắc | Thêm vai trò thứ 12, sửa ma trận quyền |
| Q4-28 | Màn quản lý danh mục 荷目 | Thêm một màn |
| Q4-44 | Lô còn hàng kẹt sau khoá ngày | Phương án (b) đổi ADR-009 và cách mở lại sổ |
| Q4-46 | Lịch chợ, ngày nghỉ chợ | Thêm màn quản lý lịch, đổi cảnh báo khoá ngày |
| Q4-55 | Nghĩa của "trả đủ" khi tính 奨励金 | Quy tắc điều kiện được thưởng |
| Q4-58 | Kỳ có hai version 料率 | Cách so ngưỡng trong tính 奨励金 |
| Q4-59 | Trả quá hạn: bỏ một giao dịch hay cả kỳ | Quy tắc tính 奨励金 |
| Q4-60 | Tổng kỳ âm | Chuyển phần âm, có thu lại tiền hay không |
| Q4-63 | Thứ tự so ngưỡng, nhân thuế, làm tròn | Công thức và dữ liệu kiểm thử |
| Q4-64 | Huỷ khoản trả ghi nhầm | Thêm thao tác huỷ có người duyệt |

## 3. Hướng đã chốt

| Mã | Vấn đề | Các phương án ở LAB-4 | Phương án chốt | Vì sao |
|---|---|---|---|---|
| H-01 | 9 màn chưa có spec | LAB-4 chỉ ghi "cần spec riêng trước khi chia task", chưa chọn cách: (a) viết spec rút gọn ngay ở LAB-5; (b) issue viết spec trong dự án, issue xây dựng ước theo màn tương tự; (c) mỗi màn một issue lớn | (b) | (a) thêm nhiều việc và lượt soát ngoài phạm vi đề; (c) trái yêu cầu "không để task quá lớn, mơ hồ"; (b) vẫn chia nhỏ được, độ tin thấp được ghi rõ (D5-12) |
| H-02 | Lô còn hàng kẹt sau khoá ngày (Q4-44, C-24) | (a) chuyển sang lô mới của ngày kế tiếp bằng bút toán chuyển; (b) mở lại sổ rồi sửa; (c) xử lý ngoài hệ thống, lô cũ về 0 bằng bút toán điều chỉnh | (a), làm hàm `transfer_stranded_lot` theo tên đề xuất ở TECH khoá ngày của SCR-21; issue làm rõ Q4-44 song song | LAB-4 để bảng và hàm chốt ở LAB-5 (D4-125 (6)); (a) là mặc định LAB-4, không phải đổi ADR-009 như (b); hàng vẫn bán tiếp được trên hệ thống, còn (c) đưa hàng ra ngoài hệ thống |
| H-03 | Yêu cầu xoá dữ liệu cá nhân khi audit phải lưu 7 năm (Q4-10, C-12) | Q4-10 hỏi khách hai cách: ẩn danh hoá sau hạn lưu, hoặc từ chối xoá vì nghĩa vụ lưu; mặc định LAB-4 gộp cả hai | Từ chối trong hạn lưu, ẩn danh hoá sau 7 năm, ghi yêu cầu vào audit; issue làm rõ Q4-10 | LAB-4 chuyển sang LAB-5 cùng Q4-10 (D4-125 (3)) vì không màn cốt lõi nào ghi dữ liệu này; theo mặc định LAB-4 để không thêm cơ chế ẩn danh hoá trong hạn |
| H-04 | Huỷ khoản trả ghi nhầm (Q4-64) | Bản đầu chưa có thao tác huỷ; hoặc thêm dòng đảo có lý do, người khác duyệt | Bản đầu chưa có; không có issue xây dựng, chỉ issue làm rõ | Mặc định LAB-4 `[Suy luận]`; thêm khi khách xác nhận cần, ước lại lúc đó |
| H-05 | Thứ tự đợt migration của phần ngoài 9 đợt | LAB-4 chưa xếp | Đợt 10 sau đợt 9 (G-04) | Không hàm nào của 9 đợt đọc các bảng này (`api-design/_index.md`), xếp sau không chặn đợt nào |

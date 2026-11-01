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
| S-02 | Bảng "Thứ tự đợt migration" và phần "ngoài 9 đợt" ở `api-design/_index.md`; H-05 bản đầu | Sửa | Đợt 10 một khối chạy sau đợt 9 → tách **10a** (cột mới của `user_profiles`, chạy ngay sau đợt 1) và **10b** (`report_runs`, `retention_deletion_requests`, `disputes` và phần ở S-04, chạy sau đợt 7) | Khi chia việc thấy hai chỗ sai thứ tự: hàm cảnh báo khoá ngày của đợt 7 có vế Critical 11:00 đọc `report_runs` (TECH khoá ngày của SCR-21), nên câu "không hàm nào của 9 đợt đọc các bảng này" không đúng; đăng nhập, khoá tạm, tài khoản migration cần cột mới của `user_profiles` từ đầu (D5-16) | E02-S09, E02-S10, E09-S03-T02, E03-S01, E03-S02, E03-S07, E17-S03 |
| S-03 | TECH khoá ngày SCR-21 mục 5 (d), H-02 | Thêm | Hàm `transfer_stranded_lot` chỉ có tên → thêm cột trỏ lô cũ và lô mới, một migration riêng sau đợt 7; vị trí nút và API chốt ở thiết kế ngắn | LAB-4 để bảng và hàm chốt ở LAB-5 (D4-125 (6)); khi chia thấy chưa có chỗ lưu quan hệ hai lô | E05-S05 |
| S-04 | DB design, `api-design/_index.md` đợt 10, `log-convention.md` | Thêm | Đợt 10b thêm: vá hàm đặt lại dữ liệu demo (bảng `disputes` có khoá ngoại tới `trades`, cùng lỗi như đợt 9); chỗ lưu trạng thái công bố đối soát (N-24); bảng cấu hình thông báo (N-17); cột trỏ bản ghi mới khi biên nhận đồng bộ được nhập lại (N-20); loại audit cho tạo tài khoản (N-01) và yêu cầu xoá dữ liệu cá nhân (H-03) | N-24, N-17 có API mà chưa có chỗ lưu; DB design không có loại audit tương ứng; phát hiện khi chia E09, E13, E14, E03, E15 | E02-S09-T01, E02-S09-T04, E09-S08-T02, E13-S05, E14-S04-T02, E03-S07-T02 |
| S-05 | DB design 6.2 (`trades.unit_price_jpy`) | Sửa | Ràng buộc đơn giá tối thiểu 1 JPY không nằm ở đợt nào → xếp vào đợt 4a, kiểm dữ liệu cũ trước khi gắn | Đối chiếu DB design mục 6 với bảng đợt khi chia E02 | E02-S04-T01 |
| S-06 | TECH tiếp nhận lô SCR-09 mục 5 | Sửa | Câu ghi chú nói `api-conventions.md` cho bỏ trống mã chống ghi trùng khi ghi trực tuyến → xoá câu ghi chú; `api-conventions.md` mục 10 đã bắt gửi ở mọi lần ghi, giữ nguyên | Khi chia E05 đọc ghi chú cũ, đối chiếu thì `api-conventions.md` bản `21bbe4b` đã đúng (soát độc lập bước 2, N3) | E05-S01, E19-S08 |
| S-07 | C-17, ADR-006, DB design (bảng thiết bị) | Thêm | Cờ "máy hiện trường" chưa có chỗ lưu → bảng thiết bị dùng chung ở máy chủ: ROLE-SYS-ADMIN cấp mã thiết bị (cookie chỉ máy chủ đọc), máy chủ kiểm mã để áp hết phiên 30 phút; API mới N-26 (cấp, thu hồi mã thiết bị, chỉ ROLE-SYS-ADMIN), loại audit cấp và thu hồi thiết bị; thêm vào đợt 10a | Lưu cờ ở trình duyệt thì người dùng tự gỡ được, quyền chỉ chặn ở giao diện, trái nguyên tắc chặn ở máy chủ (soát độc lập bước 2, V6) | E03-S04, E02-S10, E02-S10-T01 |

Việc sửa chữ trong bộ spec LAB-4 theo các dòng trên là issue E19-S08.

## 2. Giả định bổ sung

Các giả định của LAB-4 (mặc định của 64 câu Q4 và các câu No của LAB-1) giữ nguyên, không chép lại. Bảng dưới chỉ ghi giả định **mới của LAB-5**, dùng để chia việc và ước lượng.

| Mã | Giả định | Chỗ spec / RFP để ngỏ | Ảnh hưởng tới issue / estimate |
|---|---|---|---|
| G-01 | Chia việc theo mặc định LAB-4 của mọi câu khách chưa trả lời. 18 câu mà phương án khác làm đổi nhiều khối lượng có issue làm rõ riêng (danh sách G-01a), hạn trả lời trước sprint chạm phần đó | 64 câu Q4 chưa có trả lời (PREMISE LAB-4 mục 5.1) | 18 issue làm rõ; câu nào khách trả lời khác mặc định thì ước lại các issue liên quan và ghi vào `progress-report.md` mục rủi ro (D5-13) |
| G-02 | 9 màn chưa có spec (SCR-06, 22, 26, 28, 29, 30, 31, 33, 34) ước theo màn tương tự đã có spec; mỗi màn có thêm một issue viết spec; mỗi story có thêm sub thiết kế kỹ thuật ngắn của TL-A (story có ghi: thứ tự kiểm, khoá, mã lỗi, audit; story chỉ đọc: nguồn dữ liệu, bộ lọc, quyền xem); SWP chấm lại khi spec xong | LAB-4 chỉ có một dòng ở danh sách màn, ghi rõ cần spec riêng trước khi chia task (PREMISE LAB-4 mục 7) | 9 issue viết spec; các issue xây dựng của 9 màn gắn nhãn độ tin thấp, cộng riêng ở `estimate.md` (D5-12) |
| G-03 | 14 màn chỉ có wireframe (SCR-01, 02, 03, 04, 07, 08, 10, 11, 15, 16, 17, 19, 20, 32) chia việc theo wireframe, danh sách API (mã N-xx) và DB design; TL-A viết thiết kế kỹ thuật ngắn (sub `documentation`, 2 tới 4 giờ) cho mỗi story trước khi code | Không có screen spec và TECH cho 14 màn này (D4-03) | Issue có thêm bước thiết kế ngắn; độ tin ước lượng trung bình |
| G-04 | Bảng và cột chưa xếp đợt migration (`report_runs`, `retention_deletion_requests`, `disputes`, cột mới của `user_profiles`) gom thành **đợt 10**, tách 10a và 10b theo S-02 | LAB-4 xếp 9 đợt, phần này ghi "ngoài 9 đợt, chưa có TECH" (`api-design/_index.md`) | Issue migration E02-S10 (10a), E02-S09 (10b); đăng nhập, tài khoản phụ thuộc 10a; SCR-22, SCR-33, báo cáo ngày phụ thuộc 10b |
| G-05 | Việc nền chưa có TECH (gửi thông báo ngay, báo cáo ngày chạy lại khi treo hoặc lỗi, tạo lại file kế toán lỗi, xử lý biên nhận đồng bộ): mỗi việc một issue gồm thiết kế ngắn và xây dựng | LAB-4 chuyển sang LAB-5 (D4-125 (1), C-15) | Thêm issue ở epic Việc nền và tích hợp |
| G-06 | Các việc LAB-4 chuyển sang LAB-5 không có chức năng ghi: chuyển đổi dữ liệu (C-16), cấu hình nền tảng (C-17), runbook và bàn giao (C-18, C-20), vùng tra cứu lịch sử `legacy` (C-19), hàng rào đọc cho tài khoản bên ngoài (PKT-11, C-12) thành issue theo hướng đã ghi ở LAB-4, không thiết kế lại | D4-125 (2), (3) cho C-12, C-16, C-17, C-19; C-18, C-20 ghi thẳng "bước nhận LAB-5" ở bảng C-xx của LAB-4 | Thêm issue ở các epic Chuyển đổi, Hạ tầng và vận hành, Bảo mật |
| G-07 | Đội làm trên mã prototype LAB-2 (nâng cấp, không viết lại), đã quen nền Next.js, Supabase, Vercel; chỗ prototype khác thiết kế (PREMISE LAB-4 mục 6) là issue sửa mã | D4-12 chỉ nói nâng cấp nền LAB-2, không nói đội có quen nền hay không | Ước lượng không cộng thời gian học nền; issue sửa prototype tách khỏi issue làm mới |
| G-08 | Tài khoản dịch vụ (Vercel, Supabase, gửi mail, kho đối tượng) do khách đứng tên có trước Sprint 1 | Q4-19 chưa có trả lời | Không có thì issue hạ tầng của Sprint 1 bị chặn; ghi thành rủi ro trễ |
| G-09 | Một ngày công 7 giờ, như LAB-1 (D-60) | Đề không nêu cách quy giờ | Dùng khi quy SWP ra giờ và so với LAB-1 ở `estimate.md` |
| G-10 | 5 hàm nền dùng chung không có TECH (khoá theo tháng, kiểm kỳ đã chốt, tra version theo ngày, đóng biên nhận đồng bộ, số lần giao tối đa) do E02 làm trong đợt 1 và 5; epic khác chỉ gọi | Bảng đợt migration ghi tên hàm, không ghi ai viết | E02-S01-T03, E02-S05-T01 |
| G-11 | Thân hàm có TECH (kể cả hàm ghi tên ở đợt 2, 4 như cập nhật hiệu lực tham gia, tra bên mua) làm ở story của màn; E02 chỉ làm bảng, cột, backfill, vá hàm cũ | Bảng đợt ghi cả hàm, không tách phần | E04-S03, E04-S04, các story có TECH |
| G-12 | (thay bằng S-07: cờ máy hiện trường lưu ở máy chủ) | | |
| G-13 | Thông báo cho người tham gia bên ngoài do hàm cập nhật hiệu lực và việc nền nhắc hạn trả sinh ra | Q4-31 nêu loại sự kiện, không nêu nơi sinh | E04-S08; chốt ở spec SCR-06 (E04-S05) |
| G-14 | In chứng từ (không có API) chặn quyền ở trang và lớp đọc máy chủ | ADR-007 in qua trình duyệt | E12-S07 |
| G-15 | Tra cứu vùng lịch sử `legacy` chỉ ROLE-SETTLEMENT | N-22 ghi ROLE-SETTLEMENT, ADR-017 ghi chung "vai trò văn phòng" | E17-S05 |
| G-16 | Thử tải dùng một dự án tạm trong tổ chức Supabase của khách, xoá sau khi đo; phí thêm vào danh sách chờ Q4-19 | Hồ sơ tải có ở kiến trúc, môi trường thử tải chưa có | E18-S02; rủi ro chi phí |
| G-17 | Lịch ngày chợ 6 ngày mỗi tuần (LAB-1 No 13) dùng cho đo uptime và cảnh báo tới khi có trả lời Q4-46 | Q4-46 chưa trả lời | E01-S05, E09-S10 |
| G-18 | Bản chụp đối soát lúc khoá ngày cộng cả dòng đảo và dòng mới của phiếu sửa; dòng mới lưu số mới, không lưu phần chênh | TECH khoá ngày còn ghi nghĩa dòng mới để mở, TECH duyệt phiếu đã chốt | E09-S02-T01 |
| G-19 | Phần dùng chung của ghi tạm khi mất mạng (hàng đợi trên máy, mã băm nội dung, biên nhận) thuộc E14; lá ghi tạm của lô, giao nhận phụ thuộc E14-S01 | ADR-003 không nói phần dùng chung thuộc màn nào | E14-S01, E05-S01-T05, E07-S02-T07, E07-S05-T05 |
| G-20 | 30 ngày hỗ trợ vận hành sau go-live không thành issue, tính công ở `estimate.md` như PM; backlog chỉ có issue lập lịch trực và sổ sự cố | Trực theo ca không chia được thành việc tối đa 2 ngày (D5-16) | E19-S07; `estimate.md` |
| G-21 | Không có thông báo riêng cho người duyệt khi version quy tắc chờ duyệt; người duyệt xem danh sách SCR-26 lọc trạng thái chờ duyệt | SCR-27 không nói | E10-S02 |
| G-22 | Bỏ hằng số cũ trong mã prototype (số lần giao tối đa, số ngày cảnh báo hết hạn) là việc của epic dùng hằng số đó; đọc tham số từ version quy tắc | ADR-012 chuyển tham số vào version, spec không nói ai sửa mã cũ | E07-S07, E04-S09 |
| G-23 | Việc nền cảnh báo biên nhận đồng bộ treo quá 1 ngày, 3 ngày thuộc E09 (thiết kế nằm ở TECH chốt kỳ SCR-21) | TECH chốt kỳ mục 4.7 thiết kế, không nói thuộc màn nào | E09-S12 |
| G-24 | Các câu "sửa DB design, sửa bảng mã lỗi" ở mục 5 của TECH và các dòng S-xx được sửa vào bộ spec bằng một issue tài liệu | Spec LAB-4 ghi việc sửa tài liệu, không có chủ | E19-S08 |
| G-25 | Bảng đổi mã lỗi sang mã HTTP trong mã ứng dụng do người làm route duyệt phiếu sửa cập nhật một lần cho mọi mã mới | `error-codes.md` 6.6 không giao epic | E08-S06-T05 |

**G-01a. 18 câu có issue làm rõ** (đổi nhiều khối lượng nếu khách chọn khác mặc định):

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
| Q4-56 | Mẫu file CSV khoản trả, dòng lỗi | Kiểm và báo lỗi của phần nạp CSV (thêm theo D5-16) |
| Q4-57 | Kỳ nhận chênh lệch sau xác nhận | Kỳ đích của chênh lệch (thêm theo D5-18) |
| Q4-60 | Tổng kỳ âm | Chuyển phần âm, có thu lại tiền hay không |
| Q4-61 | Hạn trả đếm ngày lịch hay ngày làm việc | Cách tính hạn trả của 奨励金 (thêm theo D5-18) |
| Q4-63 | Thứ tự so ngưỡng, nhân thuế, làm tròn | Công thức và dữ liệu kiểm thử |
| Q4-64 | Huỷ khoản trả ghi nhầm | Thêm thao tác huỷ có người duyệt |

## 3. Hướng đã chốt

| Mã | Vấn đề | Các phương án ở LAB-4 | Phương án chốt | Vì sao |
|---|---|---|---|---|
| H-01 | 9 màn chưa có spec | LAB-4 chỉ ghi "cần spec riêng trước khi chia task", chưa chọn cách: (a) viết spec rút gọn ngay ở LAB-5; (b) issue viết spec trong dự án, issue xây dựng ước theo màn tương tự; (c) mỗi màn một issue lớn | (b) | (a) thêm nhiều việc và lượt soát ngoài phạm vi đề; (c) trái yêu cầu "không để task quá lớn, mơ hồ"; (b) vẫn chia nhỏ được, độ tin thấp được ghi rõ (D5-12) |
| H-02 | Lô còn hàng kẹt sau khoá ngày (Q4-44, C-24) | (a) chuyển sang lô mới của ngày kế tiếp bằng bút toán chuyển; (b) mở lại sổ rồi sửa; (c) xử lý ngoài hệ thống, lô cũ về 0 bằng bút toán điều chỉnh | (a), làm hàm `transfer_stranded_lot` theo tên đề xuất ở TECH khoá ngày của SCR-21; issue làm rõ Q4-44 song song | LAB-4 để bảng và hàm chốt ở LAB-5 (D4-125 (6)); (a) là mặc định LAB-4, không phải đổi ADR-009 như (b); hàng vẫn bán tiếp được trên hệ thống, còn (c) đưa hàng ra ngoài hệ thống |
| H-03 | Yêu cầu xoá dữ liệu cá nhân khi audit phải lưu 7 năm (Q4-10, C-12) | Q4-10 hỏi khách hai cách: ẩn danh hoá sau hạn lưu, hoặc từ chối xoá vì nghĩa vụ lưu; mặc định LAB-4 gộp cả hai | Từ chối trong hạn lưu, ẩn danh hoá sau 7 năm, ghi yêu cầu vào audit; issue làm rõ Q4-10 | LAB-4 chuyển sang LAB-5 cùng Q4-10 (D4-125 (3)) vì không màn cốt lõi nào ghi dữ liệu này; theo mặc định LAB-4 để không thêm cơ chế ẩn danh hoá trong hạn |
| H-04 | Huỷ khoản trả ghi nhầm (Q4-64) | Bản đầu chưa có thao tác huỷ; hoặc thêm dòng đảo có lý do, người khác duyệt | Bản đầu chưa có; không có issue xây dựng, chỉ issue làm rõ | Mặc định LAB-4 `[Suy luận]`; thêm khi khách xác nhận cần, ước lại lúc đó |
| H-05 | Thứ tự đợt migration của phần ngoài 9 đợt | LAB-4 chưa xếp; bản đầu PREMISE LAB-5 xếp một đợt 10 sau đợt 9 | Tách 10a sau đợt 1, 10b sau đợt 7 (S-02) | Bản đầu dựa vào câu "không hàm nào của 9 đợt đọc các bảng này" của LAB-4, câu này sai (S-02); người dùng chọn tách (D5-16) |
| H-06 | Hai hàm nộp và từ chối giao dịch (`submit_trade`, `reject_trade`) có trong danh sách hàm, nhưng hàm chốt giao dịch làm liền nộp và duyệt nên trạng thái 確認待ち không được lưu | LAB-4 ghi cả hai hàm, chưa chốt chữ ký | Việc TL-A chốt có cần hai hàm không (E06-S08, khoảng 3 giờ); cần thì tạo story xây dựng và ước lúc đó, không cần thì sửa N-05 qua E19-S08 | Bỏ ngay là quyết thay phần thiết kế đã duyệt; giữ issue thì chi phí nhỏ (D5-16) |

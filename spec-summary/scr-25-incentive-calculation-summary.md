# Tóm tắt thiết kế SCR-25 完納奨励金 (tự viết, cho người không mở được repo spec)

Bộ spec LAB-4 nằm ở repo private `fish-market-prototype` (nhánh `lab4-specs`, thư mục `specs/scr-25/`, commit `21bbe4b`) vì có câu trích RFP. File này tóm tắt bằng lời của tác giả các điểm backlog E11 dựa vào; không chép câu RFP. Mã RC-xx là ràng buộc RFP, Q4-xx là câu hỏi khách, D4-xx là quyết định LAB-4.

## 1. Màn làm gì, ai dùng

| Việc | Ai làm | API |
|---|---|---|
| Xem kết quả 完納奨励金 của một tháng, khoản trả, chênh lệch | ROLE-SETTLEMENT, ROLE-AUDIT-VIEW (chỉ xem) | A48 |
| Ghi ngày và số tiền bên mua đã trả cho từng giao dịch, nhập tay | ROLE-SETTLEMENT | A49 |
| Nạp CSV khoản trả; một dòng lỗi thì không nạp cả file | ROLE-SETTLEMENT | A50 |
| Chạy tính 完納奨励金 của một tháng (tính lại được nhiều lần) | ROLE-SETTLEMENT | A51 |
| Xác nhận kết quả của tháng | ROLE-SETTLEMENT | A52 |
| Tính chênh lệch khi có thay đổi sau khi đã xác nhận | ROLE-SETTLEMENT | A53 |

9 vai trò còn lại không vào được màn; chặn ở trang, API và hàm DB, không chỉ ẩn ở giao diện. Cả hai vai trò được dùng đều phải đăng nhập MFA.

## 2. Quy tắc tính (RC-27)

1. Giao dịch đã xác nhận trong tháng mới được xét. Mỗi giao dịch có hạn trả = ngày nghiệp vụ cộng số ngày theo version 業務規程, đếm ngày lịch giờ Nhật; trả đúng ngày hạn vẫn là trong hạn.
2. Giao dịch được tính khi tổng tiền trả trong hạn đủ số phải trả (có thuế). Quá hạn hoặc thiếu tiền thì giao dịch đó không tính; không có ân hạn. Một giao dịch quá hạn chỉ làm giao dịch đó bằng 0, không làm cả kỳ bằng 0 (cách đọc này chờ khách, Q4-59).
3. Cộng tiền trước thuế của các giao dịch được tính theo người tham gia và version 料率. So với ngưỡng của loại người tham gia: bằng hoặc vượt ngưỡng thì có thưởng.
4. Thưởng = tổng trước thuế × tỷ lệ × hệ số thuế 110/100, cắt phần lẻ yên một lần ở bước cuối. Thứ tự phép tính này quyết định kết quả nên chỉ có một hàm DB chứa công thức (thứ tự chờ khách xác nhận, Q4-63).
5. Tháng có hai version 料率 thì mỗi version so ngưỡng riêng (giả định, chờ khách ở Q4-58).

## 3. Trạng thái của kỳ (RC-38, RC-27)

- Chỉ tính được sau khi kỳ đã chốt (SCR-21). Trước hạn trả cuối của tháng, kết quả là tính tạm; qua hạn trả cuối mới xác nhận được.
- Xác nhận theo thứ tự tháng. Kết quả đã xác nhận không bị sửa.
- Thay đổi sau khi xác nhận (phiếu sửa, khoản trả ghi muộn) sinh dòng chênh lệch ghi vào kỳ chưa xác nhận sớm nhất, có nguyên nhân rõ (Q4-57 hỏi khách kỳ đích).
- Số phải trả của người tham gia âm sau khi nhận chênh lệch thì phần âm chuyển sang kỳ sau, không thu lại tiền đã trả (giả định, Q4-60).
- Tháng không có giao dịch thì không cần xác nhận; tháng chỉ có chênh lệch nhận vào vẫn tính như tháng thường.
- Ghi trùng khoản trả (cùng giao dịch, ngày, số tiền) thì cảnh báo, người dùng xác nhận mới ghi (D4-146, Q4-62).

## 4. Dữ liệu và thiết kế

- Đợt migration 9: 3 bảng mới (khoản trả, kết quả theo kỳ, chênh lệch), ràng buộc, chỉ mục, quyền đọc theo dòng, trigger chặn sửa kết quả đã xác nhận.
- 5 TECH: ghi khoản trả, nạp CSV, chạy tính, xác nhận, tính chênh lệch; mỗi TECH có thứ tự kiểm, mã lỗi, audit, ví dụ số.
- File kế toán (SCR-30) có phần 奨励金 đọc từ các bảng này.

## 5. Câu hỏi khách còn mở và issue làm rõ

Q4-55 (nghĩa của trả đủ), Q4-56 (mẫu CSV), Q4-57 (kỳ đích của chênh lệch), Q4-58 (kỳ có hai version 料率), Q4-59 (quá hạn bỏ một giao dịch hay cả kỳ), Q4-60 (tổng âm), Q4-61 (đếm ngày lịch hay ngày làm việc), Q4-63 (thứ tự so ngưỡng, nhân thuế, làm tròn), Q4-64 (huỷ khoản trả ghi nhầm): mỗi câu có issue làm rõ E11-S09..E11-S17 (xem `PREMISE.md` G-01a và `task-breakdown.md` mục 3).

## 6. Backlog dựa vào đâu

Epic E11 (17 issue, 48 sub-issue) tách theo từng điểm ở mục 2 và 3; bảng ánh xạ ở `task-breakdown.md` mục 3.

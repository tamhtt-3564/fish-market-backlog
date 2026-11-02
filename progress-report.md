# Báo cáo tiến độ Sprint 1 (giả lập)

## 1. Thông tin sprint

- **Iteration trên Project:** `Sprint 1` (trường Target version của [Project #1](https://github.com/users/tamhtt-3564/projects/1); xem nhanh ở view "Bảng trạng thái", lọc `target-version:"Sprint 1"`).
- **Thời gian giả lập:** 2027-01-11 tới 2027-01-22, 10 ngày làm việc. Sprint 1 là sprint đầu của giai đoạn xây dựng (T3 theo lịch LAB-1).
- **Đây là sprint giả lập, không phải số liệu thật.** Tiến độ từng việc sinh bằng `python scripts/simulate-sprint-1.py` với hạt ngẫu nhiên cố định (20270111), chạy lại ra cùng kết quả; dữ liệu ở `backlog/sprint-1-simulation.json`, ghi lên Project bằng `python scripts/write-sprint-1-to-project.py`.
- **Giả định của giả lập:**
  - Đội 5,8 người như giai đoạn xây dựng LAB-1 (BE 2, FE 1,5, QA 1, TL 0,5, Infra 0,4, Design 0,2, BA 0,2), cộng BrSE 0,5 người; mỗi người 6 giờ làm thật mỗi ngày.
  - Cam kết 85% năng lực; chọn việc lá theo thứ tự hạ tầng, nền dữ liệu, đăng nhập, việc làm rõ, rồi các việc khác, chỉ lấy việc có mọi việc phụ thuộc (kể cả phụ thuộc của story cha) cũng trong sprint.
  - Giờ làm thật = giờ ước × hệ số ngẫu nhiên (trung bình khoảng 1,1); việc xây dựng có 15% khả năng phải sửa lại sau review.
  - Ngày khách trả lời câu hỏi, cấp tài khoản: ngẫu nhiên từ ngày làm việc thứ 3 tới thứ 15.
  - Người còn từ 1 ngày trống thì kéo thêm việc sẵn sàng từ backlog.
- **Cam kết đầu sprint:** 55 việc, 151 SWP, 286,0 giờ ước. **Kéo thêm giữa sprint:** 2 việc, 9 SWP, 19,7 giờ ước.

## 2. Trạng thái cuối sprint

| Trạng thái | Số issue | Tổng SWP | Ghi chú |
|---|---|---|---|
| Closed | 40 | 105 | Tiếp nhận lô E05 38 SWP; nền dữ liệu E02 9 việc (migration đợt 1, 2 và một phần đợt 10a), 30 SWP; giờ thực tế của 40 việc là 206,3 so với 201,2 giờ ước (+2,5%) |
| In Progress | 3 | 12 | Spec màn SCR-26 ([#120](https://github.com/tamhtt-3564/fish-market-backlog/issues/120)) làm lâu hơn ước; 2 việc kéo thêm giữa sprint: thiết kế và form chốt 相対 ([#380](https://github.com/tamhtt-3564/fish-market-backlog/issues/380), [#384](https://github.com/tamhtt-3564/fish-market-backlog/issues/384)) |
| Issued Tasks (chưa bắt đầu) | 10 | 36 | 9 việc dựng môi trường, cấu hình, sao lưu, CI (E01) và runbook khôi phục (E19): chưa thể bắt đầu vì chưa có tài khoản dịch vụ |
| Pending (chờ khách) | 4 | 7 | Tài khoản dịch vụ ([#37](https://github.com/tamhtt-3564/fish-market-backlog/issues/37)); câu hỏi Q4-25 và Q4-19 ([#45](https://github.com/tamhtt-3564/fish-market-backlog/issues/45)), Q4-44 ([#84](https://github.com/tamhtt-3564/fish-market-backlog/issues/84)), Q4-55 ([#135](https://github.com/tamhtt-3564/fish-market-backlog/issues/135)) |
| **Tổng** | **57** | **160** | Hoàn thành 105/160 SWP (66%); so với cam kết đầu sprint 151 SWP là 70% |

Lệnh đếm: đọc trường Status, Target version, Story Point của Project (truy vấn `fieldValueByName`), 57 mục có Target version `Sprint 1`, khớp `backlog/sprint-1-simulation.json`. 735 mục còn lại giữ trạng thái New, chưa vào sprint.

## 3. Burndown

SWP còn lại cuối mỗi ngày. "Phạm vi" tăng khi kéo thêm việc giữa sprint; đường lý tưởng tính trên 151 SWP cam kết.

| Ngày | Ngày làm việc | Lý tưởng | Phạm vi | Còn lại |
|---|---|---|---|---|
| 0 | Đầu sprint | 151,0 | 151 | 151 |
| 1 | 2027-01-11 | 135,9 | 151 | 148 |
| 2 | 2027-01-12 | 120,8 | 151 | 135 |
| 3 | 2027-01-13 | 105,7 | 151 | 124 |
| 4 | 2027-01-14 | 90,6 | 151 | 109 |
| 5 | 2027-01-15 | 75,5 | 151 | 102 |
| 6 | 2027-01-18 | 60,4 | 151 | 87 |
| 7 | 2027-01-19 | 45,3 | 151 | 80 |
| 8 | 2027-01-20 | 30,2 | 156 | 74 |
| 9 | 2027-01-21 | 15,1 | 160 | 65 |
| 10 | 2027-01-22 | 0,0 | 160 | 55 |

Thực tế lệch kế hoạch ở đâu:
- **Lệch chính là hạ tầng.** Tài khoản dịch vụ (Vercel, Supabase, gửi mail, kho đối tượng, đo uptime) theo kế hoạch có trước ngày đầu sprint, nhưng tới cuối sprint vẫn chưa có. 10 việc hạ tầng phụ thuộc vào tài khoản (36 SWP) chưa bắt đầu được; đây là gần hết phần còn lại.
- **Phần không phụ thuộc tài khoản đi gần đúng kế hoạch.** Nền dữ liệu, tiếp nhận lô, giao nhận làm trên máy của đội; giờ thực tế của việc đã xong chỉ hơn ước 2,5%.
- **Từ ngày 8, đội kéo thêm 2 việc** (9 SWP) cho người đang trống vì việc hạ tầng bị chặn; hai việc này chưa xong, nên phạm vi tăng từ 151 lên 160 SWP và đường còn lại giảm chậm hơn ở hai ngày cuối.
- **Tốc độ Sprint 1:** 105 SWP. Năng lực đủ của đội khi không bị chặn ước khoảng 174 SWP mỗi sprint (321 giờ cam kết × 0,54 SWP mỗi giờ theo `estimate.md`).

## 4. Rủi ro trễ

| Rủi ro | Issue | Ảnh hưởng tới mốc nào | Hành động | Ai làm, khi nào |
|---|---|---|---|---|
| Chưa có 5 tài khoản dịch vụ do khách đứng tên | [#37](https://github.com/tamhtt-3564/fish-market-backlog/issues/37) E01-S01; chặn [#194](https://github.com/tamhtt-3564/fish-market-backlog/issues/194), [#195](https://github.com/tamhtt-3564/fish-market-backlog/issues/195), [#196](https://github.com/tamhtt-3564/fish-market-backlog/issues/196) và các việc E01-S03, S04, S05, E19-S01 | Môi trường staging cho QA và triển khai từ Sprint 2; mọi việc kiểm trên staging của Sprint 2 | Xin khách cấp tài khoản, gửi lại danh sách quyền cần cấp; Infra chuẩn bị sẵn script dựng môi trường để chạy ngay trong 1 ngày khi có tài khoản; đội dùng DB chạy trên máy cho việc phát triển trong lúc chờ | PM-A gửi khách 2027-01-25, hạn cấp 2027-01-27; Infra-A xong script trước 2027-01-27 |
| Khách chưa trả lời phương án sao lưu một vùng (Q4-25, Q4-19) | [#45](https://github.com/tamhtt-3564/fish-market-backlog/issues/45) E01-S09 | Dựng production (gói có PITR, [#194](https://github.com/tamhtt-3564/fish-market-backlog/issues/194)); khác phương án mặc định thì đổi khối lượng hạ tầng | Gửi lại câu hỏi kèm ba rủi ro và chi phí từng phương án, xin trả lời bằng văn bản | BrSE-A gửi 2027-01-25, hạn trả lời 2027-01-29 |
| Khách chưa trả lời cách xử lý lô kẹt sau khoá ngày (Q4-44) | [#84](https://github.com/tamhtt-3564/fish-market-backlog/issues/84) E05-S08 | Sprint làm chuyển lô kẹt ([#81](https://github.com/tamhtt-3564/fish-market-backlog/issues/81) E05-S05); đang làm theo phương án (a) chuyển lô | Nhắc trong họp tuần; nếu khách chọn khác (a) thì ước lại E05-S05 trước khi đưa vào sprint | BrSE-A, họp tuần 2027-01-28 |
| Khách chưa trả lời nghĩa "trả đủ" khi tính 完納奨励金 (Q4-55) | [#135](https://github.com/tamhtt-3564/fish-market-backlog/issues/135) E11-S09 | Các issue tính 完納奨励金 của E11 (điều kiện được thưởng E11-S05) | Gửi kèm ví dụ tính bằng số cho hai cách hiểu để khách chọn | BrSE-A gửi 2027-01-25, hạn trả lời trước sprint có E11-S05 |
| Spec màn SCR-26 làm lâu hơn ước (BA 0,2 người) | [#120](https://github.com/tamhtt-3564/fish-market-backlog/issues/120) E10-S01 | Các issue xây dựng màn SCR-26 (E10) chưa vào sprint được tới khi spec xong | Tăng BA lên 0,4 người ở Sprint 2 để xong spec SCR-26 và bắt đầu spec các màn chưa có spec khác | PM-A chốt ở buổi lập kế hoạch Sprint 2, 2027-01-25 |
| Tốc độ Sprint 1 (105 SWP) thấp hơn năng lực đủ (khoảng 174 SWP) | Toàn backlog: còn 2.082 SWP | Mốc Cổng 3 sẵn sàng chuyển đổi và UAT (T8 tuần 2 theo LAB-1) còn khoảng 10 sprint tính từ Sprint 2. Ở tốc độ đủ cần khoảng 12 sprint, ở tốc độ Sprint 1 cần khoảng 20 sprint | Gỡ chặn tài khoản trong tuần đầu Sprint 2; theo dõi tốc độ Sprint 2, 3; nếu vẫn dưới 174 SWP thì đề xuất với khách thêm người hoặc dời mốc | PM-A, báo cáo cùng kết quả Sprint 2 (2027-02-05) |

Ghi chú: ngày hẹn với khách trong bảng là ngày của kịch bản giả lập.

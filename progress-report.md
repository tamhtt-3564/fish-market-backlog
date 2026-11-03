# Báo cáo tiến độ Sprint 1 (giả lập)

## 1. Thông tin sprint

- **Iteration trên Project:** `Sprint 1` (trường Target version của [Project #1](https://github.com/users/tamhtt-3564/projects/1); xem ở tab [Sprint 1 (giả lập)](https://github.com/users/tamhtt-3564/projects/1/views/8): bảng cột theo trạng thái, đã lọc sẵn `target-version:"Sprint 1"`, 69 việc).
- **Thời gian giả lập:** 2027-01-11 tới 2027-01-22, 10 ngày làm việc; sprint đầu của giai đoạn xây dựng.
- **Đây là sprint giả lập, không phải số liệu thật.** Tiến độ từng việc sinh bằng `python scripts/simulate-sprint-1.py` (hạt ngẫu nhiên 20270111, chạy lại ra cùng kết quả), lưu ở `backlog/sprint-1-simulation.json`, ghi lên Project bằng `python scripts/write-sprint-1-to-project.py`. Issue có trạng thái Closed được đóng trên GitHub cho khớp board; các ngày hẹn ở mục 4 là ngày của kịch bản giả lập.
- **Giả định của giả lập** (đọc từ mã của script):
  - Đội 5,8 người bằng số người bình quân của giai đoạn xây dựng trong kế hoạch tổng; phân vai do người lập báo cáo giả định: BE 2, FE 1,5, QA 1, TL 0,5, Infra 0,4, Design 0,2, BA 0,2. Thêm BrSE 0,5 người. Mỗi người 6 giờ làm thật mỗi ngày.
  - Cam kết 85% năng lực. Chọn việc theo thứ tự: hạ tầng, nền dữ liệu, đăng nhập, việc làm rõ, rồi việc khác; chỉ lấy việc mà mọi việc phụ thuộc (kể cả phụ thuộc của story cha) cũng trong sprint.
  - Thứ tự phụ thuộc lấy từ quan hệ blocked by của backlog, gồm cả luật trong story (`task-breakdown.md`, đoạn trước mục 1.6): giao diện chờ BE và thiết kế giao diện, kiểm thử chờ việc làm mã, việc cần staging, Vercel hay production chờ dựng môi trường.
  - Giờ làm thật = giờ ước × hệ số ngẫu nhiên, trung bình 1,1. Việc xây dựng có 15% khả năng phải sửa sau review; khi đó cộng thêm 30% giờ.
  - Việc xây dựng làm xong còn 1 ngày chờ review và kiểm mới Closed; thiết kế, ca kiểm thử, tài liệu, vận hành chờ 0,5 ngày. Giờ review và kiểm của TL, QA không trừ vào năng lực của họ.
  - Ngày khách trả lời câu hỏi hoặc cấp tài khoản: ngẫu nhiên từ ngày làm việc thứ 3 tới thứ 15.
  - Ai phải chờ việc cam kết từ 1 ngày trở lên thì kéo việc sẵn sàng từ backlog làm trước.
- **Cam kết đầu sprint:** 54 việc, 146 SWP, 273,4 giờ ước. **Kéo thêm giữa sprint:** 15 việc, 59 SWP, 122,2 giờ ước.

## 2. Trạng thái cuối sprint

| Trạng thái | Số issue | Tổng SWP | Ghi chú |
|---|---|---|---|
| Closed | 41 | 115 | 32 việc cam kết (79 SWP) và 9 việc kéo thêm (36 SWP). Nhiều nhất ở tiếp nhận lô (E05, 39 SWP), nền dữ liệu (E02, 18 SWP), giao nhận (E07, 17 SWP) |
| In Progress | 4 | 16 | Thiết kế lớp ngoại tuyến ([#685](https://github.com/tamhtt-3564/fish-market-backlog/issues/685)); 3 việc kéo thêm: hàm ghi 目利き ([#369](https://github.com/tamhtt-3564/fish-market-backlog/issues/369)), thiết kế giao diện nhập giao dịch ([#380](https://github.com/tamhtt-3564/fish-market-backlog/issues/380)), spec SCR-28 ([#144](https://github.com/tamhtt-3564/fish-market-backlog/issues/144)) |
| In Review | 3 | 9 | View đợt 2a ([#221](https://github.com/tamhtt-3564/fish-market-backlog/issues/221)); form tiếp nhận lô trực tuyến ([#354](https://github.com/tamhtt-3564/fish-market-backlog/issues/354)) và ca kiểm thử ngoại lệ giao nhận ([#447](https://github.com/tamhtt-3564/fish-market-backlog/issues/447)), là việc kéo thêm |
| QA Testing | 2 | 7 | Backfill đợt 2a ([#220](https://github.com/tamhtt-3564/fish-market-backlog/issues/220)); nút 完納 trên SCR-18 ([#433](https://github.com/tamhtt-3564/fish-market-backlog/issues/433)), việc kéo thêm |
| Issued Tasks (chưa bắt đầu) | 15 | 51 | 9 việc E01 (33 SWP): dựng môi trường, cấu hình, CI, sao lưu, kiểm cảnh báo bảo mật trên staging, đều chờ tài khoản dịch vụ; 4 việc giao diện ngoại tuyến (E14, 13 SWP) chờ thiết kế #685; kiểm câu báo lỗi trên staging ([#312](https://github.com/tamhtt-3564/fish-market-backlog/issues/312)); runbook mất dự án Supabase ([#776](https://github.com/tamhtt-3564/fish-market-backlog/issues/776)) |
| Pending (chờ khách) | 4 | 7 | Tài khoản dịch vụ ([#37](https://github.com/tamhtt-3564/fish-market-backlog/issues/37)); câu hỏi Q4-28 ([#83](https://github.com/tamhtt-3564/fish-market-backlog/issues/83)), Q4-55 ([#135](https://github.com/tamhtt-3564/fish-market-backlog/issues/135)), Q4-60 ([#138](https://github.com/tamhtt-3564/fish-market-backlog/issues/138)) |
| **Tổng** | **69** | **205** | Xong 115/205 SWP (56%). Riêng phần cam kết đầu sprint: xong 79/146 SWP (54%) |

Lệnh đếm (chạy từ gốc repo):

```bash
gh api graphql --paginate -f query='query($endCursor:String){user(login:"tamhtt-3564"){projectV2(number:1){items(first:100,after:$endCursor){pageInfo{hasNextPage endCursor} nodes{t:fieldValueByName(name:"Target version"){... on ProjectV2ItemFieldIterationValue{title}} s:fieldValueByName(name:"Status"){... on ProjectV2ItemFieldSingleSelectValue{name}} p:fieldValueByName(name:"Story Point"){... on ProjectV2ItemFieldNumberValue{number}}}}}}}' --jq '.data.user.projectV2.items.nodes[] | select(.t.title=="Sprint 1") | [.s.name, .p.number] | @tsv' | awk -F'\t' '{n[$1]++; s[$1]+=$2} END {for (k in n) print k, n[k], s[k]}'
```

Trên GitHub: 41 issue đóng, 751 issue mở. 723 mục ngoài sprint giữ trạng thái New.

## 3. Burndown

SWP còn lại cuối mỗi ngày. "Phạm vi" tăng khi kéo thêm việc giữa sprint; đường lý tưởng tính trên 146 SWP cam kết.

| Ngày | Ngày làm việc | Lý tưởng | Phạm vi | Còn lại |
|---|---|---|---|---|
| 0 | Đầu sprint | 146,0 | 146 | 146 |
| 1 | 2027-01-11 | 131,4 | 146 | 146 |
| 2 | 2027-01-12 | 116,8 | 151 | 141 |
| 3 | 2027-01-13 | 102,2 | 154 | 134 |
| 4 | 2027-01-14 | 87,6 | 162 | 129 |
| 5 | 2027-01-15 | 73,0 | 174 | 124 |
| 6 | 2027-01-18 | 58,4 | 178 | 108 |
| 7 | 2027-01-19 | 43,8 | 186 | 101 |
| 8 | 2027-01-20 | 29,2 | 193 | 101 |
| 9 | 2027-01-21 | 14,6 | 205 | 100 |
| 10 | 2027-01-22 | 0,0 | 205 | 90 |

Thực tế lệch kế hoạch ở đâu:
- **Phần cam kết chỉ xong 54%.** Lý do lớn nhất: 5 tài khoản dịch vụ (Vercel, Supabase, gửi mail, kho đối tượng, đo uptime) theo kế hoạch có trước ngày đầu sprint nhưng tới cuối sprint vẫn chưa có. 9 việc E01 (33 SWP) và 1 việc kiểm trên staging không bắt đầu được; riêng 9 việc E01 là 49% phần cam kết chưa xong.
- **Đội không ngồi chờ:** từ ngày 2, người bị chặn kéo thêm 15 việc sẵn sàng (59 SWP), xong 9 việc. Vì vậy phạm vi tăng từ 146 lên 205 SWP và đường còn lại giảm chậm hơn đường lý tưởng suốt sprint.
- **Năng lực dùng không đều:** BE, QA, TL, Design, BA dùng gần hết giờ. FE chỉ dùng 29 trên 90 giờ, vì việc giao diện phải chờ hàm DB, route của BE và thiết kế; Infra dùng 10 trên 24 giờ vì chờ tài khoản. Trong Sprint 1, BE và TL là chỗ nghẽn. Tính cho cả phần xây dựng còn lại thì BE, QA và Design thiếu người nhiều nhất (`estimate.md` mục 5, bảng theo vai).
- **Ước lượng:** 41 việc đã xong làm 214,2 giờ so với 214,5 giờ ước. Có việc đang làm vượt ước: thiết kế lớp ngoại tuyến #685 đã dùng 6,5 giờ so với 4,2 giờ ước (+55%) và đang chặn 4 việc FE; form tiếp nhận lô #354 dùng 14,9 so với 10,2 giờ (+46%).
- **Tốc độ Sprint 1:** 115 SWP. Năng lực đủ của đội khi không bị chặn ước khoảng 174 SWP mỗi sprint (321 giờ cam kết × 0,54 SWP mỗi giờ theo `estimate.md`); đội chưa đạt mức này ở sprint nào.

## 4. Rủi ro trễ

| Rủi ro | Issue | Ảnh hưởng tới mốc nào | Hành động | Ai làm, khi nào |
|---|---|---|---|---|
| Chưa có 5 tài khoản dịch vụ, theo kế hoạch Quý khách cấp trước ngày đầu Sprint 1 | [#37](https://github.com/tamhtt-3564/fish-market-backlog/issues/37) E01-S01; chặn [#194](https://github.com/tamhtt-3564/fish-market-backlog/issues/194), [#195](https://github.com/tamhtt-3564/fish-market-backlog/issues/195), [#196](https://github.com/tamhtt-3564/fish-market-backlog/issues/196), các việc E01-S03, S04, S05 còn lại và các việc kiểm trên staging (#214, #312) | Môi trường staging để kiểm và triển khai từ Sprint 2 | Xin Quý khách cấp tài khoản, gửi lại danh sách quyền cần cấp; chuẩn bị sẵn script dựng môi trường để chạy xong trong 1 ngày khi có tài khoản | PM-A gửi 2027-01-25, xin cấp trước 2027-01-27; Infra-A xong script trước 2027-01-27 |
| Câu hỏi Q4-28 về màn quản lý danh mục 荷目 chưa có trả lời | [#83](https://github.com/tamhtt-3564/fish-market-backlog/issues/83) E05-S07 | Sprint làm tiếp nhận lô SCR-09 tiếp theo; nếu cần màn riêng thì thêm một màn | Gửi lại câu hỏi kèm phương án mặc định (nạp danh mục cùng dữ liệu gốc) | BrSE-A gửi 2027-01-25, xin trả lời trước 2027-02-01 |
| Câu hỏi Q4-55 (nghĩa của "trả đủ") và Q4-60 (tổng kỳ âm) về 完納奨励金 chưa có trả lời | [#135](https://github.com/tamhtt-3564/fish-market-backlog/issues/135) E11-S09, [#138](https://github.com/tamhtt-3564/fish-market-backlog/issues/138) E11-S12 | Các issue tính 完納奨励金 (điều kiện được thưởng E11-S05, chuyển phần âm E11-S06) | Gửi kèm ví dụ tính bằng số cho từng cách hiểu để Quý khách chọn | BrSE-A gửi 2027-01-25, xin trả lời trước 2027-02-05 |
| Việc giao diện phải chờ BE và thiết kế; FE dùng 32% năng lực | Ví dụ [#686](https://github.com/tamhtt-3564/fish-market-backlog/issues/686), [#687](https://github.com/tamhtt-3564/fish-market-backlog/issues/687), [#688](https://github.com/tamhtt-3564/fish-market-backlog/issues/688) chờ [#685](https://github.com/tamhtt-3564/fish-market-backlog/issues/685) | Tốc độ các sprint sau; mọi màn có giao diện | Sprint 2 xếp việc BE và thiết kế trước việc FE cùng story; FE-A còn dư năng lực (cần 6 trên 7 sprint) nên chuyển 0,5 người FE-A sang làm BE trong Sprint 2 (FE-A vẫn đủ giờ cho phần việc của mình trong 7 sprint) | PM-A chốt ở buổi lập kế hoạch Sprint 2, 2027-01-25 |
| Khối lượng xây dựng vượt lịch, kể cả khi đội chạy đủ năng lực | Toàn backlog: phần xây dựng E01..E16 còn 1.801 SWP | Hết giai đoạn xây dựng (2027-05-08, còn 7 sprint tính từ Sprint 2). Tính gộp cả đội: ở năng lực đủ 174 SWP (chưa đạt) cần khoảng 10,4 sprint, ở tốc độ đo được 115 SWP cần khoảng 15,7 sprint. Tính theo từng vai (người không đổi vai cho nhau được): dù chạy đủ năng lực, Design cần 16 sprint, QA 15, BE khoảng 14,5 (`estimate.md` mục 5) | Báo trước với Quý khách ngay, không chờ thêm số liệu. Hai phương án để chọn ở buổi review Sprint 2, kèm tác động chi phí: (a) tăng đội từ Sprint 3: nếu đội đạt năng lực đủ, cần thêm khoảng 4,7 người, chia theo vai BE 2,5, QA 1,3, FE 0,5, Design 0,3 (`estimate.md` mục 5, tính theo giờ còn lại của từng vai); nếu giữ tốc độ Sprint 1 thì cần tới khoảng 9 người (tính gộp theo SWP); (b) giữ đội, dời mốc hết xây dựng khoảng 16 tới 18 tuần ngay cả khi đạt năng lực đủ (16 tuần nếu tăng Design từ 0,2 lên 0,5 người, vì vai chậm nhất là QA 15 sprint); lâu hơn nếu giữ tốc độ Sprint 1. Song song gỡ chặn tài khoản và cân lại FE, BE để kéo tốc độ về gần năng lực đủ; số đo Sprint 2 dùng để thu hẹp khoảng | PM-A gửi phương án 2027-02-03, chốt cùng Quý khách ở buổi review Sprint 2 (2027-02-05) |

Cách tính phương án: (a) ở năng lực đủ: theo từng vai, như bảng theo vai của `estimate.md` mục 5; ở tốc độ Sprint 1: số người cần = (1.801 − SWP của Sprint 2) / 6 sprint còn lại sau Sprint 2, chia cho tốc độ mỗi người (115 / 6,3 người), trừ 6,3 người hiện có; (b) số tuần dời = (số sprint của vai chậm nhất − 7) × 2 tuần, số sprint từng vai lấy ở bảng theo vai của `estimate.md` mục 5. Số tính gộp cả đội (10,4 sprint, khoảng 7 tuần) không dùng cho phương án vì giả định người đổi vai cho nhau được.

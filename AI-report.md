# Báo cáo dùng AI (LAB-5)

Công cụ chính: Claude Code (agent chính) chạy trong project luyện tập, gọi skill của bộ Takumi, agent con và script trong `scripts/`. Mã lỗi L-xx dẫn tới bảng nhật ký lỗi AI ở cuối file. Mã D5-xx còn trong bảng nhật ký là dòng sổ quyết định LAB-5, sổ này ở project luyện tập, không nộp; nội dung quyết định đã tóm tắt ngay trong câu chứa mã.

## 1. Skill và prompt cho từng việc

| Việc | Skill, agent, script | Prompt viết thế nào |
|---|---|---|
| Lập kế hoạch, PREMISE (bước 0, 1) | Agent chính; skill tự viết `lab5-review-backlog-output` (thư mục `skills/`) để soát | Mỗi bước có một prompt ngắn nêu đầu vào (bộ spec LAB-4 commit `21bbe4b`, sổ D4-xx, estimate LAB-1), đầu ra, luật repo public (không chép RFP, không dữ liệu cá nhân). Chỗ cần người quyết thì agent hỏi bằng câu chọn có 2 tới 4 phương án và một phương án đề xuất |
| Chia task (bước 2) | 5 agent con chạy song song, mỗi agent một nhóm epic; `scripts/validate-backlog-items.py`, `render-spec-to-issue-table.py`; skill `tkm:ask-expert` soát nguyên tắc chia việc theo từng vai | Brief cho mỗi agent gồm: nhóm epic và danh sách file spec phải đọc, khuôn JSON (`backlog/backlog-item-format.md`), luật độ hạt (việc lá tối đa 14 giờ, tức 2 ngày), 11 vai phụ trách, nhãn, vai trò người dùng được làm và bị chặn, file đầu ra. Agent chính gộp 5 file, chạy script kiểm và bảng phủ hai chiều spec ↔ issue. Prompt `tkm:ask-expert`: "review trước mấy nguyên tắc trên đủ mọi role tham gia dự án", ra 7 điểm sửa, người dùng chọn sửa cả 7 |
| Tạo issue (bước 3) | `scripts/create-project-issues.py` qua `gh api graphql` | Agent chính viết script từ khuôn JSON: tạo issue cha trước con, gắn sub-issue, nhãn, Status, Phụ trách; ghi số issue dần vào file nên chạy lại được sau khi bị ngắt; đi chậm dưới giới hạn tạo nội dung của GitHub |
| Chấm SWP (bước 4, soát góc PM đầu bước 5) | Skill `tkm:sun-estimate`; 5 agent con chấm 5 lô; `tkm:ask-expert` soát dưới góc PM | Prompt gọi skill: "Chấm SWP cho backlog trên Project #1 (792 mục), ra báo cáo HTML trong `estimate/`; người dùng chốt issue mẫu trước khi ghi Story Point". Mỗi agent chấm nhận một file luật chấm (ma trận Scope × Complexity, từ vựng dấu hiệu, mức tin) và một file lô, chỉ đọc ghi trong thư mục tạm, tự kiểm JSON trước khi trả. Skill tự chọn 5 issue mẫu; người duyệt từng issue qua hai câu hỏi (mức khó, rồi điểm cụ thể). Prompt `tkm:ask-expert`: "review bước 4 as an expert PM", ra 3 vấn đề và khuyến nghị kiểm thêm 2 issue QA, FE (người dùng chọn làm) |
| Ghi SWP lên Project | Agent chính chạy `scripts/write-story-points-to-project.py` | Skill chấm SWP chỉ đọc, không ghi Project. Sau khi người duyệt issue mẫu, agent chính xuất SWP đã duyệt từ payload đã kiểm của skill ra `backlog/story-points.json` (một lệnh chạy một lần, không có script riêng trong repo), rồi chạy script ghi Story Point cho 792 mục, thêm Scope, Complexity cho 654 việc lá (gộp 10 lệnh `updateProjectV2ItemFieldValue` mỗi lần gọi, chạy nền). Ghi xong, agent đọc ngược trường Story Point của 792 mục từ Project, so với file: 0 mục lệch, tổng 19 epic bằng tổng 654 việc lá (2.187). Không giao bước ghi cho agent con, để agent chính đối chiếu được ngay |
| Quy giờ (bước 5) | `scripts/convert-story-points-to-hours.py` (tính giờ, ghi `backlog/estimated-hours.json`), `write-story-points-to-project.py --only-hours` (ghi Estimated time lên Project); agent con soát độc lập | Agent chính đưa người dùng 3 cách quy kèm số liệu lệch theo vai (một hệ số chung làm QA dư khoảng 32%, FE-B thiếu khoảng 32%); người dùng chọn hệ số theo vai. Script áp một quy tắc cho mọi việc; script thứ hai ghi Estimated time lên Project; agent đọc ngược kiểm 0 lệch |
| Báo cáo tiến độ (bước 6) | `scripts/simulate-sprint-1.py` (hạt ngẫu nhiên cố định), `write-sprint-1-to-project.py`, `add-implicit-story-dependencies.py`; agent con soát 2 lượt | Giả định của giả lập ghi trong mã và chép sang mục 1 của báo cáo. Báo cáo viết từ số đọc ngược trên Project, không từ trí nhớ của agent. Prompt soát dặn riêng: tìm việc Closed trước khi việc phụ thuộc xong, kiểm phép tính dự báo, câu chữ gửi khách được |
| Soát từng bước (bước 0 tới 8) | Skill tự viết `lab5-review-backlog-output`: cổng máy `run-lab5-backlog-gate.py` và câu hỏi B1..B9. Bước 2, 5, 6, 7, 8 có agent con soát độc lập; bước 0, 1, 3, 4 do agent chính tự soát theo skill | Prompt soát theo một khuôn: đường dẫn làm việc, nơi ghi báo cáo, phạm vi bước, các phép kiểm bắt buộc (đếm lại, đọc Project chỉ bằng query, đối chiếu nguồn), ràng buộc "chỉ ghi báo cáo soát, không sửa file nộp, không sửa Project", đầu ra (kết luận, số lỗi theo mức, dòng đề xuất nhật ký) |

## 2. Review output của AI

**Người review ở đâu.** Trong 26 quyết định ghi ở sổ quyết định LAB-5, 18 do người dùng chọn hoặc duyệt. Các chặng người quyết:
- chốt phạm vi, cách xử lý 9 màn chưa có spec và câu hỏi khách (bước 1);
- duyệt từng bước sau khi máy soát Đạt; chọn theo mẫu Project công ty; chọn cách sửa khi soát ra lỗi;
- duyệt 5 issue mẫu của skill và 2 issue kiểm thêm;
- chọn cách quy giờ; chọn cách xử lý khung sửa lỗi khi so LAB-1;
- chọn bổ sung phụ thuộc vào backlog;
- duyệt giọng văn báo cáo gửi khách.

**Máy review ở đâu.**
- Cổng máy chạy trước mỗi lần đẩy repo: dấu kiểu AI, chép câu RFP, khoá bí mật, email trong file và trong lịch sử commit, file bắt buộc theo bước.
- Script kiểm dữ liệu backlog chạy sau mỗi lần sửa.
- Agent con soát độc lập, không tham gia soạn, ở bước 2 (3 lượt), 5, 6 (2 lượt), 7, 8. Bước 0, 1, 3, 4 do agent chính tự soát theo skill; bước 4 có thêm lượt `tkm:ask-expert` soát góc PM.
- Mọi số đưa vào file được đọc ngược từ Project, kèm lệnh đếm.
- Trước khi nộp: một lượt soát độc lập theo 9 vai dùng bài (người chấm, khách, PM, BrSE, BA, TL, dev, QA, Infra), tìm 5 lỗi Nặng; người dùng chọn sửa 3 (so ước lượng theo giai đoạn và theo vai, tóm tắt SCR-25 trong repo, theo dõi issue làm rõ), 2 lỗi còn lại ghi ở mục 3.

**Phát hiện gì, xử lý thế nào.** Nhật ký có 40 lỗi AI.
- Theo kênh phát hiện (đếm theo cột "Phát hiện thế nào" của nhật ký): 24 lỗi do soát độc lập bắt, 12 lỗi do agent chính tự kiểm lại trước khi trình, 3 lỗi do agent con tự báo, 1 lỗi phát hiện khi gộp bảng phủ.
- Theo kiểu lỗi:

| Kiểu lỗi | Lỗi | Xử lý chung |
|---|---|---|
| Viết hoặc kết luận trước khi đọc nguồn hay đếm | L-01, L-02, L-03, L-06, L-09, L-17, L-19, L-24, L-26, L-29, L-32, L-33, L-34, L-38, L-40 | Mỗi số trong file kèm lệnh đếm; mở nguồn trước khi viết lý do; kết luận dự báo phải theo số đã đo (L-26, L-29) |
| Script hoặc mô hình máy làm sai nghĩa nghiệp vụ | L-14, L-15, L-21, L-22, L-23, L-25, L-27, L-39 | Soát kết quả máy theo nghĩa nghiệp vụ, không chỉ chạy được; lỗi nặng nhất là L-25: giả lập cho 14 việc kiểm thử, giao diện xong trước khi có mã, báo cáo kết luận "đi gần đúng kế hoạch". Sửa bằng 456 phụ thuộc bổ sung vào backlog (người dùng chọn sửa vào dữ liệu thay vì chỉ sửa giả lập), chạy lại giả lập |
| Chia việc bằng nhiều agent | L-04, L-05, L-07, L-12 | Việc nằm giữa hai nhóm, tiêu chí chép đồng loạt, sub trùng: gộp rồi soát chéo; agent con được phép không làm theo brief sai (L-04) |
| Dẫn mã sai, bảng thiếu mã hay thiếu liên kết, dùng cách xử lý ngoài đề | L-08, L-20, L-30, L-31, L-35, L-36 | Đối chiếu cột "issue bị ảnh hưởng" của PREMISE và đếm đủ danh sách mã A1..A53, N-01..N-25 bằng lệnh |
| Sửa một chỗ không lan, sửa không đủ | L-13, L-16, L-28 | Sửa xong tìm mọi chỗ dùng cùng ý; kiểm lại đúng ví dụ người soát đã nêu |
| Thao tác công cụ, bảo mật | L-10, L-11, L-18, L-37 | Không dùng `git reset --hard` khi còn sửa đổi chưa commit; email commit đổi sang địa chỉ noreply, viết lại lịch sử, cổng thêm kiểm email commit; kiểm quyền công cụ của agent trước khi giao việc; không cắt đầu ra của script đang ghi dữ liệu |

## 3. Điểm đặc biệt trong cách dùng AI

**Chỗ tin là hiệu quả.**
- Một nguồn dữ liệu duy nhất (`backlog/items-*.json`), mọi bảng, issue, SWP, giờ sinh bằng script. Sửa dữ liệu một chỗ rồi chạy lại là mọi nơi khớp; chạy lại không tạo trùng (kiểm 792 issue, 0 trùng).
- Đọc ngược Project sau mỗi lần ghi, so với file (Story Point, Estimated time, trạng thái Sprint 1 đều 0 mục lệch). Số trong báo cáo vì vậy có bằng chứng từ Project, không từ trí nhớ của agent.
- Soát độc lập bằng agent không tham gia soạn bắt được hơn nửa số lỗi (24/40), trong đó có lỗi nặng mà người soạn không thấy (L-25).
- Giả lập có hạt ngẫu nhiên cố định nên người soát chạy lại được và ra cùng kết quả; lệch kế hoạch đến từ mô hình, không viết tay.
- Đưa người dùng câu hỏi có phương án và số liệu đi kèm (ví dụ cách quy giờ) giúp quyết nhanh mà vẫn là người quyết.

**Chỗ chưa tốt, cần cải thiện khi làm thật.**
- Lỗi lặp lại nhiều lần cùng kiểu: viết hoặc kết luận trước khi đọc nguồn hay đếm (15 lỗi); sửa một chỗ không lan, sửa không đủ (3 lỗi). Làm thật nên đưa vào cổng máy phép đối chiếu chéo số đếm giữa các file, thay vì chỉ dựa vào soát.
- Thứ tự phụ thuộc trong story (kiểm thử chờ mã, giao diện chờ API, việc cần staging chờ môi trường) chỉ được bổ sung ở bước 6, sau khi giả lập lộ lỗi. Làm thật nên đặt luật này ngay khi chia task ở bước 2.
- SWP phân biệt việc to nhỏ kém: 415/654 việc cùng 3 SWP, tương quan với giờ thô 0,52. Skill giới hạn 5 issue mẫu, 4 trong 5 là việc ngoại lệ; phải kiểm thêm 2 issue ngoài skill. Làm thật nên chọn mẫu theo từng nhóm việc chính.
- Agent chấm riêng của skill không có quyền đọc file nên phải thay bằng agent thường (L-18, ghi ở caveats của báo cáo HTML).
- Giới hạn của GitHub tốn thời gian:
  - tạo 792 issue mất hơn 10 giờ (đi chậm để tránh bị chặn, máy ngủ ban đêm);
  - lỗi 502 khi gộp nhiều lệnh;
  - một issue chỉ chặn được tối đa 100 issue, nên 10 quan hệ chờ E01-S02 chỉ ghi trong thân issue.
- Token: chia việc bằng 5 agent và soát nhiều lượt tốn nhiều. Bước 6 soát 2 lượt vì lượt sửa đầu chưa đủ (L-28); kiểm lại đúng ví dụ người soát nêu trước khi gửi soát lại thì đỡ một lượt.

- Hai lỗi Nặng của lượt soát theo vai chưa sửa, người dùng chọn để lại:
  - 16 việc dev được tính Closed khi chưa có staging. Tuỳ cách hiểu định nghĩa xong: nếu QA kiểm trên máy của đội thì đúng; nếu bắt kiểm trên staging thì tốc độ Sprint 1 còn thấp hơn.
  - Báo cáo tiến độ viết tiếng Việt cho lớp học; gửi khách Nhật thật thì cần bản 1 trang tiếng Nhật, bỏ lệnh đếm và chuyện phân bổ giờ nội bộ.

**Chưa có ý tưởng:** cách để AI tự nhận ra chỗ "kết quả máy đúng cú pháp nhưng sai nghĩa nghiệp vụ" (L-25) mà không cần một lượt soát riêng.

## Nhật ký lỗi AI

Chép từ nhật ký lỗi AI của LAB-5, đánh số theo thứ tự ghi.

| Mã | Ngày | Bước | AI sai gì | Phát hiện thế nào | Sửa thế nào |
|---|---|---|---|---|---|
| L-01 | 2026-10-30 | Lập kế hoạch (D5-04) | Claude đề xuất sprint giả lập 2026-11-09..11-20 "bắt đầu từ ngày kick-off LAB-1" mà không mở lịch LAB-1: theo step-07 mục 6, T1–T2 là giai đoạn yêu cầu, thiết kế; việc xây dựng (backlog LAB-5) bắt đầu từ T3. Người dùng đã chốt theo đề xuất sai | Claude đọc kế hoạch nguồn lực LAB-1 khi đặt tên vai cho trường Phụ trách | Chưa tạo Iteration; hỏi lại người dùng, người dùng chốt 2027-01-11 (D5-04) |
| L-02 | 2026-11-01 | 1 (PREMISE) | Bản nháp PREMISE gán ý không có ở nguồn: H-03 thêm phương án "ẩn danh hoá ngay khi có yêu cầu" mà Q4-10 không hỏi; H-02 viết phương án (c) "không còn lịch sử" trong khi (c) vẫn ghi bút toán có lý do; G-06 dẫn D4-125 cho C-18, C-20 (hai dòng này giao thẳng LAB-5). Tái phạm kiểu "gán ý cho mã không nói ý đó" của LAB-1..4 | Tác giả mở lại dòng Q4-10, Q4-44 và bảng C-xx khi tự soát bước 1 | Sửa theo đúng chữ nguồn; ghi ở `docs/lab5/reviews/step-01-review.md` |
| L-03 | 2026-11-01 | 1 (PREMISE), lập brief bước 2 | Claude viết H-05 "đợt 10 sau đợt 9" dựa vào một câu của LAB-4 ("không hàm nào của 9 đợt đọc các bảng này") mà không mở TECH kiểm: hàm cảnh báo khoá ngày của đợt 7 đọc `report_runs`. Câu sai từ LAB-4, Claude chép sang không kiểm (tái phạm "nhận nguồn không kiểm" của LAB-4) | Agent soạn E08, E09 đọc TECH khoá ngày khi chia việc | Sửa H-05, thêm S-02, tách đợt 10a, 10b (D5-16) |
| L-04 | 2026-11-01 | Brief bước 2 | Brief cho nhóm 完納奨励金 dặn ghi phụ thuộc "sang E12" cho phần file kế toán: ngược chiều, vì phần xuất dữ liệu thanh toán của E12 cần bảng của đợt 9 ở E11 | Agent nhóm 完納奨励金 tự phát hiện, không làm theo brief, báo lại | E12-S09 phụ thuộc E11-S01; E11 không phụ thuộc E12 |
| L-05 | 2026-11-01 | 2 (chia việc) | Năm agent chia theo nhóm epic để lọt việc nằm giữa hai nhóm: bỏ hằng số cũ trong mã, việc nền cảnh báo biên nhận đồng bộ, sửa tài liệu spec không nhóm nào nhận; phụ thuộc chéo nhóm không ghi được | Đọc mục "chỗ hở" của 5 bảng phủ khi gộp | Thêm 4 issue, nối phụ thuộc (D5-17); bài học: chia theo nhóm thì bước gộp phải dò riêng việc "giao nhóm khác" |
| L-06 | 2026-11-01 | 2 (task-breakdown mục 3) | Claude viết "E11 có 47 sub-issue" bằng cách cộng nhẩm từ danh sách, chưa đếm bằng lệnh (tái phạm lỗi đếm tay của LAB-4) | Đếm bằng lệnh trước khi trình người dùng: 48 | Sửa số, ghi lệnh đếm cạnh số |
| L-07 | 2026-11-01 | 2 (soát độc lập) | Năm agent soạn chép một bộ tiêu chí chung "vai bị chặn gọi thẳng API" vào 23 ca kiểm thử của việc nền và migration không có API; bước thiết kế ngắn và lớp QA không đều giữa các nhóm (7 Vừa) | Soát độc lập bước 2 (V2..V5, N5) | Sửa bằng luật chung có script (D5-18) |
| L-08 | 2026-11-01 | 2 (task-breakdown mục 4) | Claude dùng "Tạo issue", "Đã giao" ở cột "Xử lý" trong khi đề chỉ cho 4 cách | Soát độc lập bước 2 (V1) | Đổi thành giả định G-22..G-25 |
| L-09 | 2026-11-01 | 2 (PREMISE S-06) | Claude tin lời agent rằng `api-conventions.md` cho bỏ trống mã chống ghi trùng; mở file thì bản hiện tại đã đúng, chỉ còn câu ghi chú cũ ở TECH SCR-09 (tái phạm "nhận nguồn không kiểm") | Soát độc lập bước 2 (N3) | Viết lại S-06 trỏ đúng chỗ |
| L-10 | 2026-11-01 | 2 (sửa theo soát) | Claude thử cổng email bằng một commit giả rồi xoá bằng `git reset --hard`, làm mất các sửa đổi chưa commit của `PREMISE.md` | Kiểm số dòng PREMISE ngay sau lệnh | Khôi phục từ bản sao trong scratchpad và chạy lại script sửa; bài học: không dùng `reset --hard` khi còn thay đổi chưa commit, xoá commit thử bằng `reset --soft` |
| L-11 | 2026-11-01 | 0..1 (đẩy repo) | Commit lên repo public mang email công ty của người dùng; cổng máy chỉ quét file nên không bắt được | Soát độc lập bước 2 | Đổi email noreply, viết lại commit (D5-18); cổng thêm kiểm email commit |
| L-12 | 2026-11-01 | 2 (sửa lượt 1) | Claude thêm sub thiết kế hàng loạt bằng script mà không kiểm story đã có sub thiết kế do agent tạo, sinh 2 cặp trùng (E05-S05, E07-S05) | Soát lượt 2 (R2-V2) | Bỏ E05-S05-T07, E07-S05-T08 |
| L-13 | 2026-11-01 | 2 (sửa lượt 1) | Sửa cờ máy hiện trường (V6) chỉ ở tiêu chí của E03-S04, không lan sang mô tả, lá chặn quyền và bảng ở đợt 10a (tái phạm "sửa một chỗ không lan"); còn sót một chỗ "15 câu" trong JSON (tái phạm N1) | Soát lượt 2 (R2-V1, R2-N1) | Viết lại mô tả, tiêu chí E03-S04-T02, T03, E02-S10-T01; sửa E18-S05 |
| L-14 | 2026-11-01 | 2 (sửa lượt 2) | Script phân loại sub thiết kế "đọc / ghi" theo chữ trong tiêu đề lá code, xếp nhầm 4 story có ghi (E03-S04, E04-S08, E06-S07, E15-S06) vào loại đọc | Claude liệt kê và đọc lại 19 mục loại đọc trước khi trình | Sửa 4 mục về tiêu chí ghi |
| L-15 | 2026-11-01 | 2 (sửa lượt 2) | Phân loại sub thiết kế đọc / ghi theo chữ ở tiêu đề lá code, không đọc tiêu chí ghi của story: còn 3 mục xếp sai sau khi đã sửa tay 4 mục | Soát lượt 3 (R3-N1) | Sửa 3 mục |
| L-16 | 2026-11-01 | 2 (sửa lượt 2) | Sửa S-07 ở lá nhưng không lan sang issue cha E02-S10 và mã dẫn của các lá (tái phạm "sửa không lan" lần thứ ba trong bước 2) | Soát lượt 3 (R3-N2) | Lan S-07, thêm N-26 |
| L-17 | 2026-11-02 | 4 | Bản nháp `estimate.md` viết "63 việc độ tin thấp phần lớn là việc làm rõ với khách" mà chưa đếm; đếm thật chỉ 1 việc làm rõ, 40 việc thuộc 9 màn chưa có spec (tái phạm "số không có lệnh đếm" của LAB-4) | Tác giả tự đếm trước khi commit | Sửa theo số đếm, ghi lệnh đếm kèm câu |
| L-18 | 2026-11-02 | 4 | Giao 5 lô chấm SWP cho agent `sun-estimate-worker` mà không kiểm agent đó có quyền đọc file; cả 5 lô trả về rỗng, mất một lượt chạy | 5 agent tự báo BLOCKED | Chạy lại bằng agent thường, ghi chỗ lệch quy trình vào caveats của báo cáo và D5-21 |
| L-19 | 2026-11-02 | 5 | Viết lý do so LAB-1 "LAB-1 không có dòng sửa lỗi UAT riêng" mà không đọc lại LAB-1: bỏ sót T-06 (16 MD) và phần sửa lỗi trong U-01, tổng so lệch cách tính | Soát độc lập bước 5 | Thêm hai khung T-06, U-01 vào bảng thành phần (D5-23) |
| L-20 | 2026-11-02 | 5 | Gán dòng PREMISE sai epic trong bảng so LAB-1 và bảng epic: S-03 cho E09 (đúng là E05-S05), G-22 cho E10 (đúng là E04-S09, E07-S07) (tái phạm dẫn mã không kiểm nguồn của LAB-4) | Soát độc lập bước 5, đối chiếu cột issue chịu ảnh hưởng của PREMISE | Sửa mã dẫn ở mục 4, 5 |
| L-21 | 2026-11-02 | 5 | Script quy giờ dùng hàm làm tròn mặc định của Python (tròn nửa về chẵn, sai số số thực): 21 việc lệch 0,1 giờ so với tính tay | Soát độc lập bước 5 tính tay #72, #439 | Đổi sang làm tròn kiểu thường bằng Decimal, ghi lại Project (D5-23) |
| L-22 | 2026-11-02 | 6 | Script giả lập bản đầu bắt mỗi người làm đúng thứ tự cam kết: FE-B đứng chờ việc bị chặn, 0 giờ cả sprint trong khi có việc không phụ thuộc | Tác giả soát phân bổ giờ theo vai | Mỗi lượt lấy việc sẵn sàng sớm nhất; rút số ngẫu nhiên trước theo thứ tự cố định |
| L-23 | 2026-11-02 | 6 | Script giả lập không cho việc lá thừa hưởng phụ thuộc của story cha: việc dựng môi trường (E01-S02) được tính Closed khi khách chưa cấp tài khoản (E01-S01) | Tác giả đối chiếu `customer_wait` của E01-S01 | Lấy phụ thuộc của mọi cấp cha; thêm bước kéo việc cho người trống; dọn 3 việc lần ghi trước khỏi Sprint 1 trên Project |
| L-24 | 2026-11-02 | 6 | Bản nháp báo cáo viết "nền dữ liệu migration đợt 1 tới 10 xong cả 30 SWP" (thật: 9 việc đợt 1, 2, một phần 10a) và "đường còn lại đi ngang hai ngày cuối" (thật: vẫn giảm) (tái phạm "viết trước, đếm sau") | Tác giả đối chiếu file giả lập trước khi commit | Sửa câu theo số đếm |
| L-25 | 2026-11-02 | 6 | Giả lập dùng `depends_on` như đủ, trong khi backlog bước 2 không khai việc kiểm thử chờ việc làm mã và FE chờ BE cùng story: 14 việc (40 SWP) Closed vô lý, báo cáo kết luận "đi gần đúng kế hoạch" (tô hồng do tin kết quả máy, không soát theo nghĩa nghiệp vụ) | Soát độc lập bước 6 | Bổ sung 310 phụ thuộc vào backlog và GitHub, chạy lại giả lập (D5-25) |
| L-26 | 2026-11-02 | 6 | Hành động rủi ro đặt ngưỡng "nếu tốc độ vẫn dưới 174 SWP" trong khi chính số đã tính cho thấy ở 174 SWP vẫn trễ mốc (kết luận không theo số) | Soát độc lập bước 6 | Hành động mới: báo ngay, đưa hai phương án tăng người hoặc dời mốc |
| L-27 | 2026-11-02 | 6 | Giả lập để người bị chặn ngồi chờ thay vì kéo việc sẵn sàng làm trước: BE dùng một nửa năng lực khi backlog còn 12 việc sẵn sàng | Tác giả đếm việc sẵn sàng theo vai | Kéo việc khi việc cam kết tiếp theo phải chờ từ 1 ngày |
| L-28 | 2026-11-02 | 6 | Khi sửa theo lượt 1 chỉ áp 2 trong 3 luật thứ tự đã nêu, bỏ luật "việc trên staging chờ dựng môi trường": #214, chính việc lượt 1 nêu đích danh, vẫn Closed (tái phạm sửa không đủ, không kiểm lại đúng ví dụ đã nêu) | Soát độc lập bước 6 lượt 2 | Thêm luật 4 và luật giao diện chờ thiết kế (D5-26) |
| L-29 | 2026-11-02 | 6 | Phương án gửi khách tính ở năng lực 174 SWP mà đội chưa từng đạt, không ghi cơ sở (tái phạm kết luận không theo số đã đo) | Soát độc lập bước 6 lượt 2 | Ghi theo khoảng từ tốc độ đo được tới năng lực đủ, kèm cách tính |
| L-30 | 2026-11-02 | 7 | PREMISE S-01 ghi đợt migration 9 thuộc "epic Nền dữ liệu" trong khi dữ liệu đặt ở E11-S01 (tên E02 ghi rõ "đợt 1..8 và đợt 10"); ba lượt soát bước 2 và bước 1 không bắt | Tác giả đối chiếu khi làm bảng spec → epic cho README | Sửa ô issue bị ảnh hưởng của S-01, gắn link |
| L-31 | 2026-11-02 | 7 | Bảng epic mục 1.6 của `task-breakdown.md` (bước 2) thiếu A32 và 9 mã N (N-05..09, N-11..13, N-19); README chép lại nên thiếu theo (tái phạm chép bảng tóm tắt không đối chiếu danh sách mã đầy đủ). Người soát bước 7 chỉ bắt A32 | Soát độc lập bước 7 (A32); tác giả đếm đủ A1..A53, N-01..N-25 trên cả hai bảng | Bổ sung 10 mã vào cả hai bảng, đếm lại còn thiếu 0 |
| L-32 | 2026-11-02 | 8 | AI-report viết "mỗi bước có agent con soát độc lập" trong khi bước 0, 1, 3, 4 chỉ có agent chính tự soát; đếm kênh phát hiện 15/12 thay vì 16/11; viết "đọc ngược bắt được lần ghi dở" khi chưa lần nào bắt (tái phạm viết trước khi đọc nguồn, nhận vượt bằng chứng) | Soát độc lập bước 8, đối chiếu dòng "Người soát" của docs/lab5/reviews/step-00..04 | Ghi đúng các bước có soát độc lập, sửa số đếm, viết lại câu theo việc đã xảy ra |
| L-33 | 2026-11-02 | 8 | Mô tả script không khớp mã: gán việc ghi Estimated time lên Project cho `convert-story-points-to-hours.py`; ghi Scope, Complexity "cho 792 mục" trong khi script chỉ ghi cho 654 việc lá | Soát độc lập bước 8, đọc mã hai script | Sửa câu mục 1 theo mã |
| L-34 | 2026-11-02 | 5, 6 | So LAB-1 chỉ theo tổng (+7,5%) nên che chỗ vượt 52% của giai đoạn xây dựng; báo cáo lấy chỗ nghẽn của Sprint 1 (BE, TL) làm chẩn đoán cho cả dự án, trong khi theo giờ còn lại thì BE, QA, Design thiếu người nhiều nhất (kết luận không theo số đã có) | Soát độc lập theo 9 vai trước khi nộp (vai PM) | Thêm bảng so theo giai đoạn và theo vai vào `estimate.md` mục 5, phương án tăng người ghi theo vai |
| L-35 | 2026-11-02 | 2, 6 | 16/18 issue làm rõ không nối tới issue chịu ảnh hưởng, không có hạn trả lời; 7 câu Closed trong giả lập mà không ghi câu trả lời, vẫn mang nhãn chờ khách | Soát độc lập theo 9 vai trước khi nộp (vai BrSE) | `scripts/record-clarification-follow-up.py`: ghi issue chịu ảnh hưởng, hạn, câu trả lời giả lập, gỡ nhãn; cập nhật thân issue |
| L-36 | 2026-11-02 | 1..7 | File nộp dẫn mã sổ quyết định và mã báo cáo soát (D5-xx, V6, N3) nằm ngoài repo, người chấm không kiểm được; spec SCR-25 mà backlog dựa nhiều nhất chỉ ở repo private | Soát độc lập theo 9 vai trước khi nộp (vai người chấm) | Thay mã bằng lý do ngắn; thêm tóm tắt SCR-25 tự viết ở `spec-summary/`, trỏ từ PREMISE S-01 |
| L-37 | 2026-11-02 | Sửa trước nộp | Chạy script cập nhật thân issue rồi chuyển đầu ra sang lệnh `head -1`: script bị dừng sau dòng in đầu, không cập nhật issue nào mà vẫn tưởng xong | Lần chạy kiểm thứ hai vẫn báo 17 issue cũ; so thân một issue với bản sinh từ file | Chạy lại không cắt đầu ra, kiểm còn 0 issue cũ |
| L-38 | 2026-11-02 | Sửa trước nộp | Phương án (a) ghi "tăng đội từ Sprint 3" nhưng số người theo vai lấy từ bảng tính cho 7 sprint bắt đầu Sprint 2 (4 người thay vì 4,7); ô BA ghi 0 người khi còn thiếu 0,02 (kết luận không theo đúng mốc đã nêu) | Kiểm độc lập phần sửa theo vai | Tính lại theo 6 sprint cho người vào từ Sprint 3: 4,7 người (BE 2,5, QA 1,3, FE 0,5, Design 0,3); ghi chú BA |
| L-39 | 2026-11-02 | Sửa trước nộp | Script theo dõi issue làm rõ chỉ đặt Due Date cho việc ngoài sprint: 3 câu còn chờ trong Sprint 1 (#83, #135, #138) mang Due Date cuối sprint, lệch hạn trả lời ghi trong thân issue | Kiểm độc lập phần sửa theo vai, so Project với JSON | Đặt Due Date cho mọi câu chưa trả lời; script ghi sprint dùng hạn trả lời cho việc Pending |
| L-40 | 2026-11-02 | Sửa trước nộp | Tóm tắt SCR-25 viết rộng hơn nguồn: "file kế toán đọc từ các bảng này" (thật: chỉ khoản trả, chênh lệch không vào file kế toán, SCR-30 chưa có spec) và ghi "đếm ngày lịch" như đã chốt (thật: giả định chờ Q4-61) | Kiểm độc lập phần sửa theo vai, đối chiếu spec gốc | Sửa hai câu theo nguồn |

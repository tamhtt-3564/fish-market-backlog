# Chia việc: từ bộ spec LAB-4 tới backlog trên GitHub Project

Đầu vào: bộ spec LAB-4 bản `21bbe4b` và các giả định, hướng chốt ở `PREMISE.md`. Phạm vi: mọi việc kỹ thuật (D5-11); quản lý dự án và buffer không thành issue.

## 1. Nguyên tắc chia task

### 1.1 Ba tầng trên Project, theo mẫu Project của công ty

Project dựng theo cấu trúc mẫu quản lý dự án của công ty (bộ nhãn `type:*`, 18 trạng thái, các trường Story Point, Estimated time, Target version, Priority, Start Date, Due Date). Loại việc phân biệt bằng nhãn `type:*`.

| Tầng | Là gì | Nhãn loại | Ví dụ |
|---|---|---|---|
| Epic | Một vùng nghiệp vụ hoặc một mảng kỹ thuật dùng chung; là issue cha, không tự có việc làm | `type:epic` | Epic 完納奨励金 |
| Issue | Một chức năng người dùng thấy được (hàm ghi có TECH, màn đọc, việc nền) | `type:story` | Chạy tính 完納奨励金 của một tháng (A51) |
| Issue | Việc kỹ thuật trọn vẹn không phải chức năng người dùng: đợt migration, cấu hình nền tảng, runbook, đào tạo | `type:devtask` (migration) hoặc `type:operation` | Migration đợt 9; cấu hình giám sát uptime |
| Issue | Viết spec cho màn chưa có spec | `type:documentation` | Viết spec SCR-22 |
| Issue | Câu khách cần làm rõ | `type:investigation` | Làm rõ Q4-59 |
| Sub-issue | Một lớp việc của story, một người làm, **tối đa 2 ngày công (14 giờ)** | `type:uidesign`, `type:devtask` (kèm `team:backend`, `team:frontend`, `team:infrastructure`), `type:testdesign`, `type:testexecution` | Hàm DB `calculate_incentive_period` kèm test; route A51; khối nút chạy tính trên SCR-25; ca kiểm thử SCR-25 |

Epic, issue, sub-issue nối bằng quan hệ cha con có sẵn của GitHub (trường `Parent issue`, `Sub-issues progress`).

Trường đề yêu cầu: điểm SWP đã review ghi ở **Story Point**, giờ ước lượng ở **Estimated time**, sprint ở **Target version** (trường kiểu Iteration). Trường thêm ngoài mẫu: `Phụ trách (giả định)` (Assignees chỉ gán được tài khoản thật), `Scope`, `Complexity` (kết quả chấm của skill SWP). Nhãn thêm ngoài mẫu: `chờ khách`, `độ tin thấp`.

### 1.2 Ai làm gì (trường `Phụ trách (giả định)`)

| Vai | Phụ trách loại việc nào |
|---|---|
| BA-A | Viết spec cho 9 màn chưa có spec (G-02) |
| Design-A | Thiết kế giao diện cho màn mới hoặc đổi nhiều so với prototype |
| TL-A | Thiết kế kỹ thuật ngắn (sub `documentation`, 2 tới 4 giờ) cho mọi story của 23 màn không có TECH: 14 màn chỉ có wireframe (G-03) và 9 màn chưa có spec (G-02); review code, duyệt migration |
| BE-A, BE-B | Hàm DB, API, migration, việc nền |
| FE-A, FE-B | Giao diện |
| QA-A | Viết ca kiểm thử từ spec, kiểm từng issue trước khi Closed (trạng thái QA Testing), kiểm thử hệ thống (E18) |
| Infra-A | Hạ tầng, cấu hình nền tảng, giám sát, runbook |
| BrSE-A | 18 issue làm rõ với khách: dịch câu hỏi, gửi, ghi câu trả lời |
| PM-A | Không có issue: lập sprint, theo dõi tiến độ, báo cáo khách (công tính ở `estimate.md`) |

Giờ của issue làm rõ (BrSE-A) chỉ để theo dõi, **không cộng** vào tổng so với LAB-1, vì LAB-1 đã tính chung trong phần PM + BrSE.

### 1.3 Việc của phía khách

Khách không có issue, nhưng nhiều issue phải chờ khách: trả lời 18 câu Q4, cấp tài khoản dịch vụ (G-08), cấp file xuất của hệ thống cũ (Q4-24), duyệt version quy tắc, làm UAT.
Issue bị chặn gắn nhãn **`chờ khách`**; phần mô tả ghi khách cần làm gì và hạn cần có. Các issue này là nguồn chính của bảng rủi ro trễ ở `progress-report.md`.

Đào tạo IT của khách và hỗ trợ UAT (chuẩn bị dữ liệu, giải đáp, phân loại lỗi) là issue ở E19. Lỗi UAT tìm ra thành issue `type:uatbug` khi phát sinh, không có sẵn trong backlog; giờ dự phòng cho việc sửa lỗi UAT ghi ở `estimate.md`. Việc người dùng của khách làm UAT không vào backlog.

### 1.4 Chia tới đâu thì dừng

- Một issue mà một người làm xong trong 2 ngày thì **không tách** sub-issue (ví dụ màn danh sách chỉ đọc dùng một API có sẵn).
- Issue lớn hơn 2 ngày thì tách sub-issue **theo lớp**: thiết kế giao diện (màn mới hoặc đổi nhiều); hàm DB và test của hàm; API route; giao diện; ca kiểm thử và kiểm của QA; kiểm thử đầu cuối khi luồng đi qua nhiều màn.
- Issue có giao diện hoặc API ghi rõ **vai trò người dùng hệ thống** (11 vai trò ở ma trận quyền LAB-4) nào được làm, vai trò nào bị chặn. Ca kiểm thử phải có vai bị chặn, và chặn phải ở hàm DB hoặc API, không chỉ ẩn nút (gồm tài khoản bên ngoài ROLE-PARTICIPANT-VIEW, PKT-11).
- Một lớp vẫn lớn hơn 2 ngày thì tách tiếp **theo nhánh nghiệp vụ** ghi ở TECH (ví dụ tính tạm và tính sau hạn; 相対 và せり), không tách theo file.
- Mỗi biến nghiệp vụ của 完納奨励金 (điều kiện được thưởng, hạn trả, công thức, version 料率, chênh lệch sau xác nhận, phần âm chuyển kỳ sau, khoản trả trùng) là ít nhất một issue hoặc sub-issue có tiêu chí xong riêng, không gộp.
- Chỗ khách chưa trả lời mà đổi nhiều khối lượng có **issue làm rõ** riêng (18 câu, `PREMISE.md` G-01a); chỗ còn lại làm theo mặc định LAB-4.
- Màn chưa có spec có **issue viết spec** riêng (G-02); issue xây dựng của màn đó gắn độ tin thấp.

### 1.5 Định nghĩa xong

Trạng thái đi theo mẫu. Việc xây dựng: `In Progress` → `In Review` (TL-A review code; trượt thì `Technical Review Failed`) → `QA Testing` (QA-A kiểm; trượt thì `QA Testing Failed`) → `QA Testing Passed` → `Closed`. Thiết kế giao diện, ca kiểm thử, tài liệu, vận hành: `In Progress` → `In Review` → `Review Passed (...)` hoặc `Review Failed (...)` → `Closed`. Chờ khách quá hạn thì `Pending`. Các bước UAT, `Ready for Delivery` dùng khi khách làm UAT, ngoài sprint giả lập.

| Loại | Xong khi |
|---|---|
| Thiết kế giao diện | Bản thiết kế khớp wireframe LAB-4 và quy ước nhập (nút cao tối thiểu 48 px); BA hoặc người dùng đại diện duyệt |
| Xây dựng (hàm DB, API, giao diện) | Test của lớp đó chạy xanh (hàm DB: đủ các phép kiểm và mã lỗi ở TECH; API: mã HTTP và mã lỗi ở API design; giao diện: nhãn, câu báo tiếng Nhật đúng bảng đã duyệt); thao tác ghi có dòng audit; vai trò bị chặn bị chặn ở hàm DB hoặc API; TL-A review và gộp code; QA-A kiểm theo ca kiểm thử viết từ spec, đạt trên staging |
| Ca kiểm thử | Ca kiểm thử phủ các nhánh, mã lỗi và vai trò bị chặn ghi ở spec, TECH; TL-A hoặc BA soát |
| Migration | Chạy được trên DB của đợt trước, backfill đúng nguồn, có script quay lui hoặc ghi rõ không quay lui được; prototype vẫn chạy sau đợt |
| Viết spec | Spec theo mẫu QC-01 như 11 màn đã có, qua soát và BA duyệt; SWP các issue xây dựng của màn được chấm lại |
| Làm rõ | Khách trả lời, câu trả lời ghi vào bảng Q4; issue chịu ảnh hưởng được sửa và ước lại |
| Hạ tầng, vận hành | Cấu hình hoặc runbook có trong repo, người thứ hai làm theo được |

### 1.6 Danh sách epic

| Mã | Epic | Nguồn chính |
|---|---|---|
| E01 | Hạ tầng và môi trường | Kiến trúc mục 8, ADR-002, ADR-018, C-17 |
| E02 | Nền dữ liệu (migration đợt 1..8 và đợt 10) | `api-design/_index.md`, DB design mục 6, G-04 |
| E03 | Đăng nhập, tài khoản, phân quyền | SCR-01, 02, 07, 08; A1..A5, N-01, N-02; ADR-006, 014, 019; PKT-11 |
| E04 | Người tham gia và tư cách tham gia | SCR-03..06; A6..A9, A15, N-03, N-04, N-25; ADR-011 |
| E05 | Tiếp nhận lô và 目利き | SCR-09..12; A10..A14; H-02 |
| E06 | Giao dịch 相対 / せり | SCR-13..16; A16..A20, A33, A34 |
| E07 | Giao nhận | SCR-17..19; A21..A25, A37 |
| E08 | Phiếu điều chỉnh và file đính kèm | SCR-23, 24; A29..A31, A35, A36, A45..A47 |
| E09 | Đối soát, khoá ngày, mở lại sổ, chốt kỳ | SCR-20, 21; A26..A28, A38..A40, N-24; ADR-009 |
| E10 | Version 業務規程 / 料率 | SCR-26, 27; A41..A44; ADR-012 |
| E11 | **完納奨励金** | SCR-25; A48..A53; đợt migration 9; Q4-55, 56, 57, 58, 59, 60, 61, 63, 64 |
| E12 | Báo cáo, in chứng từ, xuất kế toán | SCR-28..30; N-14, N-15; ADR-005, 007 |
| E13 | Thông báo và việc nền | SCR-31; N-16, N-17, N-23; ADR-004; G-05 |
| E14 | Mất mạng và đồng bộ | SCR-34; N-20, N-21; ADR-003 |
| E15 | Audit, lưu trữ, xoá theo hạn | SCR-32, 33; N-18; ADR-008, 015; H-03 |
| E16 | Tranh chấp | SCR-22; N-10 |
| E17 | Chuyển đổi dữ liệu và vùng lịch sử | ADR-017; C-16, C-19; N-22 |
| E18 | Kiểm thử hệ thống và phi chức năng | Kiến trúc mục 8, NFR, ma trận quyền (QT-xx) |
| E19 | Vận hành, đào tạo, hỗ trợ UAT, bàn giao | C-18, C-20; kiến trúc 8.1, 8.3; mục 1.3 |

## 2. Spec → issue

Bảng sinh từ dữ liệu backlog bằng `python scripts/render-spec-to-issue-table.py <thư mục specs LAB-4>`; cột Issue ghi mã mục, mỗi mã là link tới issue trên GitHub (gắn bằng `python scripts/link-backlog-keys-to-issues.py task-breakdown.md PREMISE.md`, số issue lấy ở `backlog/issue-numbers.json`). Đơn vị spec: 27 TECH, 34 màn, 10 đợt migration, 8 việc LAB-4 chuyển sang LAB-5. API, câu Q4, PKT, ADR đối chiếu ở bảng phủ của từng nhóm khi chia; mọi API đều nằm trong issue của TECH hoặc màn tương ứng (kiểm bằng lệnh: 53 mã A1..A53 và 25 mã N-01..N-25 đều có trong `spec_refs` hoặc tiêu đề của ít nhất một mục).

| Loại | Spec | Epic | Issue | Phần spec chưa thành issue và vì sao |
|---|---|---|---|---|
| TECH | SCR_05_UPSERT_PARTICIPANT_VALIDITY | E04, E17 | [E04-S03](https://github.com/tamhtt-3564/fish-market-backlog/issues/70), [E17-S03](https://github.com/tamhtt-3564/fish-market-backlog/issues/173) | Không |
| TECH | SCR_09_CREATE_LOT | E05 | [E05-S01](https://github.com/tamhtt-3564/fish-market-backlog/issues/77) | Không |
| TECH | SCR_12_RECORD_JUDGMENT | E05 | [E05-S04](https://github.com/tamhtt-3564/fish-market-backlog/issues/80) | Không |
| TECH | SCR_13_CONFIRM_AITAI_TRADE | E06 | [E06-S01](https://github.com/tamhtt-3564/fish-market-backlog/issues/85), [E06-S04](https://github.com/tamhtt-3564/fish-market-backlog/issues/88) | Không |
| TECH | SCR_13_DISCARD_TRADE_DRAFT | E06 | [E06-S03](https://github.com/tamhtt-3564/fish-market-backlog/issues/87) | Không |
| TECH | SCR_13_SAVE_TRADE_DRAFT | E06 | [E06-S03](https://github.com/tamhtt-3564/fish-market-backlog/issues/87), [E06-S04](https://github.com/tamhtt-3564/fish-market-backlog/issues/88) | Không |
| TECH | SCR_14_CONFIRM_SERI_TRADE | E06 | [E06-S02](https://github.com/tamhtt-3564/fish-market-backlog/issues/86), [E06-S04](https://github.com/tamhtt-3564/fish-market-backlog/issues/88) | Không |
| TECH | SCR_18_COMPLETE_DELIVERY | E07 | [E07-S03](https://github.com/tamhtt-3564/fish-market-backlog/issues/95) | Không |
| TECH | SCR_18_DECIDE_DELIVERY_HOLD | E07 | [E07-S04](https://github.com/tamhtt-3564/fish-market-backlog/issues/96) | Không |
| TECH | SCR_18_RECORD_DELIVERY | E07 | [E07-S02](https://github.com/tamhtt-3564/fish-market-backlog/issues/94), [E07-S05](https://github.com/tamhtt-3564/fish-market-backlog/issues/97) | Không |
| TECH | SCR_21_CLOSE_PERIOD | E09 | [E09-S01](https://github.com/tamhtt-3564/fish-market-backlog/issues/108), [E09-S06](https://github.com/tamhtt-3564/fish-market-backlog/issues/113), [E09-S12](https://github.com/tamhtt-3564/fish-market-backlog/issues/119) | Không |
| TECH | SCR_21_DECIDE_DAY_REOPEN | E09 | [E09-S05](https://github.com/tamhtt-3564/fish-market-backlog/issues/112) | Không |
| TECH | SCR_21_LOCK_BUSINESS_DAY | E05, E09 | [E05-S05](https://github.com/tamhtt-3564/fish-market-backlog/issues/81), [E09-S01](https://github.com/tamhtt-3564/fish-market-backlog/issues/108), [E09-S02](https://github.com/tamhtt-3564/fish-market-backlog/issues/109), [E09-S03](https://github.com/tamhtt-3564/fish-market-backlog/issues/110), [E09-S10](https://github.com/tamhtt-3564/fish-market-backlog/issues/117) | Không |
| TECH | SCR_21_REQUEST_DAY_REOPEN | E09 | [E09-S04](https://github.com/tamhtt-3564/fish-market-backlog/issues/111) | Không |
| TECH | SCR_23_CREATE_CORRECTION | E06, E08 | [E06-S07](https://github.com/tamhtt-3564/fish-market-backlog/issues/91), [E08-S01](https://github.com/tamhtt-3564/fish-market-backlog/issues/100), [E08-S04](https://github.com/tamhtt-3564/fish-market-backlog/issues/103), [E08-S08](https://github.com/tamhtt-3564/fish-market-backlog/issues/107) | Không |
| TECH | SCR_23_RESUBMIT_CORRECTION | E08 | [E08-S02](https://github.com/tamhtt-3564/fish-market-backlog/issues/101), [E08-S08](https://github.com/tamhtt-3564/fish-market-backlog/issues/107) | Không |
| TECH | SCR_23_UPLOAD_ATTACHMENT | E08 | [E08-S03](https://github.com/tamhtt-3564/fish-market-backlog/issues/102) | Không |
| TECH | SCR_24_DECIDE_CORRECTION | E08 | [E08-S06](https://github.com/tamhtt-3564/fish-market-backlog/issues/105), [E08-S08](https://github.com/tamhtt-3564/fish-market-backlog/issues/107) | Không |
| TECH | SCR_24_WITHDRAW_CORRECTION | E08 | [E08-S07](https://github.com/tamhtt-3564/fish-market-backlog/issues/106), [E08-S08](https://github.com/tamhtt-3564/fish-market-backlog/issues/107) | Không |
| TECH | SCR_25_CALCULATE_INCENTIVE_ADJUSTMENT | E11 | [E11-S04](https://github.com/tamhtt-3564/fish-market-backlog/issues/130), [E11-S07](https://github.com/tamhtt-3564/fish-market-backlog/issues/133) | Không |
| TECH | SCR_25_CONFIRM_INCENTIVE_RESULT | E11 | [E11-S04](https://github.com/tamhtt-3564/fish-market-backlog/issues/130), [E11-S06](https://github.com/tamhtt-3564/fish-market-backlog/issues/132) | Không |
| TECH | SCR_25_IMPORT_PAYMENT_CSV | E11 | [E11-S03](https://github.com/tamhtt-3564/fish-market-backlog/issues/129), [E11-S15](https://github.com/tamhtt-3564/fish-market-backlog/issues/141) | Không |
| TECH | SCR_25_RECORD_PAYMENT | E11 | [E11-S02](https://github.com/tamhtt-3564/fish-market-backlog/issues/128) | Không |
| TECH | SCR_25_RUN_INCENTIVE_CALCULATION | E11 | [E11-S04](https://github.com/tamhtt-3564/fish-market-backlog/issues/130), [E11-S05](https://github.com/tamhtt-3564/fish-market-backlog/issues/131) | Không |
| TECH | SCR_27_DECIDE_RULE_VERSION | E10 | [E10-S06](https://github.com/tamhtt-3564/fish-market-backlog/issues/125) | Không |
| TECH | SCR_27_SAVE_RULE_VERSION_DRAFT | E10 | [E10-S04](https://github.com/tamhtt-3564/fish-market-backlog/issues/123) | Không |
| TECH | SCR_27_SUBMIT_RULE_VERSION | E10 | [E10-S05](https://github.com/tamhtt-3564/fish-market-backlog/issues/124) | Không |
| Màn | SCR-01 | E03 | [E03-S02](https://github.com/tamhtt-3564/fish-market-backlog/issues/57), [E03-S03](https://github.com/tamhtt-3564/fish-market-backlog/issues/58), [E03-S12](https://github.com/tamhtt-3564/fish-market-backlog/issues/67) | Không |
| Màn | SCR-02 | E03, E13, E14 | [E03-S04](https://github.com/tamhtt-3564/fish-market-backlog/issues/59), [E03-S05](https://github.com/tamhtt-3564/fish-market-backlog/issues/60), [E03-S12](https://github.com/tamhtt-3564/fish-market-backlog/issues/67), [E13-S04](https://github.com/tamhtt-3564/fish-market-backlog/issues/157), [E14-S01](https://github.com/tamhtt-3564/fish-market-backlog/issues/160) | Không |
| Màn | SCR-03 | E04 | [E04-S01](https://github.com/tamhtt-3564/fish-market-backlog/issues/68) | Không |
| Màn | SCR-04 | E04 | [E04-S02](https://github.com/tamhtt-3564/fish-market-backlog/issues/69) | Không |
| Màn | SCR-05 | E04 | [E04-S03](https://github.com/tamhtt-3564/fish-market-backlog/issues/70), [E04-S09](https://github.com/tamhtt-3564/fish-market-backlog/issues/76) | Không |
| Màn | SCR-06 | E04 | [E04-S05](https://github.com/tamhtt-3564/fish-market-backlog/issues/72), [E04-S06](https://github.com/tamhtt-3564/fish-market-backlog/issues/73), [E04-S07](https://github.com/tamhtt-3564/fish-market-backlog/issues/74), [E04-S08](https://github.com/tamhtt-3564/fish-market-backlog/issues/75) | Không |
| Màn | SCR-07 | E03 | [E03-S06](https://github.com/tamhtt-3564/fish-market-backlog/issues/61), [E03-S07](https://github.com/tamhtt-3564/fish-market-backlog/issues/62) | Không |
| Màn | SCR-08 | E03 | [E03-S07](https://github.com/tamhtt-3564/fish-market-backlog/issues/62), [E03-S08](https://github.com/tamhtt-3564/fish-market-backlog/issues/63), [E03-S09](https://github.com/tamhtt-3564/fish-market-backlog/issues/64) | Không |
| Màn | SCR-09 | E05, E07, E14 | [E05-S01](https://github.com/tamhtt-3564/fish-market-backlog/issues/77), [E07-S06](https://github.com/tamhtt-3564/fish-market-backlog/issues/98), [E14-S01](https://github.com/tamhtt-3564/fish-market-backlog/issues/160) | Không |
| Màn | SCR-10 | E05 | [E05-S02](https://github.com/tamhtt-3564/fish-market-backlog/issues/78) | Không |
| Màn | SCR-11 | E05 | [E05-S03](https://github.com/tamhtt-3564/fish-market-backlog/issues/79), [E05-S05](https://github.com/tamhtt-3564/fish-market-backlog/issues/81) | Không |
| Màn | SCR-12 | E05, E07 | [E05-S04](https://github.com/tamhtt-3564/fish-market-backlog/issues/80), [E07-S06](https://github.com/tamhtt-3564/fish-market-backlog/issues/98) | Không |
| Màn | SCR-13 | E04, E06, E07 | [E04-S04](https://github.com/tamhtt-3564/fish-market-backlog/issues/71), [E06-S01](https://github.com/tamhtt-3564/fish-market-backlog/issues/85), [E06-S03](https://github.com/tamhtt-3564/fish-market-backlog/issues/87), [E06-S04](https://github.com/tamhtt-3564/fish-market-backlog/issues/88), [E07-S06](https://github.com/tamhtt-3564/fish-market-backlog/issues/98) | Không |
| Màn | SCR-14 | E04, E06, E07 | [E04-S04](https://github.com/tamhtt-3564/fish-market-backlog/issues/71), [E06-S01](https://github.com/tamhtt-3564/fish-market-backlog/issues/85), [E06-S02](https://github.com/tamhtt-3564/fish-market-backlog/issues/86), [E06-S03](https://github.com/tamhtt-3564/fish-market-backlog/issues/87), [E06-S04](https://github.com/tamhtt-3564/fish-market-backlog/issues/88), [E07-S06](https://github.com/tamhtt-3564/fish-market-backlog/issues/98) | Không |
| Màn | SCR-15 | E06, E17 | [E06-S05](https://github.com/tamhtt-3564/fish-market-backlog/issues/89), [E17-S05](https://github.com/tamhtt-3564/fish-market-backlog/issues/175) | Không |
| Màn | SCR-16 | E06, E17 | [E06-S06](https://github.com/tamhtt-3564/fish-market-backlog/issues/90), [E06-S07](https://github.com/tamhtt-3564/fish-market-backlog/issues/91), [E06-S08](https://github.com/tamhtt-3564/fish-market-backlog/issues/92), [E17-S05](https://github.com/tamhtt-3564/fish-market-backlog/issues/175) | Không |
| Màn | SCR-17 | E07 | [E07-S01](https://github.com/tamhtt-3564/fish-market-backlog/issues/93) | Không |
| Màn | SCR-18 | E07, E14 | [E07-S02](https://github.com/tamhtt-3564/fish-market-backlog/issues/94), [E07-S03](https://github.com/tamhtt-3564/fish-market-backlog/issues/95), [E07-S04](https://github.com/tamhtt-3564/fish-market-backlog/issues/96), [E07-S06](https://github.com/tamhtt-3564/fish-market-backlog/issues/98), [E07-S07](https://github.com/tamhtt-3564/fish-market-backlog/issues/99), [E14-S01](https://github.com/tamhtt-3564/fish-market-backlog/issues/160) | Không |
| Màn | SCR-19 | E07, E14 | [E07-S05](https://github.com/tamhtt-3564/fish-market-backlog/issues/97), [E07-S06](https://github.com/tamhtt-3564/fish-market-backlog/issues/98), [E14-S01](https://github.com/tamhtt-3564/fish-market-backlog/issues/160) | Không |
| Màn | SCR-20 | E09 | [E09-S07](https://github.com/tamhtt-3564/fish-market-backlog/issues/114), [E09-S08](https://github.com/tamhtt-3564/fish-market-backlog/issues/115), [E09-S11](https://github.com/tamhtt-3564/fish-market-backlog/issues/118) | Không |
| Màn | SCR-21 | E09, E11 | [E09-S01](https://github.com/tamhtt-3564/fish-market-backlog/issues/108), [E09-S02](https://github.com/tamhtt-3564/fish-market-backlog/issues/109), [E09-S03](https://github.com/tamhtt-3564/fish-market-backlog/issues/110), [E09-S04](https://github.com/tamhtt-3564/fish-market-backlog/issues/111), [E09-S05](https://github.com/tamhtt-3564/fish-market-backlog/issues/112), [E09-S06](https://github.com/tamhtt-3564/fish-market-backlog/issues/113), [E09-S10](https://github.com/tamhtt-3564/fish-market-backlog/issues/117), [E09-S11](https://github.com/tamhtt-3564/fish-market-backlog/issues/118), [E09-S12](https://github.com/tamhtt-3564/fish-market-backlog/issues/119), [E11-S08](https://github.com/tamhtt-3564/fish-market-backlog/issues/134) | Không |
| Màn | SCR-22 | E16 | [E16-S01](https://github.com/tamhtt-3564/fish-market-backlog/issues/2), [E16-S03](https://github.com/tamhtt-3564/fish-market-backlog/issues/4), [E16-S04](https://github.com/tamhtt-3564/fish-market-backlog/issues/5) | Không |
| Màn | SCR-23 | E08, E09 | [E08-S01](https://github.com/tamhtt-3564/fish-market-backlog/issues/100), [E08-S02](https://github.com/tamhtt-3564/fish-market-backlog/issues/101), [E08-S03](https://github.com/tamhtt-3564/fish-market-backlog/issues/102), [E08-S08](https://github.com/tamhtt-3564/fish-market-backlog/issues/107), [E09-S11](https://github.com/tamhtt-3564/fish-market-backlog/issues/118) | Không |
| Màn | SCR-24 | E08, E09, E11 | [E08-S03](https://github.com/tamhtt-3564/fish-market-backlog/issues/102), [E08-S05](https://github.com/tamhtt-3564/fish-market-backlog/issues/104), [E08-S06](https://github.com/tamhtt-3564/fish-market-backlog/issues/105), [E08-S07](https://github.com/tamhtt-3564/fish-market-backlog/issues/106), [E08-S08](https://github.com/tamhtt-3564/fish-market-backlog/issues/107), [E09-S11](https://github.com/tamhtt-3564/fish-market-backlog/issues/118), [E11-S08](https://github.com/tamhtt-3564/fish-market-backlog/issues/134) | Không |
| Màn | SCR-25 | E11, E12 | [E11-S02](https://github.com/tamhtt-3564/fish-market-backlog/issues/128), [E11-S03](https://github.com/tamhtt-3564/fish-market-backlog/issues/129), [E11-S04](https://github.com/tamhtt-3564/fish-market-backlog/issues/130), [E11-S05](https://github.com/tamhtt-3564/fish-market-backlog/issues/131), [E11-S06](https://github.com/tamhtt-3564/fish-market-backlog/issues/132), [E11-S07](https://github.com/tamhtt-3564/fish-market-backlog/issues/133), [E11-S08](https://github.com/tamhtt-3564/fish-market-backlog/issues/134), [E11-S09](https://github.com/tamhtt-3564/fish-market-backlog/issues/135), [E11-S10](https://github.com/tamhtt-3564/fish-market-backlog/issues/136), [E11-S11](https://github.com/tamhtt-3564/fish-market-backlog/issues/137), [E11-S12](https://github.com/tamhtt-3564/fish-market-backlog/issues/138), [E11-S13](https://github.com/tamhtt-3564/fish-market-backlog/issues/139), [E11-S14](https://github.com/tamhtt-3564/fish-market-backlog/issues/140), [E11-S15](https://github.com/tamhtt-3564/fish-market-backlog/issues/141), [E11-S16](https://github.com/tamhtt-3564/fish-market-backlog/issues/142), [E11-S17](https://github.com/tamhtt-3564/fish-market-backlog/issues/143), [E12-S09](https://github.com/tamhtt-3564/fish-market-backlog/issues/152) | Không |
| Màn | SCR-26 | E10 | [E10-S01](https://github.com/tamhtt-3564/fish-market-backlog/issues/120), [E10-S02](https://github.com/tamhtt-3564/fish-market-backlog/issues/121), [E10-S03](https://github.com/tamhtt-3564/fish-market-backlog/issues/122) | Không |
| Màn | SCR-27 | E10, E11 | [E10-S03](https://github.com/tamhtt-3564/fish-market-backlog/issues/122), [E10-S04](https://github.com/tamhtt-3564/fish-market-backlog/issues/123), [E10-S05](https://github.com/tamhtt-3564/fish-market-backlog/issues/124), [E10-S06](https://github.com/tamhtt-3564/fish-market-backlog/issues/125), [E10-S07](https://github.com/tamhtt-3564/fish-market-backlog/issues/126), [E11-S08](https://github.com/tamhtt-3564/fish-market-backlog/issues/134) | Không |
| Màn | SCR-28 | E12 | [E12-S01](https://github.com/tamhtt-3564/fish-market-backlog/issues/144), [E12-S05](https://github.com/tamhtt-3564/fish-market-backlog/issues/148), [E12-S06](https://github.com/tamhtt-3564/fish-market-backlog/issues/149) | Không |
| Màn | SCR-29 | E12 | [E12-S02](https://github.com/tamhtt-3564/fish-market-backlog/issues/145), [E12-S07](https://github.com/tamhtt-3564/fish-market-backlog/issues/150) | Không |
| Màn | SCR-30 | E12 | [E12-S03](https://github.com/tamhtt-3564/fish-market-backlog/issues/146), [E12-S09](https://github.com/tamhtt-3564/fish-market-backlog/issues/152), [E12-S10](https://github.com/tamhtt-3564/fish-market-backlog/issues/153) | Không |
| Màn | SCR-31 | E13, E19 | [E13-S05](https://github.com/tamhtt-3564/fish-market-backlog/issues/158), [E13-S06](https://github.com/tamhtt-3564/fish-market-backlog/issues/159), [E19-S05](https://github.com/tamhtt-3564/fish-market-backlog/issues/190) | Không |
| Màn | SCR-32 | E15 | [E15-S01](https://github.com/tamhtt-3564/fish-market-backlog/issues/164) | Không |
| Màn | SCR-33 | E15, E19 | [E15-S02](https://github.com/tamhtt-3564/fish-market-backlog/issues/165), [E15-S04](https://github.com/tamhtt-3564/fish-market-backlog/issues/167), [E15-S06](https://github.com/tamhtt-3564/fish-market-backlog/issues/169), [E19-S05](https://github.com/tamhtt-3564/fish-market-backlog/issues/190) | Không |
| Màn | SCR-34 | E14, E19 | [E14-S01](https://github.com/tamhtt-3564/fish-market-backlog/issues/160), [E14-S02](https://github.com/tamhtt-3564/fish-market-backlog/issues/161), [E14-S03](https://github.com/tamhtt-3564/fish-market-backlog/issues/162), [E14-S04](https://github.com/tamhtt-3564/fish-market-backlog/issues/163), [E19-S05](https://github.com/tamhtt-3564/fish-market-backlog/issues/190) | Không |
| Đợt migration | W1 | E01, E02, E14 | [E01-S02](https://github.com/tamhtt-3564/fish-market-backlog/issues/38), [E01-S04](https://github.com/tamhtt-3564/fish-market-backlog/issues/40), [E02-S01](https://github.com/tamhtt-3564/fish-market-backlog/issues/46), [E14-S04](https://github.com/tamhtt-3564/fish-market-backlog/issues/163) | Không |
| Đợt migration | W2 | E02, E04 | [E02-S02](https://github.com/tamhtt-3564/fish-market-backlog/issues/47), [E04-S01](https://github.com/tamhtt-3564/fish-market-backlog/issues/68), [E04-S03](https://github.com/tamhtt-3564/fish-market-backlog/issues/70), [E04-S09](https://github.com/tamhtt-3564/fish-market-backlog/issues/76) | Không |
| Đợt migration | W3 | E02, E05 | [E02-S03](https://github.com/tamhtt-3564/fish-market-backlog/issues/48), [E05-S01](https://github.com/tamhtt-3564/fish-market-backlog/issues/77), [E05-S02](https://github.com/tamhtt-3564/fish-market-backlog/issues/78), [E05-S03](https://github.com/tamhtt-3564/fish-market-backlog/issues/79), [E05-S04](https://github.com/tamhtt-3564/fish-market-backlog/issues/80), [E05-S06](https://github.com/tamhtt-3564/fish-market-backlog/issues/82) | Không |
| Đợt migration | W4 | E02, E04, E06, E07 | [E02-S04](https://github.com/tamhtt-3564/fish-market-backlog/issues/49), [E04-S04](https://github.com/tamhtt-3564/fish-market-backlog/issues/71), [E06-S01](https://github.com/tamhtt-3564/fish-market-backlog/issues/85), [E06-S02](https://github.com/tamhtt-3564/fish-market-backlog/issues/86), [E06-S03](https://github.com/tamhtt-3564/fish-market-backlog/issues/87), [E06-S04](https://github.com/tamhtt-3564/fish-market-backlog/issues/88), [E06-S05](https://github.com/tamhtt-3564/fish-market-backlog/issues/89), [E07-S05](https://github.com/tamhtt-3564/fish-market-backlog/issues/97) | Không |
| Đợt migration | W5 | E02, E07 | [E02-S05](https://github.com/tamhtt-3564/fish-market-backlog/issues/50), [E07-S01](https://github.com/tamhtt-3564/fish-market-backlog/issues/93), [E07-S02](https://github.com/tamhtt-3564/fish-market-backlog/issues/94), [E07-S03](https://github.com/tamhtt-3564/fish-market-backlog/issues/95), [E07-S05](https://github.com/tamhtt-3564/fish-market-backlog/issues/97), [E07-S07](https://github.com/tamhtt-3564/fish-market-backlog/issues/99) | Không |
| Đợt migration | W6 | E02, E04, E06, E07, E08, E13 | [E02-S06](https://github.com/tamhtt-3564/fish-market-backlog/issues/51), [E04-S08](https://github.com/tamhtt-3564/fish-market-backlog/issues/75), [E06-S07](https://github.com/tamhtt-3564/fish-market-backlog/issues/91), [E07-S04](https://github.com/tamhtt-3564/fish-market-backlog/issues/96), [E08-S01](https://github.com/tamhtt-3564/fish-market-backlog/issues/100), [E08-S02](https://github.com/tamhtt-3564/fish-market-backlog/issues/101), [E08-S03](https://github.com/tamhtt-3564/fish-market-backlog/issues/102), [E08-S04](https://github.com/tamhtt-3564/fish-market-backlog/issues/103), [E08-S06](https://github.com/tamhtt-3564/fish-market-backlog/issues/105), [E08-S07](https://github.com/tamhtt-3564/fish-market-backlog/issues/106), [E13-S02](https://github.com/tamhtt-3564/fish-market-backlog/issues/155) | Không |
| Đợt migration | W7 | E02, E09, E12 | [E02-S07](https://github.com/tamhtt-3564/fish-market-backlog/issues/52), [E09-S01](https://github.com/tamhtt-3564/fish-market-backlog/issues/108), [E09-S02](https://github.com/tamhtt-3564/fish-market-backlog/issues/109), [E09-S03](https://github.com/tamhtt-3564/fish-market-backlog/issues/110), [E09-S04](https://github.com/tamhtt-3564/fish-market-backlog/issues/111), [E09-S05](https://github.com/tamhtt-3564/fish-market-backlog/issues/112), [E09-S06](https://github.com/tamhtt-3564/fish-market-backlog/issues/113), [E09-S07](https://github.com/tamhtt-3564/fish-market-backlog/issues/114), [E09-S09](https://github.com/tamhtt-3564/fish-market-backlog/issues/116), [E12-S08](https://github.com/tamhtt-3564/fish-market-backlog/issues/151) | Không |
| Đợt migration | W8 | E02, E10 | [E02-S08](https://github.com/tamhtt-3564/fish-market-backlog/issues/53), [E10-S03](https://github.com/tamhtt-3564/fish-market-backlog/issues/122), [E10-S04](https://github.com/tamhtt-3564/fish-market-backlog/issues/123), [E10-S05](https://github.com/tamhtt-3564/fish-market-backlog/issues/124), [E10-S06](https://github.com/tamhtt-3564/fish-market-backlog/issues/125) | Không |
| Đợt migration | W9 | E11, E12 | [E11-S01](https://github.com/tamhtt-3564/fish-market-backlog/issues/127), [E11-S02](https://github.com/tamhtt-3564/fish-market-backlog/issues/128), [E11-S03](https://github.com/tamhtt-3564/fish-market-backlog/issues/129), [E11-S05](https://github.com/tamhtt-3564/fish-market-backlog/issues/131), [E11-S06](https://github.com/tamhtt-3564/fish-market-backlog/issues/132), [E11-S07](https://github.com/tamhtt-3564/fish-market-backlog/issues/133), [E12-S09](https://github.com/tamhtt-3564/fish-market-backlog/issues/152) | Không |
| Đợt migration | W10 | E02, E03, E12, E13, E14, E15, E16 | [E02-S09](https://github.com/tamhtt-3564/fish-market-backlog/issues/54), [E02-S10](https://github.com/tamhtt-3564/fish-market-backlog/issues/55), [E03-S01](https://github.com/tamhtt-3564/fish-market-backlog/issues/56), [E03-S02](https://github.com/tamhtt-3564/fish-market-backlog/issues/57), [E03-S07](https://github.com/tamhtt-3564/fish-market-backlog/issues/62), [E12-S05](https://github.com/tamhtt-3564/fish-market-backlog/issues/148), [E13-S06](https://github.com/tamhtt-3564/fish-market-backlog/issues/159), [E14-S04](https://github.com/tamhtt-3564/fish-market-backlog/issues/163), [E15-S04](https://github.com/tamhtt-3564/fish-market-backlog/issues/167), [E16-S03](https://github.com/tamhtt-3564/fish-market-backlog/issues/4) | Tách 10a ([E02-S10](https://github.com/tamhtt-3564/fish-market-backlog/issues/55)), 10b ([E02-S09](https://github.com/tamhtt-3564/fish-market-backlog/issues/54)) theo PREMISE S-02 |
| Việc LAB-4 chuyển LAB-5 | C-12 | E02, E03, E04, E15 | [E02-S05](https://github.com/tamhtt-3564/fish-market-backlog/issues/50), [E03-S11](https://github.com/tamhtt-3564/fish-market-backlog/issues/66), [E04-S06](https://github.com/tamhtt-3564/fish-market-backlog/issues/73), [E15-S03](https://github.com/tamhtt-3564/fish-market-backlog/issues/166), [E15-S07](https://github.com/tamhtt-3564/fish-market-backlog/issues/170) | Không |
| Việc LAB-4 chuyển LAB-5 | C-15 | E01, E02, E09, E12, E13, E14 | [E01-S05](https://github.com/tamhtt-3564/fish-market-backlog/issues/41), [E02-S09](https://github.com/tamhtt-3564/fish-market-backlog/issues/54), [E09-S02](https://github.com/tamhtt-3564/fish-market-backlog/issues/109), [E09-S03](https://github.com/tamhtt-3564/fish-market-backlog/issues/110), [E12-S05](https://github.com/tamhtt-3564/fish-market-backlog/issues/148), [E12-S08](https://github.com/tamhtt-3564/fish-market-backlog/issues/151), [E12-S09](https://github.com/tamhtt-3564/fish-market-backlog/issues/152), [E13-S01](https://github.com/tamhtt-3564/fish-market-backlog/issues/154), [E13-S03](https://github.com/tamhtt-3564/fish-market-backlog/issues/156), [E14-S02](https://github.com/tamhtt-3564/fish-market-backlog/issues/161), [E14-S04](https://github.com/tamhtt-3564/fish-market-backlog/issues/163) | Phần việc nền không có TECH: thiết kế ngắn trong issue (PREMISE G-05) |
| Việc LAB-4 chuyển LAB-5 | C-16 | E17 | [E17-S02](https://github.com/tamhtt-3564/fish-market-backlog/issues/172), [E17-S03](https://github.com/tamhtt-3564/fish-market-backlog/issues/173), [E17-S07](https://github.com/tamhtt-3564/fish-market-backlog/issues/177), [E17-S08](https://github.com/tamhtt-3564/fish-market-backlog/issues/178) | Không |
| Việc LAB-4 chuyển LAB-5 | C-17 | E01, E03, E18, E19 | [E01-S02](https://github.com/tamhtt-3564/fish-market-backlog/issues/38), [E01-S03](https://github.com/tamhtt-3564/fish-market-backlog/issues/39), [E01-S04](https://github.com/tamhtt-3564/fish-market-backlog/issues/40), [E03-S04](https://github.com/tamhtt-3564/fish-market-backlog/issues/59), [E18-S06](https://github.com/tamhtt-3564/fish-market-backlog/issues/185), [E19-S02](https://github.com/tamhtt-3564/fish-market-backlog/issues/187), [E19-S07](https://github.com/tamhtt-3564/fish-market-backlog/issues/192) | Không |
| Việc LAB-4 chuyển LAB-5 | C-18 | E19 | [E19-S01](https://github.com/tamhtt-3564/fish-market-backlog/issues/186), [E19-S03](https://github.com/tamhtt-3564/fish-market-backlog/issues/188), [E19-S04](https://github.com/tamhtt-3564/fish-market-backlog/issues/189), [E19-S05](https://github.com/tamhtt-3564/fish-market-backlog/issues/190), [E19-S06](https://github.com/tamhtt-3564/fish-market-backlog/issues/191), [E19-S07](https://github.com/tamhtt-3564/fish-market-backlog/issues/192) | Trực 30 ngày sau go-live không thành issue (PREMISE G-20) |
| Việc LAB-4 chuyển LAB-5 | C-19 | E15, E17, E18 | [E15-S07](https://github.com/tamhtt-3564/fish-market-backlog/issues/170), [E17-S04](https://github.com/tamhtt-3564/fish-market-backlog/issues/174), [E17-S05](https://github.com/tamhtt-3564/fish-market-backlog/issues/175), [E17-S06](https://github.com/tamhtt-3564/fish-market-backlog/issues/176), [E17-S09](https://github.com/tamhtt-3564/fish-market-backlog/issues/179), [E18-S03](https://github.com/tamhtt-3564/fish-market-backlog/issues/182) | Không |
| Việc LAB-4 chuyển LAB-5 | C-20 | E06, E19 | [E06-S04](https://github.com/tamhtt-3564/fish-market-backlog/issues/88), [E19-S02](https://github.com/tamhtt-3564/fish-market-backlog/issues/187), [E19-S04](https://github.com/tamhtt-3564/fish-market-backlog/issues/189) | Không |
| Việc LAB-4 chuyển LAB-5 | C-24 | E05, E06, E07, E08, E09, E10 | [E05-S01](https://github.com/tamhtt-3564/fish-market-backlog/issues/77), [E05-S04](https://github.com/tamhtt-3564/fish-market-backlog/issues/80), [E05-S05](https://github.com/tamhtt-3564/fish-market-backlog/issues/81), [E06-S01](https://github.com/tamhtt-3564/fish-market-backlog/issues/85), [E06-S03](https://github.com/tamhtt-3564/fish-market-backlog/issues/87), [E07-S02](https://github.com/tamhtt-3564/fish-market-backlog/issues/94), [E07-S03](https://github.com/tamhtt-3564/fish-market-backlog/issues/95), [E07-S04](https://github.com/tamhtt-3564/fish-market-backlog/issues/96), [E08-S01](https://github.com/tamhtt-3564/fish-market-backlog/issues/100), [E08-S03](https://github.com/tamhtt-3564/fish-market-backlog/issues/102), [E08-S06](https://github.com/tamhtt-3564/fish-market-backlog/issues/105), [E09-S02](https://github.com/tamhtt-3564/fish-market-backlog/issues/109), [E10-S03](https://github.com/tamhtt-3564/fish-market-backlog/issues/122), [E10-S06](https://github.com/tamhtt-3564/fish-market-backlog/issues/125) | Không |

**Phần spec chưa thành issue và vì sao** (ngoài các dòng bảng trên):

| Phần | Vì sao không thành issue |
|---|---|
| Quản lý dự án (PM) | Không gán việc được cho chính người lập sprint; công tính ở `estimate.md` (D5-11) |
| 30 ngày trực sau go-live | Trực theo ca, không chia được thành việc tối đa 2 ngày; chỉ có issue lập lịch trực [E19-S07](https://github.com/tamhtt-3564/fish-market-backlog/issues/192) (PREMISE G-20) |
| Người dùng của khách làm UAT | Việc của khách; đội chỉ có issue hỗ trợ UAT ở E19 (mục 1.3) |
| 48 câu Q4 không thuộc G-01a | Làm theo mặc định LAB-4, không đổi nhiều khối lượng (PREMISE G-01) |
| 6 option của LAB-1, gói upsale LAB-3 | Ngoài phạm vi cơ bản (PREMISE LAB-4 mục 7) |
| Câu QA còn Open ở SCR-09, SCR-12, SCR-18 | Làm theo cách TECH đã ghi; không đổi khối lượng |

## 3. Hạng mục chịu ràng buộc đặc thù của đề: 完納奨励金

Đề bắt tách 完納奨励金 (business logic nhiều biến) thành task riêng. Epic E11 có 17 issue, 48 sub-issue (đếm: `python scripts/validate-backlog-items.py --summary`, dòng E11); mỗi biến nghiệp vụ là một mục có tiêu chí xong riêng.

| Ràng buộc (biến nghiệp vụ) | Issue | Vì sao tách riêng |
|---|---|---|
| Dữ liệu riêng của 奨励金 (khoản trả, kết quả theo kỳ, chênh lệch) | [E11-S01](https://github.com/tamhtt-3564/fish-market-backlog/issues/127) (đợt migration 9) | Ba bảng mới, không dùng chung đợt nào; tách để các phần tính chạy được trên DB đã có bảng |
| Ghi khoản trả: nhập tay, nạp CSV | [E11-S02](https://github.com/tamhtt-3564/fish-market-backlog/issues/128), [E11-S03](https://github.com/tamhtt-3564/fish-market-backlog/issues/129) | Hai đường ghi khác nhau về kiểm, lỗi, quyền; CSV có luật một dòng lỗi thì không nạp cả file ([E11-S03-T02](https://github.com/tamhtt-3564/fish-market-backlog/issues/585)) |
| Khoản trả trùng: cảnh báo, người dùng xác nhận mới ghi | [E11-S02-T03](https://github.com/tamhtt-3564/fish-market-backlog/issues/579), [E11-S03-T03](https://github.com/tamhtt-3564/fish-market-backlog/issues/586) | Quyết định riêng của người dùng (D4-146), dễ sai nếu gộp vào ghi khoản trả |
| Điều kiện được thưởng: trả đủ trong hạn, quá hạn, trả thiếu | [E11-S05-T01](https://github.com/tamhtt-3564/fish-market-backlog/issues/597) | Là biến quyết định có thưởng hay không; câu khách còn mở ([E11-S09](https://github.com/tamhtt-3564/fish-market-backlog/issues/135), [E11-S11](https://github.com/tamhtt-3564/fish-market-backlog/issues/137)) |
| Hạn trả: ngày nghiệp vụ cộng số ngày, đếm ngày lịch giờ Nhật | [E11-S05-T02](https://github.com/tamhtt-3564/fish-market-backlog/issues/598), làm rõ [E11-S17](https://github.com/tamhtt-3564/fish-market-backlog/issues/143) (Q4-61) | Sai một ngày là sai thưởng; cần test riêng ở biên tháng |
| Công thức: so ngưỡng trước thuế, nhân tỷ lệ, nhân thuế, cắt phần lẻ một lần | [E11-S05-T03](https://github.com/tamhtt-3564/fish-market-backlog/issues/599) | Thứ tự phép tính đổi kết quả; câu khách còn mở ([E11-S13](https://github.com/tamhtt-3564/fish-market-backlog/issues/139)) |
| Kỳ có hai version 料率 | [E11-S05-T04](https://github.com/tamhtt-3564/fish-market-backlog/issues/600) | So ngưỡng riêng từng version; câu khách còn mở ([E11-S10](https://github.com/tamhtt-3564/fish-market-backlog/issues/136)) |
| Tính tạm trước hạn trả cuối, tính lại nhiều lần | [E11-S05-T05](https://github.com/tamhtt-3564/fish-market-backlog/issues/601) | Trạng thái kỳ khác nhau trước và sau hạn |
| Kỳ không có giao dịch, tháng chỉ có chênh lệch nhận vào | [E11-S05-T06](https://github.com/tamhtt-3564/fish-market-backlog/issues/602) | Nhánh biên dễ sót |
| Bộ ví dụ biên thành test tự động | [E11-S05-T10](https://github.com/tamhtt-3564/fish-market-backlog/issues/606) | Kiểm công thức bằng số, độc lập với giao diện |
| Xác nhận theo thứ tự tháng, chỉ sau hạn trả cuối | [E11-S06-T01](https://github.com/tamhtt-3564/fish-market-backlog/issues/609), [E11-S06-T02](https://github.com/tamhtt-3564/fish-market-backlog/issues/610) | Chặn xác nhận lệch thứ tự và kết quả đã cũ |
| Phần âm chuyển sang kỳ sau | [E11-S06-T03](https://github.com/tamhtt-3564/fish-market-backlog/issues/611) | Không thu lại tiền đã trả; câu khách còn mở ([E11-S12](https://github.com/tamhtt-3564/fish-market-backlog/issues/138)) |
| Chênh lệch sau xác nhận: kỳ đích, do phiếu sửa, do trả muộn | [E11-S07-T01](https://github.com/tamhtt-3564/fish-market-backlog/issues/616), [E11-S07-T02](https://github.com/tamhtt-3564/fish-market-backlog/issues/617), [E11-S07-T03](https://github.com/tamhtt-3564/fish-market-backlog/issues/618), làm rõ [E11-S16](https://github.com/tamhtt-3564/fish-market-backlog/issues/142) (Q4-57) | Ba nguồn chênh lệch khác nhau, cùng ghi vào kỳ chưa xác nhận sớm nhất |
| Màn SCR-25 và quyền theo vai | [E11-S04](https://github.com/tamhtt-3564/fish-market-backlog/issues/130) và các sub giao diện của S02..S07 | Giao diện và quyền đọc tách khỏi logic tính |
| Kiểm thử đầu cuối qua ba tháng | [E11-S08](https://github.com/tamhtt-3564/fish-market-backlog/issues/134) | Chứng minh các biến chạy đúng khi nối nhau |
| Phần 奨励金 trong file kế toán | [E12-S09](https://github.com/tamhtt-3564/fish-market-backlog/issues/152) (phụ thuộc [E11-S01](https://github.com/tamhtt-3564/fish-market-backlog/issues/127)) | Thuộc epic xuất kế toán, nhưng dùng dữ liệu của E11 |
| Câu khách chưa trả lời | [E11-S09](https://github.com/tamhtt-3564/fish-market-backlog/issues/135)..[E11-S17](https://github.com/tamhtt-3564/fish-market-backlog/issues/143) (Q4-55, 58, 59, 60, 63, 64, 56, 57, 61) | Mỗi câu đổi một biến; theo dõi riêng để ước lại đúng chỗ |

## 4. Chỗ hở hoặc mâu thuẫn của spec LAB-4 phát hiện khi chia

| Spec | Chỗ hở / mâu thuẫn | Xử lý |
|---|---|---|
| Bảng đợt migration, phần "ngoài 9 đợt" (`api-design/_index.md`) | Câu "không hàm nào của 9 đợt đọc các bảng này" sai: hàm cảnh báo khoá ngày của đợt 7 đọc bảng báo cáo; cột mới của bảng người dùng cần từ đầu | Đã sửa thiết kế: PREMISE S-02, H-05 |
| TECH khoá ngày SCR-21 mục 5 (d) | Hàm chuyển lô kẹt chỉ có tên, chưa có chỗ lưu quan hệ hai lô, chưa có API | Đã sửa thiết kế: PREMISE S-03 |
| DB design, `log-convention.md`, N-24, N-17, N-20, N-01 | Công bố đối soát, cấu hình thông báo chưa có chỗ lưu; thiếu cột nhập lại biên nhận, thiếu loại audit tạo tài khoản và yêu cầu xoá dữ liệu cá nhân; đợt 10 thiếu vá hàm đặt lại dữ liệu demo | Đã sửa thiết kế: PREMISE S-04 |
| DB design 6.2 | Ràng buộc đơn giá tối thiểu không nằm ở đợt nào | Đã sửa thiết kế: PREMISE S-05 |
| TECH SCR-09 mục 5 | Câu ghi chú cũ nói `api-conventions.md` cho bỏ trống mã chống ghi trùng khi ghi trực tuyến; `api-conventions.md` bản hiện tại đã bắt gửi ở mọi lần | Đã sửa thiết kế: PREMISE S-06 |
| DB 6.5, N-05, SCR-14 | Hai hàm nộp và từ chối giao dịch không có chỗ dùng, trạng thái chờ xác nhận không được lưu | Để mở: TL-A chốt ở [E06-S08](https://github.com/tamhtt-3564/fish-market-backlog/issues/92) trước sprint làm SCR-16 (PREMISE H-06) |
| Bảng đợt migration (5 hàm nền) | Hàm nền dùng chung không có TECH, không ghi ai viết | Giả định: PREMISE G-10 |
| Bảng đợt migration (đợt 2, 4) | Ghi cả hàm có TECH, không tách phần của migration và của màn | Giả định: PREMISE G-11 |
| C-17, ADR-006 | Cờ máy hiện trường chưa có chỗ lưu; lưu ở trình duyệt thì người dùng tự gỡ được, chỉ chặn ở giao diện | Đã sửa thiết kế: PREMISE S-07 |
| Q4-31, N-25 | Chưa nói hàm nào sinh thông báo cho người tham gia | Giả định: PREMISE G-13 |
| ADR-007 | In chứng từ không có API, luật chặn ở API không áp nguyên được | Giả định: PREMISE G-14 |
| N-22, ADR-017 | Vai trò được tra vùng lịch sử nói khác nhau | Giả định: PREMISE G-15 |
| Kiến trúc mục 8 (tải) | Chưa có môi trường thử tải | Giả định: PREMISE G-16 |
| Kiến trúc mục 8 (uptime) | Đo uptime cần lịch ngày chợ chưa chốt | Giả định: PREMISE G-17 |
| TECH khoá ngày và TECH duyệt phiếu | Nghĩa dòng mới của phiếu sửa: một chỗ để mở, một chỗ đã chốt | Giả định: PREMISE G-18 |
| 14 màn chỉ có wireframe, 9 màn chưa có spec | Story có hàm ghi mà không có ai thiết kế thứ tự kiểm, khoá, mã lỗi, audit trước khi code | Giả định: PREMISE G-02, G-03 (thiết kế kỹ thuật ngắn của TL-A) |
| ADR-003, TECH SCR-09, SCR-18 | Phần dùng chung của ghi tạm khi mất mạng không thuộc màn nào | Giả định: PREMISE G-19 |
| SCR-27 | Không nói có thông báo cho người duyệt version | Giả định: PREMISE G-21 |
| ADR-012, mã prototype | Hằng số số lần giao, số ngày cảnh báo còn trong mã, spec không nói ai bỏ | Giả định: PREMISE G-22 |
| TECH chốt kỳ SCR-21 mục 4.7 | Việc nền cảnh báo biên nhận đồng bộ treo đã thiết kế mà không thuộc màn nào | Giả định: PREMISE G-23 |
| Mục 5 (b), (c) của các TECH | Nhiều dòng "sửa DB design, sửa bảng mã lỗi" là sửa tài liệu | Giả định: PREMISE G-24 |
| `error-codes.md` 6.6 | Bảng đổi mã lỗi sang mã HTTP trong mã chưa giao epic nào | Giả định: PREMISE G-25 |
| Q4-56, SCR-25 QA | Mẫu CSV và luật dòng lỗi là giả định, đổi nhiều khối lượng | Tạo issue làm rõ: [E11-S15](https://github.com/tamhtt-3564/fish-market-backlog/issues/141) (PREMISE G-01a) |
| C-19, Q4-10 | Vùng lịch sử hết hạn 7 năm chưa có hàm ẩn danh hoá | Để mở: chờ trả lời Q4-10 (issue làm rõ ở E15); issue chỉ chừa đường trong trigger |
| SCR-25 QA Q3, kiến trúc 5.4 | Kiến trúc cho tính sau hạn, SCR-25 cho tính tạm sớm hơn | Để mở: làm theo SCR-25 (bản chi tiết hơn); khác thì chỉ bỏ nhánh tính tạm ở [E11-S05-T05](https://github.com/tamhtt-3564/fish-market-backlog/issues/601) |
| TECH tải file phiếu sửa mục 5 (e) | Phiếu đã nộp mà file lỗi sau khi rời màn thì không gắn lại được | Để mở: thêm nút ở SCR-24 là thay đổi giao diện chưa ai yêu cầu; nếu cần, một sub giao diện khoảng 4 giờ |
| SCR-21 SPEC 6.6, QA Q10 | Không có thao tác rút đề nghị mở lại sổ | Để mở: spec ghi là suy luận, chưa ai yêu cầu |
| C-14 | Tên người đang đăng nhập có phải ghi log đọc dữ liệu cá nhân không | Để mở: chốt ở thiết kế ngắn [E03-S10-T01](https://github.com/tamhtt-3564/fish-market-backlog/issues/302), chỉ đổi số dòng log |
| C-20, kiến trúc 8.1 | Nhập bù phiếu giấy vào ngày đã khoá khi hệ thống ngừng qua mốc khoá | Để mở: chốt khi viết runbook [E19-S02](https://github.com/tamhtt-3564/fish-market-backlog/issues/187) |

# Estimate backlog LAB-5 (Product A, chợ thủy sản)

## 1. Báo cáo HTML của skill

- Báo cáo: [`estimate/reports/sun-estimate-fish-market-backlog-project-1-20261102.html`](estimate/reports/sun-estimate-fish-market-backlog-project-1-20261102.html) (tải về rồi mở bằng trình duyệt; chạy được không cần mạng).
- Skill: `tkm:sun-estimate`, mô hình `swp-matrix-v2`. Mỗi việc chấm hai trục: Scope (độ rộng: bao nhiêu thành phần, tầng) và Complexity (độ khó bên trong). SWP tra từ bảng cố định theo hai trục, không cộng hai trục.
- Nguồn chấm: 792 issue đọc từ Project #1 ngày 2026-11-02, chỉ đọc. 654 việc lá được chấm trực tiếp. 138 mục cha (19 epic, 85 story, 34 issue có sub-issue) không chấm riêng; SWP của mục cha là tổng SWP các con.
- Kết quả: tổng 2.187 SWP. Độ tin: cao 241 việc, vừa 350, thấp 63. Không việc nào bị đề nghị tách thêm.
- Phân bố SWP của 654 việc lá: 1 SWP 39 việc, 2 SWP 27, 3 SWP 415, 4 SWP 79, 5 SWP 54, 6 SWP 34, 8 SWP 3, 10 SWP 2, 15 SWP 1. Phần lớn ở 3 SWP vì mỗi việc lá đã chia nhỏ tối đa 2 ngày một người (`task-breakdown.md` mục 1.4).
- Trường Story Point trên Project là SWP đã review ở mục 2. Mục cha ghi tổng của các con; việc lá ghi thêm trường Scope và Complexity. Số liệu nằm ở `backlog/story-points.json`, ghi lên Project bằng `python scripts/write-story-points-to-project.py`.
- Lệnh đếm:
  - tổng và phân bố: đọc `backlog/story-points.json`, cộng `swp` các mục `direct: true`;
  - đối chiếu Project: truy vấn `fieldValueByName("Story Point")` của 792 mục, kết quả 0 mục lệch, tổng việc lá 2.187, tổng 19 epic 2.187.

Chỗ làm khác quy trình của skill, có ghi trong phần "caveats" của báo cáo:
- Agent chấm riêng của skill không có quyền đọc ghi file nên không nhận được lô việc. 5 lô được chấm lại bằng agent thường, theo cùng bộ luật chấm, chỉ đọc ghi trong thư mục tạm, không gọi mạng.
- Skill chỉ đọc. Bước ghi Story Point lên Project là script riêng của repo này, chạy sau khi người đã duyệt (cách làm người dùng chốt từ đầu).
- Thân issue dẫn mã spec LAB-4 nằm ở repo private, agent chấm không mở được nên chỉ dựa vào chữ trong issue. Trong 63 việc độ tin thấp: 40 việc thuộc 9 màn chưa có spec (PREMISE G-02), 10 việc đã gắn nhãn `độ tin thấp` từ bước 2, 1 việc làm rõ với khách, 12 việc còn lại do thân issue ngắn (đếm: lọc `confidence == "low"` trong `backlog/story-points.json`, đối chiếu `spec_refs`, nhãn, loại trong `backlog/items-*.json`). Các việc này chấm lại khi có spec hoặc câu trả lời của khách.

## 2. Issue mẫu skill chọn để kiểm

Skill tự chọn 5 issue theo luật cố định: nhỏ nhất, trung vị, lớn nhất, lệch xa trung vị nhất, độ tin thấp nhất. Người duyệt từng issue qua hai câu hỏi: mức khó (rất dễ, dễ, vừa, khó, rất khó), rồi điểm cụ thể trong mức đó.

| Issue | Vì sao được chọn | Skill chấm (Scope × Complexity → SWP) | Bạn chốt | Lý do |
|---|---|---|---|---|
| [#45](https://github.com/tamhtt-3564/fish-market-backlog/issues/45) E01-S09 Làm rõ Q4-25 kèm Q4-19 (rủi ro sao lưu một vùng) | Nhỏ nhất | 1 × 0 → 1 | 1 | Một lần hỏi đáp với khách, ghi câu trả lời vào bảng Q4; không có quyết định kỹ thuật trong issue |
| [#563](https://github.com/tamhtt-3564/fish-market-backlog/issues/563) E10-S05-T01 Hàm DB nộp version và đếm số lần đổi, kèm test | Trung vị | 2 × 2 → 3 | 3 | Hai hàm trong một tầng DB đã có thiết kế TECH; độ khó nằm ở biên 4 lần đổi và loại trừ bản rollback, đúng mức "dễ" |
| [#178](https://github.com/tamhtt-3564/fish-market-backlog/issues/178) E17-S08 Chạy chuyển đổi dữ liệu gốc lên production trước go-live | Lớn nhất | 5 × 5 → 15 | 15 | Thao tác một lần trên production, có go / no-go, khó quay lui; định dạng dữ liệu hệ thống cũ chưa rõ nên độ khó cao là có căn cứ |
| [#177](https://github.com/tamhtt-3564/fish-market-backlog/issues/177) E17-S07 Diễn tập chuyển đổi trên staging | Lệch xa trung vị | 5 × 3 → 10 | 10 | Chạy trọn thủ tục bằng file thật của khách, đo giờ, đối số; nhẹ hơn #178 vì trên staging làm lại được |
| [#3](https://github.com/tamhtt-3564/fish-market-backlog/issues/3) E16-S02 Làm rõ luồng và hạn xử lý tranh chấp (Q4-02) | Độ tin thấp nhất | 2 × 1 → 3 | 3 | Ngoài hỏi khách còn phải sửa và ước lại các issue tranh chấp liên quan, nên nặng hơn #45 |

Không sửa issue mẫu nào: cả 5 điểm đều khớp cảm nhận của người duyệt về độ khó, và thứ tự giữa các issue mẫu hợp lý (diễn tập nhẹ hơn chạy thật, việc làm rõ kéo theo sửa issue nặng hơn việc chỉ hỏi đáp). Vì không có chỉnh sửa, skill không lan điều chỉnh sang việc khác; 654 việc giữ nguyên điểm skill chấm (báo cáo HTML: trạng thái "accepted", 0 việc đổi điểm).

**Kiểm thêm 2 issue điển hình** (ngoài skill, vì skill giới hạn 5 issue mẫu). 4/5 issue mẫu của skill là việc ngoại lệ (làm rõ với khách, chuyển đổi dữ liệu), không có việc QA hay FE, trong khi QA chiếm 32% tổng SWP. Luật chọn: trong nhóm việc, lấy việc có SWP trung vị, rồi giờ thô trung vị, rồi số issue nhỏ nhất.

| Issue | Đại diện cho | Skill chấm (Scope × Complexity → SWP) | Bạn chốt | Lý do |
|---|---|---|---|---|
| [#11](https://github.com/tamhtt-3564/fish-market-backlog/issues/11) E16-S03-T06 QA kiểm mở tranh chấp và danh sách tranh chấp (SCR-22) | 117 việc chạy kiểm thử; 68 việc cùng nhóm hiệu chỉnh | 2 × 1 → 3 | 3 | Chạy bộ ca có sẵn của một tính năng, ghi kết quả; thao tác quen |
| [#286](https://github.com/tamhtt-3564/fish-market-backlog/issues/286) E03-S07-T05 Hộp tạo tài khoản trên SCR-07 (N-01) | 82 việc dev FE; 56 việc cùng nhóm hiệu chỉnh | 2 × 1 → 3 | 3 | Một hộp tạo có ô chọn theo điều kiện, phím Esc, câu báo lỗi; validation thường |

"Cùng nhóm hiệu chỉnh" là nhóm skill dùng để lan điều chỉnh: cùng ngành (`primaryDiscipline`), cùng loại việc (`workType`), cùng hai bộ dấu hiệu Scope và Complexity (đếm: lọc 4 trường này trong payload nhúng ở báo cáo HTML). Cả hai giữ nguyên nên không nhóm việc nào phải chỉnh. Hai việc cùng 3 SWP nhưng giờ thô khác nhau (4 và 8 giờ): khác biệt về giờ giữa QA và FE được xử lý ở bước quy giờ (mục 3), không phải bằng cách đổi SWP.

Lưu ý cho bước quy giờ: SWP đo độ rộng và độ khó, không đo giờ. Hai issue cùng ước thô 10 giờ có thể khác SWP xa nhau (#563 3 SWP, #178 15 SWP). Mục 3 phải chọn cách quy có tính tới chuyện này.

## 3. Cách quy ra giờ

**Cách đã chọn:** quy ước đổi SWP ra giờ theo **hệ số của từng vai** (người duyệt chọn ở bước 5).

**Vì sao:**
- SWP đo độ rộng và độ khó, không đo giờ. Cùng 3 SWP, việc chạy bộ ca kiểm thử của QA thường ngắn hơn việc dev giao diện FE. Giờ thô trung bình mỗi SWP: QA-A 1,40 giờ, FE-B 2,72 giờ.
- Dùng một hệ số chung (1,84 giờ/SWP) thì phần QA dư khoảng 32%, phần FE-B thiếu khoảng 32%. Kế hoạch nhân sự sẽ thừa QA, thiếu FE.
- Giữ nguyên giờ thô của bước 2 thì sát từng việc hơn, nhưng giờ thô do AI ước lúc chia việc, chưa ai duyệt từng cái; còn SWP đã qua 5 issue mẫu của skill và 2 issue kiểm thêm.
- Hệ số theo vai vừa gắn giờ với SWP đã duyệt, vừa giữ tổng giờ từng vai bằng giờ thô của vai đó.

**Quy tắc** (áp cho mọi việc lá, không ngoại lệ):
1. Hệ số vai = tổng giờ thô bước 2 / tổng SWP các việc lá của vai đó, làm tròn 2 chữ số.
2. Giờ việc lá = SWP × hệ số vai, làm tròn 0,1 giờ kiểu thường (từ 0,05 làm tròn lên).
3. Giờ mục cha (story, issue có sub-issue, epic) = tổng giờ các con.
4. Chạy `python scripts/convert-story-points-to-hours.py`: ghi `backlog/estimated-hours.json`, in hai bảng dưới. Ghi trường Estimated time lên Project bằng `python scripts/write-story-points-to-project.py`.

| Vai | Việc lá | Tổng SWP | Giờ thô bước 2 | Hệ số giờ/SWP | Giờ quy đổi |
|---|---|---|---|---|---|
| BA-A | 10 | 44 | 108 | 2,45 | 108,2 |
| BE-A | 107 | 402 | 835 | 2,08 | 834,4 |
| BE-B | 113 | 388 | 810 | 2,09 | 813,8 |
| BrSE-A | 18 | 20 | 48 | 2,40 | 48,0 |
| Design-A | 31 | 98 | 170 | 1,73 | 169,7 |
| FE-A | 40 | 128 | 326 | 2,55 | 327,9 |
| FE-B | 42 | 127 | 345 | 2,72 | 346,7 |
| Infra-A | 28 | 112 | 175 | 1,56 | 174,8 |
| QA-A | 211 | 697 | 974 | 1,40 | 975,8 |
| TL-A | 54 | 171 | 240 | 1,40 | 239,4 |
| **Tổng** | **654** | **2.187** | **4.031** | | **4.038,7** |

Tổng quy đổi lệch giờ thô 7,7 giờ do làm tròn hệ số và làm tròn từng việc (chưa làm tròn: 4.034,18 giờ).

Tính thử bằng tay bốn việc:
- [#563](https://github.com/tamhtt-3564/fish-market-backlog/issues/563) E10-S05-T01, BE-A: 3 SWP × 2,08 = 6,24, làm tròn 6,2 giờ.
- [#11](https://github.com/tamhtt-3564/fish-market-backlog/issues/11) E16-S03-T06, QA-A: 3 SWP × 1,40 = 4,2 giờ.
- [#72](https://github.com/tamhtt-3564/fish-market-backlog/issues/72) E04-S05, BA-A: 5 SWP × 2,45 = 12,25, làm tròn lên 12,3 giờ.
- [#178](https://github.com/tamhtt-3564/fish-market-backlog/issues/178) E17-S08, Infra-A: 15 SWP × 1,56 = 23,4 giờ.

**Giới hạn của cách này:** trong cùng một vai, việc 2 giờ thô và việc 10 giờ thô cùng 3 SWP nhận cùng số giờ (tương quan SWP với giờ thô chỉ 0,52). Tổng theo vai và theo epic tin được hơn số giờ của từng việc. Khi lập sprint, người làm chỉnh giờ từng việc ở buổi lập kế hoạch.

**Khoảng dao động:** báo cáo HTML dịch ±1 bậc SWP cho 413 việc độ tin vừa và thấp: 1.802 tới 2.614 SWP, quy ra khoảng 3.399 tới 4.770 giờ. Chỉ dịch 63 việc độ tin thấp: 2.126 tới 2.256 SWP, khoảng 3.916 tới 4.179 giờ. Cách tính giờ của khoảng: mỗi việc giữ giờ/SWP của chính nó (`estimated-hours.json` chia `story-points.json`), nhân với SWP đã dịch một bậc trên dãy SWP hợp lệ của skill.

## 4. Tổng theo epic

Giờ ở bảng là giờ backlog, chưa có buffer, PM, BrSE điều phối, hỗ trợ 30 ngày (các phần này ở mục 5). Số issue là issue cấp một của epic; việc lá là mục được chấm SWP trực tiếp.

| Epic | Số issue | Việc lá | Tổng SWP | Tổng giờ | Ghi chú |
|---|---|---|---|---|---|
| E01 Hạ tầng và môi trường | 9 | 24 | 80 | 136,1 | 1 issue làm rõ với khách gộp Q4-25 và Q4-19 (E01-S09) |
| E02 Nền dữ liệu (đợt 1..8, 10) | 10 | 39 | 159 | 313,7 | Gồm 5 hàm nền dùng chung (PREMISE G-10); đợt 10 tách 10a, 10b (S-02) |
| E03 Đăng nhập, tài khoản, phân quyền | 12 | 60 | 177 | 313,9 | Thêm bảng thiết bị và mã máy hiện trường (S-07) |
| E04 Người tham gia | 9 | 40 | 125 | 233,5 | SCR-06 chưa có spec, có issue viết spec (G-02); bỏ hằng số số ngày cảnh báo trong mã (G-22) |
| E05 Tiếp nhận lô và 目利き | 8 | 32 | 106 | 205,5 | Thêm chuyển lô kẹt sau khoá ngày (S-03, E05-S05) |
| E06 Giao dịch 相対 / せり | 8 | 39 | 121 | 228,0 | E06-S08: TL-A chốt hai hàm của N-05 (H-06) |
| E07 Giao nhận | 7 | 34 | 122 | 230,8 | Bỏ hằng số số lần giao tối đa trong mã (G-22) |
| E08 Phiếu điều chỉnh, file đính kèm | 8 | 44 | 153 | 297,2 | |
| E09 Đối soát, khoá ngày, chốt kỳ | 12 | 55 | 191 | 356,9 | Việc nền cảnh báo biên nhận đồng bộ treo (G-23) |
| E10 Version 業務規程 / 料率 | 7 | 30 | 89 | 171,9 | SCR-26 chưa có spec (G-02) |
| E11 **完納奨励金** | 17 | 58 | 173 | 336,5 | Tách theo từng biến nghiệp vụ (`task-breakdown.md` mục 3); 9 issue làm rõ Q4 |
| E12 Báo cáo, in, xuất kế toán | 10 | 40 | 122 | 230,3 | SCR-28, 29, 30 chưa có spec (G-02) |
| E13 Thông báo, việc nền | 6 | 27 | 87 | 160,7 | SCR-31 chưa có spec (G-02) |
| E14 Mất mạng và đồng bộ | 4 | 21 | 67 | 132,0 | SCR-34 chưa có spec (G-02) |
| E15 Audit, lưu trữ, xoá theo hạn | 7 | 29 | 93 | 167,3 | SCR-33 chưa có spec (G-02) |
| E16 Tranh chấp | 4 | 15 | 48 | 94,2 | SCR-22 chưa có spec (G-02) |
| E17 Chuyển đổi dữ liệu | 9 | 26 | 115 | 197,8 | Có việc SWP cao nhất: chạy chuyển đổi trên production (#178, 15 SWP) |
| E18 Kiểm thử hệ thống, phi chức năng | 6 | 21 | 96 | 134,4 | Chỉ phần chung; kiểm thử từng tính năng nằm trong epic của tính năng |
| E19 Vận hành, đào tạo, hỗ trợ UAT, bàn giao | 8 | 20 | 63 | 98,0 | Hỗ trợ 30 ngày không có issue (G-20), tính ở mục 5 |
| **Tổng** | **161** | **654** | **2.187** | **4.038,7** | = 577,0 MD (1 MD = 7 giờ) |

Lệnh đếm: `python scripts/convert-story-points-to-hours.py` (bảng epic); số issue và việc lá đếm theo số dấu `-` của mã trong `backlog/story-points.json`.

## 5. So với estimate LAB-1

Estimate LAB-1 ra **805 MD**, đã gồm buffer 15%, PM và BrSE. Để so cùng cách, tổng LAB-5 cộng thêm đúng các phần LAB-1 có mà backlog không có:

| Thành phần | LAB-5 (MD) | Cách tính |
|---|---|---|
| Giờ backlog | 577,0 | 4.038,7 giờ / 7 |
| Buffer 15% | 86,5 | Như LAB-1, cho mọi việc trong backlog |
| Sửa lỗi kiểm thử hệ thống | 16,0 | Đóng khung như LAB-1 dòng T-06 (FE 6, BE 10 MD). Backlog không có issue sẵn cho việc này: lỗi tìm ra thành issue khi phát sinh |
| Hỗ trợ và sửa lỗi suốt cửa sổ UAT 6 tuần | 23,0 | Đóng khung như LAB-1 dòng U-01 (FE 4, BE 7, QA 11, Infra 1 MD; buffer 0%). Lỗi UAT thành issue `type:uatbug` khi phát sinh, tiêu công từ khung này |
| Hỗ trợ vận hành ban đầu | 23,0 | Đóng khung như LAB-1: hỗ trợ 30 ngày 22 MD (buffer 0%), đo KPI sau 1 tháng 1 MD (buffer 15%); không thành issue (G-20) |
| PM và BrSE điều phối | 139,7 | Cùng tỷ lệ LAB-1: 130 MD trên 675 MD phần còn lại (19,3%), tính trên 725,5 MD. Trùng nhẹ với 18 issue làm rõ của BrSE-A (48 giờ, khoảng 7 MD) đã nằm trong backlog |
| **Tổng** | **865,2** | Hơn LAB-1 60,2 MD (+7,5%), trong độ chính xác ±25% LAB-1 đã ghi |

So theo phần (LAB-5 tính kèm buffer 15% để cùng cách với LAB-1):

| Phần (LAB-1 → epic LAB-5) | LAB-1 (MD) | LAB-5 (MD) | Chênh | Vì sao |
|---|---|---|---|---|
| F01 Người tham gia → E04 | 29 | 38,4 | +9,4 | Kiểm thử từng tính năng chuyển vào epic tính năng (LAB-1 để ở "Kiểm thử hệ thống"); thêm issue viết spec SCR-06 (G-02); bỏ hằng số cũ trong mã (G-22) |
| F02 Xác thực, phân quyền → E03 | 24 | 51,6 | +27,6 | Thêm bảng thiết bị, mã máy hiện trường chặn ở máy chủ (PREMISE S-07); 11 vai trò, mỗi API có ca kiểm vai bị chặn |
| F03 Tiếp nhận lô, 目利き → E05 | 25 | 33,8 | +8,8 | Kiểm thử chuyển vào epic; thêm chuyển lô kẹt sau khoá ngày (S-03) |
| F04 Giao dịch → E06 | 32 | 37,5 | +5,5 | Kiểm thử chuyển vào epic |
| F05 Giao nhận → E07 | 25 | 37,9 | +12,9 | Kiểm thử chuyển vào epic; ghi tạm khi mất mạng phụ thuộc E14 (G-19); bỏ hằng số cũ trong mã (G-22) |
| F06 Đối soát, chốt sổ, tranh chấp → E09, E16 | 29 | 74,1 | +45,1 | Spec LAB-4 sâu hơn LAB-1: khoá ngày hai cổng, mở lại sổ, chốt kỳ; việc nền cảnh báo biên nhận treo (G-23) |
| F07 Điều chỉnh sau chốt → E08 | 16 | 48,8 | +32,8 | Phiếu sửa có duyệt, dòng đảo và dòng mới, file đính kèm (TECH LAB-4 chi tiết hơn); bảng đổi mã lỗi (G-25) |
| F08 完納奨励金 → E11 | 16 | 55,3 | +39,3 | LAB-1 ước như một tính năng; spec SCR-25 (PREMISE S-01) có 6 API, đợt migration 9, chênh lệch sau xác nhận, hai version 料率; đề bắt tách theo từng biến |
| F09 Version quy tắc → E10 | 11 | 28,2 | +17,2 | Spec SCR-26, 27 chi tiết hơn; SCR-26 chưa có spec, có issue viết spec (G-02) |
| F10, F11 Báo cáo, in, kế toán → E12 | 46 | 37,8 | −8,2 | LAB-1 ước 12 báo cáo cố định theo giả định; spec LAB-4 gom vào 3 màn (SCR-28..30) |
| F12 Thông báo → E13 | 14 | 26,4 | +12,4 | Thêm việc nền chưa có TECH, mỗi việc kèm thiết kế ngắn (G-05) |
| F13 Audit, lưu trữ → E15 | 29 | 27,5 | −1,5 | Gần như khớp |
| F14 và Nền tảng, thiết kế → E01, E02, E14 | 166 | 95,6 | −70,4 | Wireframe và spec 34 màn (LAB-1 X-03, X-08, 55 MD) đã làm ở LAB-2..4; phần còn lại là spec 9 màn và thiết kế ngắn của TL-A, nằm trong epic tính năng (G-02, G-03) |
| F15 và Chuyển đổi dữ liệu → E17 | 53 | 32,5 | −20,5 | ADR-017 chốt phạm vi hẹp hơn LAB-1: dữ liệu gốc vào bảng nghiệp vụ, 13 tháng lịch sử vào vùng tra cứu chỉ đọc, giao dịch dở chạy nốt ở hệ thống cũ (không chuyển); độ tin thấp vì định dạng hệ thống cũ chưa rõ |
| Kiểm thử hệ thống → E18 và khung sửa lỗi | 89 | 38,1 | −50,9 | Gồm 16 MD khung sửa lỗi như T-06. Kiểm thử từng tính năng (QA-A 211 việc) đã chia vào epic tính năng; E18 còn 6 issue chung: kế hoạch kiểm thử, kiểm thử đầu cuối, tải, quét quyền theo 11 vai, accessibility, bảo mật |
| UAT, đào tạo, bàn giao → E19 và khung UAT | 48 | 39,1 | −8,9 | Gồm 23 MD khung UAT như U-01. Phần còn thấp hơn: đào tạo và tài liệu vận hành của E19 ước theo việc cụ thể, nhỏ hơn U-02, U-03 của LAB-1 |
| Hỗ trợ vận hành ban đầu | 23 | 23,0 | 0 | Đóng khung như LAB-1 |
| PM và BrSE | 130 | 139,7 | +9,7 | Cùng tỷ lệ 19,3%, base lớn hơn |
| **Tổng** | **805** | **865,3** | **+60,3** | Lệch 0,1 so với bảng thành phần do làm tròn từng dòng |

So theo giai đoạn của kế hoạch nguồn lực LAB-1 (mục 6 của estimate LAB-1; MD LAB-1 mỗi giai đoạn đã gồm phần PM, BrSE). LAB-5 = giờ các epic của giai đoạn / 7 × 1,15, cộng khung đóng, rồi cộng phần PM và BrSE 19,3%:

| Giai đoạn LAB-1 | LAB-1 (MD) | Epic LAB-5 | LAB-5 (MD) | Chênh | Ghi chú |
|---|---|---|---|---|---|
| GĐ1 Yêu cầu, thiết kế (T1..T2) | 124 | (không có) | 0,0 | −124,0 | Đã làm ở LAB-2..4 (wireframe, spec, kiến trúc); spec 9 màn còn thiếu và thiết kế ngắn nằm trong GĐ2 |
| GĐ2 Xây dựng (T3..T6) | 465 | E01..E16 | 707,0 | **+242,0 (+52%)** | Chỗ vượt chính: kiểm thử từng tính năng, spec 9 màn, thiết kế ngắn của TL nằm ở đây; quy tắc nghiệp vụ LAB-4 chi tiết hơn |
| GĐ3 Kiểm thử hệ thống, chuyển đổi (T7..T8 tuần 2) | 120 | E17, E18, khung sửa lỗi 16 MD | 84,2 | −35,8 | Kiểm thử từng tính năng đã chuyển sang GĐ2 |
| GĐ4 UAT, đào tạo, chuyển đổi chính thức (T8 tuần 3..T9) | 69 | E19, khung UAT 23 MD | 46,6 | −22,4 | |
| GĐ5 Hỗ trợ vận hành ban đầu (T10) | 27 | Khung hỗ trợ 23 MD | 27,4 | +0,4 | |
| **Tổng** | **805** | | **865,2** | **+60,2** | |

Đội và lịch của LAB-1 không đủ cho GĐ2. Với đội 5,8 người như giả lập Sprint 1 (cam kết 85% năng lực), phần xây dựng E01..E16 còn lại sau Sprint 1 cần số sprint theo từng vai như dưới; GĐ2 còn 7 sprint tính từ Sprint 2:

| Vai | Giờ còn lại (E01..E16) | Năng lực mỗi sprint (giờ) | Sprint cần | Người cần thêm để xong trong 7 sprint |
|---|---|---|---|---|
| BE-A, BE-B | 743,1 + 727,8 | 51,0 + 51,0 | 14,6; 14,3 | 1,1 + 1,0 |
| QA-A | 763,0 | 51,0 | 15,0 | 1,1 |
| Design-A | 162,8 | 10,2 | 16,0 | 0,3 |
| FE-B | 346,7 | 25,5 | 13,6 | 0,5 |
| FE-A, TL-A, BA-A, Infra-A, BrSE-A | | | 1,1 tới 7,7 | 0 |
| **Tổng** | | | | **khoảng 4 người** |

Cách tính: giờ còn lại = `estimated-hours.json` của việc lá E01..E16 chưa Closed sau Sprint 1, theo `owner`; năng lực = người × 60 giờ × 85%; người cần thêm = giờ còn lại / (7 × 60 × 0,85) − số người hiện có. Chỗ nghẽn dài hạn là BE, QA và Design; TL chỉ nghẽn ở Sprint 1 (thiết kế ngắn dồn đầu dự án).

Ngoài ra, 3 việc lá sau khi quy giờ vượt luật 14 giờ của `task-breakdown.md` mục 1.4 (luật áp cho giờ thô bước 2): [#178](https://github.com/tamhtt-3564/fish-market-backlog/issues/178) 23,4 giờ, [#355](https://github.com/tamhtt-3564/fish-market-backlog/issues/355) 16,3 giờ, [#179](https://github.com/tamhtt-3564/fish-market-backlog/issues/179) 15,6 giờ; tách nhỏ ở buổi lập kế hoạch sprint có các việc này.

Đọc bảng:
- Tổng cao hơn 7,5% (trong độ chính xác ±25% của LAB-1), nhưng con số này **che chỗ vượt**: riêng giai đoạn xây dựng vượt 52%, bù lại bằng 124 MD thiết kế đã làm ở LAB-2..4. Kế hoạch đội và lịch của LAB-1 phải sửa theo bảng giai đoạn, không theo tổng. **Cơ cấu đổi nhiều**: phần tính năng nghiệp vụ tăng, phần nền tảng, thiết kế và kiểm thử hệ thống giảm. Hai lý do chính: wireframe và spec đã làm ở LAB-2..4 nên không còn trong backlog; kiểm thử từng tính năng được chia về epic của tính năng.
- Phần tăng nhiều nhất (E11, E09, E08, E03) là chỗ spec LAB-4 làm rõ thêm quy tắc nghiệp vụ so với lúc ước LAB-1. 完納奨励金 tăng từ 16 lên 55,3 MD, đúng với yêu cầu tách theo từng biến của đề.
- Hai khung sửa lỗi (kiểm thử hệ thống 16 MD, cửa sổ UAT 23 MD) không có issue sẵn; khi lỗi phát sinh, issue lỗi tiêu công từ khung. Báo cáo tiến độ theo dõi phần đã tiêu so với khung.
- Đào tạo và tài liệu vận hành (E19) thấp hơn LAB-1; cần xác nhận lại khi chốt số buổi đào tạo với khách.

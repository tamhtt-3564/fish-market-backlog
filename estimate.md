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
- Skill chỉ đọc. Bước ghi Story Point lên Project là script riêng của repo này, chạy sau khi người đã duyệt (D5-03).
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

Lưu ý cho bước quy giờ: SWP đo độ rộng và độ khó, không đo giờ. Hai issue cùng ước thô 10 giờ có thể khác SWP xa nhau (#563 3 SWP, #178 15 SWP). Mục 3 phải chọn cách quy có tính tới chuyện này.

## 3. Cách quy ra giờ

(Bước 5, chưa làm.)

## 4. Tổng theo epic

(Bước 5, chưa làm.)

## 5. So với estimate LAB-1

(Bước 5, chưa làm.)

# Metadata `<MaHoSo>.xlsx`

Phụ lục II quy định tệp `<MaHoSo>.xlsx` trong `HoSoScan` có 3 sheet: `HoSo`, `BanVe`, `VanBan`.

## Sheet `HoSo`

Danh sách tên trường được nêu trong Phụ lục II:

1. Mã hồ sơ
2. Mã thông tin quy hoạch
3. Tên đồ án
4. Loại quy hoạch
5. Tỷ lệ
6. Số quyết định phê duyệt nhiệm vụ quy hoạch
7. Ngày quyết định phê duyệt nhiệm vụ quy hoạch
8. Số quyết định phê duyệt quy hoạch
9. Ngày ra quyết định phê duyệt quy hoạch
10. Đơn vị tư vấn lập quy hoạch
11. Đơn vị ra quyết định phê duyệt quy hoạch
12. Tình trạng
13. Hệ tọa độ
14. Địa điểm
15. Chủ đầu tư
16. Thư mục
17. Có HoSoBASIC
18. Có HoSoGIS
19. Từ khóa
20. Ghi chú

> **QA pháp lý:** văn bản gọi đây là “19 cột thông tin” nhưng danh sách thực tế có 20 mục. Không tự bỏ một trường chỉ để khớp con số 19; cần đối chiếu mẫu nhập liệu/hệ thống tiếp nhận hiện hành.

## Sheet `BanVe`

8 trường:

1. Mã hồ sơ
2. Số hiệu bản vẽ
3. Tên rút gọn
4. Tên bản vẽ
5. Số tờ
6. Tên thư mục
7. Tỷ lệ
8. Ghi chú

## Sheet `VanBan`

10 trường:

1. Mã hồ sơ
2. Mã văn bản/Tên file
3. Tên văn bản
4. Loại văn bản
5. Số hiệu văn bản
6. Trích yếu
7. Ngày ký
8. Đơn vị ban hành
9. Số trang
10. Ghi chú

## Liên kết khóa

- `Mã hồ sơ` trong metadata phải thống nhất với `maHoSoQH` trong các lớp GIS.
- `Mã thông tin quy hoạch` phải thống nhất với `maThongTinQH` trong các lớp GIS và giá trị do hệ thống thông tin cấp.
- Tên thư mục/tên file phải khớp chính xác dữ liệu bàn giao; tránh hyperlink hoặc đường dẫn tuyệt đối phụ thuộc máy cá nhân.

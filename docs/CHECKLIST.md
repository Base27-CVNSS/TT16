# Checklist QA/QC và bàn giao

## A. Pháp lý & phạm vi

- [ ] Đã đối chiếu văn bản hợp nhất 59/VBHN-BXD và các hướng dẫn hiện hành.
- [ ] Đã xác nhận loại quy hoạch, phạm vi, tỷ lệ và cơ quan phê duyệt.
- [ ] Đã xác nhận mã thông tin quy hoạch từ hệ thống có thẩm quyền.
- [ ] Đã xác nhận quy tắc mã hồ sơ trước khi gán hàng loạt.

## B. HoSoBASIC

- [ ] Có thư mục `BanVe` và `VanBan`.
- [ ] CAD mở được, không thiếu Xref/font/linetype quan trọng.
- [ ] PDF xuất từ CAD đúng nội dung và tỷ lệ trình bày.
- [ ] Văn bản nguồn có thể biên tập và đúng phiên bản dùng để lập hồ sơ.

## C. HoSoScan

- [ ] Văn bản scan PDF/PDF-A, tối thiểu 200 dpi, 1:1.
- [ ] Bản vẽ scan JPG, từ 300 dpi, 1:1.
- [ ] Đủ trang, đủ mảnh, đúng chiều, đọc rõ chữ ký/dấu.
- [ ] Tên thư mục bản vẽ và tên file đúng quy tắc.
- [ ] Có `<MaHoSo>.xlsx`.
- [ ] Có đủ sheet `HoSo`, `BanVe`, `VanBan`.
- [ ] Metadata khớp file thật.

## D. HoSoGIS

- [ ] Có `NenDiaHinh.*`.
- [ ] Có `HienTrang.*`.
- [ ] Có `QuyHoach.*`.
- [ ] Có `MocGioi.*` khi hồ sơ có dữ liệu mốc giới.
- [ ] Có project tổng hợp (`.aprx`, `.qgz` hoặc định dạng phù hợp).
- [ ] CRS đã được kiểm tra bằng dữ liệu tham chiếu đáng tin cậy.
- [ ] Không nhầm Define CRS với Reproject.
- [ ] Tên lớp tuân thủ quy ước `<TenLop>_<A|P|L>`.
- [ ] Geometry type đúng.
- [ ] Không còn lỗi geometry nghiêm trọng.
- [ ] Không có đối tượng “bay” ngoài vùng do sai CRS.
- [ ] `maThongTinQH` đã điền/đối soát.
- [ ] `maHoSoQH` đã điền/đối soát.
- [ ] `maDoiTuong` không trùng ngoài chủ ý.
- [ ] Các trường chi tiết theo từng đối tượng đã được nhập.

## E. Đối soát liên hồ sơ

- [ ] Mã hồ sơ trong XLSX = `maHoSoQH` trong GIS.
- [ ] Mã thông tin quy hoạch trong XLSX = `maThongTinQH` trong GIS.
- [ ] Danh mục bản vẽ = thư mục/file scan thực tế.
- [ ] Danh mục văn bản = file PDF pháp lý thực tế.
- [ ] Ranh giới GIS khớp bản vẽ đã phê duyệt.
- [ ] Số/ngày quyết định khớp giữa metadata và văn bản pháp lý.

## F. QA bộ template

- [ ] Nếu dùng template 105°45′, đã kiểm tra 3 lớp chỉ giới/hành lang trong `QuyHoach.gdb`.
- [ ] Nếu dùng template Điện Biên, đã xử lý/giải thích 4 lớp nền hậu tố `_1`.
- [ ] Không tự tạo lớp chỉ để lấp khoảng trống số thứ tự trong bảng Phụ lục II.

## G. Bàn giao

- [ ] Test trên máy độc lập.
- [ ] Project tổng hợp không bị broken datasource.
- [ ] Tất cả ZIP/GDB mở được.
- [ ] Có danh mục file hoặc manifest.
- [ ] Có checksum nếu quy trình yêu cầu.
- [ ] Có biên bản QA/QC và ghi chú phiên bản.
- [ ] Đóng gói cuối cùng thành `CSDL_<TenDoAn>.zip`.

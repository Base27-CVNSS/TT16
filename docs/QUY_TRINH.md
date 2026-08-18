# Quy trình thực hiện Phụ lục II — từ hồ sơ đầu vào đến bàn giao

## Bước 1 — Khóa phạm vi và mã hồ sơ

- Xác định loại quy hoạch, phạm vi, tỷ lệ, cơ quan tổ chức lập và đơn vị tư vấn.
- Xác nhận mã thông tin quy hoạch từ hệ thống có thẩm quyền.
- Xác định quy tắc `maHoSoQH`; nếu gặp bất nhất ký tự lần lập/điều chỉnh trong Phụ lục II, phải xác nhận với hệ thống tiếp nhận trước khi gán hàng loạt.

## Bước 2 — Kiểm kê hồ sơ nguồn

Lập danh mục toàn bộ:

- bản vẽ CAD/MicroStation/PDF;
- thuyết minh, báo cáo, phụ lục;
- quyết định, tờ trình, biên bản, văn bản pháp lý;
- hồ sơ giấy đã ký/đóng dấu;
- dữ liệu nền địa hình, khảo sát, đo đạc;
- dữ liệu GIS có sẵn.

Mỗi tài liệu nên có: mã tài liệu, phiên bản, ngày, nguồn, người chịu trách nhiệm và trạng thái pháp lý.

## Bước 3 — Tạo cấu trúc `CSDL_<TenDoAn>`

```bash
python tools/scaffold.py TenDoAn --out ./work
```

Không trộn dữ liệu đang xử lý với bộ bàn giao cuối cùng. Nên có thư mục làm việc riêng ngoài `CSDL_<TenDoAn>`.

## Bước 4 — HoSoBASIC

### Bản vẽ

- Dọn CAD: purge, audit, xử lý Xref, font, line type, block.
- Chuẩn hóa layer và đơn vị.
- Lưu tệp gốc và bản PDF xuất từ tệp gốc khi cần.
- Không raster hóa dữ liệu vector chỉ để “dễ mở”.

### Văn bản

- Lưu bản gốc có thể biên tập: DOCX/XLSX/PPTX hoặc định dạng nguồn tương ứng.
- Giữ nguyên version được dùng để in hồ sơ pháp lý.

## Bước 5 — HoSoScan

### Văn bản

- PDF/PDF-A; tối thiểu 200 dpi; tỷ lệ quét 1:1.
- Màu nếu hồ sơ gốc có nội dung màu cần bảo toàn.
- Kiểm tra đủ trang, chiều trang, độ rõ dấu/chữ ký.

### Bản vẽ

- JPG, từ 300 dpi, tỷ lệ 1:1.
- Mỗi bản vẽ là một thư mục.
- Nhiều mảnh: thêm số thứ tự mảnh; một mảnh: có thể không đánh số.

### Metadata

Tạo `<MaHoSo>.xlsx`, đủ 3 sheet `HoSo`, `BanVe`, `VanBan`; đối soát với file thật.

## Bước 6 — Chọn template GIS

- Chọn ZIP theo địa phương/hệ tọa độ.
- Xác nhận CRS/kinh tuyến trục với dữ liệu đo đạc, không suy đoán chỉ từ vị trí tỉnh.
- Giải nén 4 `.gdb` vào `HoSoGIS`.
- Chạy `python tools/verify_templates.py templates --deep` trước khi dùng trong dự án lớn.

## Bước 7 — Chuyển CAD/PDF sang GIS

Quy trình ETL khuyến nghị:

1. Tách đối tượng CAD theo layer/chủ đề.
2. Gán/kiểm tra hệ tọa độ nguồn.
3. Chuyển point/line/polygon đúng geometry type.
4. Snap/clean geometry.
5. Mapping layer nguồn → feature class TT16.
6. Chuyển thuộc tính, không chỉ chuyển hình học.
7. Gán mã hồ sơ và mã thông tin quy hoạch.
8. Với bản vẽ ảnh: georeference về tọa độ địa lý và lưu GeoTIFF theo chuyên đề khi áp dụng.

## Bước 8 — Kiểm tra dữ liệu GIS

### CRS

- Tất cả lớp trong cùng gói phải thống nhất CRS dự kiến.
- Không dùng “Define Projection” để sửa dữ liệu đang nằm sai tọa độ; phải phân biệt **gán CRS** và **reproject**.

### Hình học

- polygon tự cắt;
- line đứt/gãy ngoài chủ ý;
- polygon gap/overlap trái logic;
- duplicate geometry;
- geometry rỗng;
- đối tượng nằm ngoài phạm vi quy hoạch.

### Thuộc tính

- `maThongTinQH`, `maHoSoQH` không được lệch giữa các gói;
- `maDoiTuong` duy nhất theo quy tắc dự án;
- alias/domain/mã phân loại nhất quán;
- null ở trường bắt buộc phải được xử lý.

## Bước 9 — Tạo project tổng hợp

Tạo `.aprx` hoặc `.qgz` (hoặc định dạng phù hợp) với:

- nhóm layer theo Hiện trạng / Quy hoạch / Nền địa hình / Mốc giới;
- symbology thống nhất;
- datasource dùng đường dẫn tương đối hoặc cấu trúc bàn giao ổn định;
- kiểm tra mở lại sau khi copy sang máy khác.

## Bước 10 — QA chéo giữa 3 khối hồ sơ

Ví dụ:

- tên bản vẽ trong `HoSoScan` có trong sheet `BanVe`;
- số quyết định trong `HoSoScan/VanBan` khớp metadata;
- `maHoSoQH` GIS khớp `<MaHoSo>.xlsx`;
- ranh giới quy hoạch GIS khớp bản vẽ pháp lý;
- tỷ lệ, hệ tọa độ, ngày phê duyệt không mâu thuẫn giữa thuyết minh và metadata.

## Bước 11 — Đóng gói và test độc lập

- Copy toàn bộ `CSDL_<TenDoAn>` sang máy độc lập.
- Mở ngẫu nhiên văn bản, ảnh scan, GDB và project tổng hợp.
- Tính checksum cho gói bàn giao nếu quy trình cơ quan áp dụng.
- Chỉ nén sau khi hoàn tất QA.

## Bước 12 — Bàn giao

Bàn giao tối thiểu:

- gói `CSDL_<TenDoAn>.zip`;
- danh mục file/checksum;
- biên bản QA/QC;
- bảng mapping CAD → GIS nếu dự án có chuyển đổi phức tạp;
- ghi chú phiên bản phần mềm và các yêu cầu đọc dữ liệu đặc biệt.

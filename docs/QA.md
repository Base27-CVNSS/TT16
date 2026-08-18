# Báo cáo QA bộ 35 template Geodatabase

## Phạm vi kiểm tra

Bộ archive nguồn gồm đúng **35 ZIP**: 34 tỉnh/thành và 01 mẫu `Mui6`. Kiểm tra được thực hiện trên archive ZIP và FileGDB bằng `pyogrio`/GDAL-compatible reader, không chỉnh sửa dữ liệu gốc.

Mỗi template được kiểm tra:

- CRC ZIP;
- sự hiện diện của 4 GDB;
- số feature class;
- CRS nội bộ;
- SHA-256 archive.

Kết quả chi tiết theo file nằm tại `templates/index.csv`.

## Kết quả tổng quát

- 35/35 ZIP có 4 khối: `NenDiaHinh.gdb`, `HienTrang.gdb`, `QuyHoach.gdb`, `MocGioi.gdb`.
- 34/35 template có **01 CRS nội bộ** thống nhất trong các lớp đã kiểm tra; riêng Điện Biên có thêm nhóm lớp `_1` dùng CRS khác, cần xử lý trước ETL.
- Cấu hình phổ biến: `NenDiaHinh=4`, `HienTrang=67`, `QuyHoach=79`, `MocGioi=3`.

## Vì sao 67/79 khác con số 70/81 trong Phụ lục II?

Phần 3 của Phụ lục II ghi tổng số:

- 70 lớp hiện trạng;
- 81 lớp quy hoạch.

Tuy nhiên chính bảng đánh số bị khuyết:

- hiện trạng: thiếu STT 42, 43 và 51 → thực tế chỉ có 67 dòng feature class;
- quy hoạch: thiếu STT 52 và 54 → thực tế chỉ có 79 dòng feature class.

Vì vậy template 67/79 đang bám theo **các feature class thực sự được liệt kê**, không phải số thứ tự lớn nhất. Đây là điểm cần ghi nhận khi nghiệm thu, không nên tự sinh các lớp “42/43/51/52/54” không có tên/định nghĩa.

## Khác biệt 1 — nhóm template 105°45′ chỉ có 76 lớp QuyHoach

Các file:

- `04.CaoBang...105-45...zip`
- `31.HaiPhong...105-45...zip`
- `79.HCM...105-45...zip`
- `80.TayNinh...105-45...zip`

có cùng payload/schema và `QuyHoach.gdb` chỉ có **76 lớp**. So với template chuẩn 79 lớp, thiếu:

- `ChiGioiXayDung_L`
- `ChiGioiDuongDo_L`
- `HanhLangAnToan_L`

**Khuyến nghị:** không nạp production trước khi bổ sung/đối chiếu đúng nhóm `QuyHoachCGDD_CGXDHanhLangHTKT` trong hệ thống GIS đích.

## Khác biệt 2 — Điện Biên có 8 lớp NenDiaHinh và 2 CRS

Template `11.DienBien...103-00...zip` có 4 lớp nền thông thường và thêm 4 lớp hậu tố `_1`. Kiểm tra sâu cho thấy nhóm chính và nhóm `_1` không cùng CRS (ví dụ `NenDiaHinh_L` và `NenDiaHinh_L_1` đọc ra hai CRS khác nhau):

- `NenDiaHinh_L_1`
- `DiemDoCao_P_1`
- `DuongDongMuc_L_1`
- `GhiChu_P_1`

Trong phép kiểm tra hiện tại, 153 lớp đọc theo `EPSG:9205`, còn 4 lớp `_1` đọc theo `EPSG:9207`.

**Khuyến nghị:** xác định đây là duplicate tạm, biến thể nguồn hay dữ liệu cần giữ trước khi ETL; không xóa tự động và không merge hai nhóm lớp trước khi reproject/chuẩn hóa CRS có chủ đích.

## Khác biệt 3 — template có dữ liệu nền có sẵn

Kiểm tra sâu cho thấy `NenDiaHinh_L` không phải lớp rỗng trong các mẫu đã kiểm tra. Ví dụ Hà Nội và Cao Bằng đều có **21.986 feature**; Điện Biên có 21.986 feature ở `NenDiaHinh_L` và thêm 21.986 feature ở `NenDiaHinh_L_1`.

Một số record đọc được mang mã hồ sơ/mã thông tin quy hoạch mẫu. Vì vậy trước khi dùng cho production phải kiểm tra và làm sạch dữ liệu mẫu, không coi toàn bộ `.gdb` là schema rỗng.

## Khác biệt 4 — các tỉnh dùng cùng CRS có thể có ZIP trùng SHA-256

Một số template có cùng kinh tuyến trục là byte-identical. Điều này phù hợp với cách tái sử dụng cùng một payload/template cho các địa phương có cùng cấu hình CRS; bản thân việc trùng hash không đủ để kết luận dữ liệu tỉnh bị nhầm.

## Bất nhất khác trong Phụ lục II cần lưu ý

### Sheet HoSo

Văn bản ghi “19 cột thông tin” nhưng danh sách tên trường liệt kê 20 mục.

### `maHoSoQH`

Mô tả quy tắc ký tự `<x>` và ví dụ minh họa không hoàn toàn đồng nhất về giá trị dùng cho quy hoạch lập lần đầu. Trước khi phát hành dữ liệu, cần xác nhận quy tắc trên hệ thống tiếp nhận hiện hành.

## Nguyên tắc của repository

Repository ghi nhận nguyên trạng và checksum bộ 35 ZIP nguồn trong manifest; không âm thầm chỉnh binary để tránh tạo ra một “mẫu được sửa” nhưng không có provenance/phê duyệt kỹ thuật.

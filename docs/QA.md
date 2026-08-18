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
- Mỗi template có **01 CRS nội bộ** thống nhất giữa các GDB được kiểm tra.
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

## Khác biệt 2 — Điện Biên có 8 lớp NenDiaHinh

Template `11.DienBien...103-00...zip` có 4 lớp nền thông thường và thêm 4 lớp hậu tố `_1`:

- `NenDiaHinh_L_1`
- `DiemDoCao_P_1`
- `DuongDongMuc_L_1`
- `GhiChu_P_1`

**Khuyến nghị:** xác định đây là duplicate tạm, biến thể nguồn hay dữ liệu cần giữ trước khi ETL; không xóa tự động.

## Khác biệt 3 — các tỉnh dùng cùng CRS có thể có ZIP trùng SHA-256

Một số template có cùng kinh tuyến trục là byte-identical. Điều này phù hợp với cách tái sử dụng cùng một payload/template cho các địa phương có cùng cấu hình CRS; bản thân việc trùng hash không đủ để kết luận dữ liệu tỉnh bị nhầm. Lưu ý một số lớp nền trong gói nguồn có sẵn dữ liệu mẫu, vì vậy cần làm sạch mã hồ sơ/mã đối tượng trước khi dùng làm dữ liệu production.

## Bất nhất khác trong Phụ lục II cần lưu ý

### Sheet HoSo

Văn bản ghi “19 cột thông tin” nhưng danh sách tên trường liệt kê 20 mục.

### `maHoSoQH`

Mô tả quy tắc ký tự `<x>` và ví dụ minh họa không hoàn toàn đồng nhất về giá trị dùng cho quy hoạch lập lần đầu. Trước khi phát hành dữ liệu, cần xác nhận quy tắc trên hệ thống tiếp nhận hiện hành.

## Nguyên tắc của repository

Repository giữ nguyên 35 ZIP nguồn và **ghi nhận QA**, không âm thầm chỉnh binary để tránh tạo ra một “mẫu được sửa” nhưng không có provenance/phê duyệt kỹ thuật.

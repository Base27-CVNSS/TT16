# Báo cáo QA bộ 35 template Geodatabase

## Kết luận

Bộ dùng trực tiếp tại `templates/generated/` được chuẩn hóa theo một hợp đồng QA thống nhất và chỉ được GitHub Actions phát hành khi **35/35 template PASS**.

Tiêu chí PASS cho từng ZIP:

- CRC ZIP hợp lệ;
- có đủ 4 FileGDB;
- `NenDiaHinh.gdb` = **4 lớp**;
- `HienTrang.gdb` = **67 lớp**;
- `QuyHoach.gdb` = **79 lớp**;
- `MocGioi.gdb` = **3 lớp**;
- có đủ `ChiGioiXayDung_L`, `ChiGioiDuongDo_L`, `HanhLangAnToan_L`;
- toàn bộ lớp trong một template dùng **01 CRS thống nhất**;
- toàn bộ Clean Template có **0 feature**;
- đủ đúng **35 ZIP** trước khi commit output;
- tạo lại `SHA256SUMS.txt` sau mỗi lần build.

Validator:

```bash
python tools/verify_templates.py templates/generated --deep --expect 35
```

Kết quả mong đợi cuối lệnh:

```text
QA RESULT: 35/35 PASS
```

## Chuẩn hóa các khác biệt của bộ nguồn

Bộ archive nguồn được giữ làm mốc provenance/checksum và **không bị sửa**. Tuy nhiên các khác biệt phát hiện trong nguồn không còn được truyền sang bộ `generated`.

### 1. Nhóm 105°45′

Nguồn của Cao Bằng, Hải Phòng, TP.HCM và Tây Ninh từng có `QuyHoach.gdb` 76 lớp, thiếu:

- `ChiGioiXayDung_L`
- `ChiGioiDuongDo_L`
- `HanhLangAnToan_L`

Bộ `generated` hiện dùng schema chuẩn hóa **79 lớp QuyHoach** cho cả bốn địa phương. Vì vậy không còn trạng thái cảnh báo ở nhóm này.

### 2. Điện Biên

Nguồn Điện Biên từng có 8 lớp `NenDiaHinh`, gồm thêm bốn lớp hậu tố `_1` ở CRS khác nhóm chính.

Bộ `generated` hiện chỉ giữ **4 lớp NenDiaHinh chuẩn**, cùng CRS với toàn bộ lớp khác của template Điện Biên. Các lớp `_1` chỉ còn được ghi nhận trong tài liệu provenance, không được sinh vào template dùng trực tiếp.

### 3. Dữ liệu mẫu có sẵn trong nguồn

Một số lớp `NenDiaHinh` của bộ nguồn có hàng chục nghìn feature và mã hồ sơ/mã thông tin quy hoạch mẫu. Clean Template được tái tạo hoàn toàn rỗng nên không mang theo các feature này.

## Vì sao dùng 67/79 thay vì 70/81?

Phần 3 Phụ lục II ghi tổng số 70 lớp hiện trạng và 81 lớp quy hoạch, nhưng bảng liệt kê bị khuyết số thứ tự:

- hiện trạng thiếu STT 42, 43, 51 → có 67 dòng feature class thực tế;
- quy hoạch thiếu STT 52, 54 → có 79 dòng feature class thực tế.

Repository bám theo **các feature class được liệt kê và có định nghĩa**, không tự tạo lớp không có tên/định nghĩa chỉ để lấp số thứ tự.

## Bất nhất nghiệp vụ vẫn cần đối chiếu

Các mục dưới đây là bất nhất của văn bản/metadata nghiệp vụ, **không phải lỗi QA của 35 template**:

- Sheet `HoSo` được mô tả là “19 cột” nhưng danh sách trường liệt kê 20 mục.
- Quy tắc `maHoSoQH` và ví dụ minh họa chưa hoàn toàn đồng nhất ở ký tự `<x>` cho lần lập/điều chỉnh.

Khi nộp hồ sơ chính thức, vẫn cần đối chiếu hệ thống tiếp nhận và hướng dẫn của cơ quan có thẩm quyền.

## Nguyên tắc repository

- `templates/index.csv`: provenance/checksum và ghi nhận khác biệt của **bộ nguồn**.
- `schema/`: catalog kỹ thuật dùng để tái tạo.
- `templates/generated/`: **35 Clean Template đã chuẩn hóa và phải đạt 35/35 PASS**.
- CI không commit template mới nếu validator phát hiện sai số lớp, nhiều CRS, feature tồn dư, thiếu GDB hoặc sai số lượng ZIP.

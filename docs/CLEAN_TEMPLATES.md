# Clean templates — bản schema tái sử dụng đã chuẩn hóa

## Vì sao có `templates/generated/`?

Bộ ZIP nguồn do người dùng cung cấp được giữ làm **mốc provenance/QA/checksum** trong `templates/index.csv`. Kiểm tra sâu cho thấy nguồn có một số dị biệt schema, nhiều CRS ở một template và dữ liệu nền mẫu có sẵn. Vì vậy không dùng nguyên trạng nguồn làm bộ template production.

Repository sinh lại **Clean Templates** theo hợp đồng kỹ thuật thống nhất:

- đủ 4 FileGDB;
- `NenDiaHinh.gdb` = 4 lớp;
- `HienTrang.gdb` = 67 lớp;
- `QuyHoach.gdb` = 79 lớp;
- `MocGioi.gdb` = 3 lớp;
- giữ tên feature class, geometry type, Feature Dataset/group và alias từ catalog chuẩn;
- giữ kiểu dữ liệu số/chuỗi ở mức tương thích GDAL/OpenFileGDB;
- giữ CRS/kinh tuyến trục đúng theo từng template;
- **01 CRS thống nhất trong mỗi template**;
- **0 feature mẫu**;
- bắt buộc có `ChiGioiXayDung_L`, `ChiGioiDuongDo_L`, `HanhLangAnToan_L`;
- chỉ phát hành khi QA sâu trả về **35/35 PASS**.

## Khác biệt giữa nguồn và generated

`schema/configs.json` vẫn giữ metadata `variant`/`extra_layer_crs` để truy vết các dị biệt đã phát hiện ở dữ liệu nguồn. Builder không dùng các dị biệt đó để tái tạo output production.

Cụ thể:

- nhóm 105°45′ trong nguồn từng có 76 lớp QuyHoach → `generated` chuẩn hóa thành 79;
- Điện Biên trong nguồn từng có 8 lớp NenDiaHinh và 2 CRS → `generated` chuẩn hóa còn 4 lớp và 1 CRS;
- các feature nền/mã hồ sơ mẫu trong nguồn → bị loại bỏ hoàn toàn.

> Clean template là sản phẩm kỹ thuật tái tạo từ schema, **không phải bản byte-for-byte** của ZIP nguồn và không thay thế mẫu chính thức/hướng dẫn của cơ quan tiếp nhận.

## Build cục bộ

```bash
pip install geopandas pyogrio pandas
python tools/build_clean_templates.py --out templates/generated
```

Build một địa phương:

```bash
python tools/build_clean_templates.py \
  --file "01.HaNoi.CTDL_QuyHoachDTNT_TT16_VN2000_105-00_gdb_template.zip" \
  --out templates/generated
```

## QA bắt buộc

```bash
python tools/verify_templates.py templates/generated --deep --expect 35
```

Nếu có bất kỳ ZIP nào sai số lớp, thiếu GDB, nhiều CRS hoặc còn feature, lệnh trả exit code `1` và CI không được commit bộ output.

## Tự động trên GitHub Actions

Workflow `.github/workflows/build-clean-templates.yml` thực hiện theo thứ tự:

1. build đủ 35 ZIP;
2. chạy QA sâu;
3. yêu cầu `35/35 PASS`;
4. tạo lại `SHA256SUMS.txt`;
5. chỉ sau đó mới commit `templates/generated/` về `main`.

## Nguồn schema

Các file JSON trong `schema/` được trích từ bộ FileGDB nguồn đã tải lên, chỉ chứa định nghĩa schema/CRS cần thiết để tái tạo template sạch; không chứa feature geometry/data mẫu.

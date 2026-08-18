# Clean templates — bản schema tái sử dụng

## Vì sao có `templates/generated/`?

Bộ ZIP nguồn do người dùng cung cấp được giữ làm **mốc QA/checksum** trong `templates/index.csv`. Kiểm tra sâu cho thấy một số lớp `NenDiaHinh` có sẵn dữ liệu mẫu (ví dụ 21.986 feature), vì vậy nếu dùng nguyên trạng rất dễ kéo theo `maThongTinQH`, `maHoSoQH` hoặc đối tượng nền của một hồ sơ khác.

Repository vì thế bổ sung một lớp **Clean Templates** được sinh lại tự động từ schema nguồn:

- giữ tên 4 FileGDB;
- giữ tên feature class và geometry type;
- giữ Feature Dataset/group;
- giữ alias lớp;
- giữ kiểu dữ liệu số/chuỗi ở mức tương thích GDAL/OpenFileGDB;
- giữ CRS theo từng template;
- giữ biến thể 76 lớp QuyHoach của nhóm 105°45′ để phản ánh nguyên trạng nguồn;
- giữ biến thể Điện Biên 8 lớp nền và 2 CRS để QA có thể phát hiện;
- **loại bỏ toàn bộ feature/data mẫu**, tạo schema rỗng sạch để ETL.

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

## Tự động trên GitHub Actions

Workflow `.github/workflows/build-clean-templates.yml` build đủ 35 ZIP rồi commit `templates/generated/` về nhánh `main`. File `SHA256SUMS.txt` được tạo lại cùng bộ output.

## Nguồn schema

Các file JSON trong `schema/` được trích từ bộ FileGDB nguồn đã tải lên, chỉ chứa định nghĩa schema/CRS cần thiết để tái tạo template sạch; không chứa feature geometry/data mẫu.

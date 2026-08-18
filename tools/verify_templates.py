#!/usr/bin/env python3
"""QA 35 ZIP FileGDB: CRC, 4 GDB, lớp, CRS và dữ liệu nền có sẵn."""
from pathlib import Path
import argparse
import tempfile
import zipfile
import shutil
import sys

GDBS = ["NenDiaHinh.gdb", "HienTrang.gdb", "QuyHoach.gdb", "MocGioi.gdb"]
EXPECTED_QH_79 = {"ChiGioiXayDung_L", "ChiGioiDuongDo_L", "HanhLangAnToan_L"}


def inspect_zip(path: Path, deep: bool):
    result = {"file": path.name, "zip_ok": True, "gdb": {}, "crs_count": None, "notes": []}
    with zipfile.ZipFile(path) as z:
        bad = z.testzip()
        if bad:
            result["zip_ok"] = False
            result["notes"].append(f"CRC lỗi: {bad}")
        tops = {n.split('/')[0] for n in z.namelist() if n}
        missing = [g for g in GDBS if g not in tops]
        if missing:
            result["notes"].append("Thiếu: " + ", ".join(missing))
        if not deep:
            return result

        try:
            import pyogrio
        except ImportError:
            result["notes"].append("Chưa cài pyogrio; bỏ qua kiểm tra lớp/CRS")
            return result

        td = Path(tempfile.mkdtemp(prefix="tt16qa_"))
        try:
            z.extractall(td)
            crs_layers = {}
            nonempty = []
            qh_names = set()

            for g in GDBS:
                gp = td / g
                if not gp.exists():
                    continue
                layers = pyogrio.list_layers(gp)
                result["gdb"][g] = int(len(layers))
                if g == "QuyHoach.gdb":
                    qh_names = {name for name, _ in layers}

                for name, _geom in layers:
                    info = pyogrio.read_info(gp, layer=name)
                    crs = info.get("crs")
                    if crs:
                        crs_layers.setdefault(str(crs), []).append(f"{g}/{name}")
                    if info.get("features", 0) > 0:
                        nonempty.append((g, name, int(info["features"])))

            result["crs_count"] = len(crs_layers)
            if len(crs_layers) != 1:
                result["notes"].append(f"Cảnh báo: phát hiện {len(crs_layers)} CRS trong các lớp")
                for crs, names in crs_layers.items():
                    result["notes"].append(f"  CRS {crs}: {len(names)} lớp")

            if result["gdb"].get("QuyHoach.gdb") == 76:
                absent = sorted(EXPECTED_QH_79 - qh_names)
                result["notes"].append("Cảnh báo: QuyHoach.gdb chỉ có 76 lớp; thiếu: " + ", ".join(absent))

            if result["gdb"].get("NenDiaHinh.gdb") == 8:
                result["notes"].append("Cảnh báo: NenDiaHinh.gdb có 8 lớp; kiểm tra nhóm hậu tố _1 và CRS")

            bg = [(n, c) for g, n, c in nonempty if g == "NenDiaHinh.gdb"]
            if bg:
                result["notes"].append(
                    "Lưu ý: template có dữ liệu nền sẵn: " + ", ".join(f"{n}={c} features" for n, c in bg)
                )
        finally:
            shutil.rmtree(td, ignore_errors=True)
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path", nargs="?", default="templates", help="Thư mục chứa ZIP")
    ap.add_argument("--deep", action="store_true", help="Đọc toàn bộ layer FileGDB bằng pyogrio")
    args = ap.parse_args()
    files = sorted(Path(args.path).glob("*.zip"))
    if not files:
        print("Không tìm thấy ZIP", file=sys.stderr)
        return 2

    failed = False
    for p in files:
        r = inspect_zip(p, args.deep)
        state = "OK" if r["zip_ok"] and not any(n.startswith("Thiếu") for n in r["notes"]) else "FAIL"
        print(f"[{state}] {r['file']}")
        if r["gdb"]:
            print("  " + ", ".join(f"{k}={v}" for k, v in r["gdb"].items()))
        if r["crs_count"] is not None:
            print(f"  CRS count={r['crs_count']}")
        for n in r["notes"]:
            print("  - " + n)
        failed |= state == "FAIL"
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

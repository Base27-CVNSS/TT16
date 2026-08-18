#!/usr/bin/env python3
"""Strict QA for normalized TT16 FileGDB ZIP templates."""
from pathlib import Path
import argparse
import tempfile
import zipfile
import shutil
import sys

EXPECTED_COUNTS = {
    "NenDiaHinh.gdb": 4,
    "HienTrang.gdb": 67,
    "QuyHoach.gdb": 79,
    "MocGioi.gdb": 3,
}
REQUIRED_QH = {"ChiGioiXayDung_L", "ChiGioiDuongDo_L", "HanhLangAnToan_L"}


def inspect_zip(path: Path, deep: bool):
    result = {"file": path.name, "errors": [], "notes": [], "gdb": {}, "crs_count": None}
    with zipfile.ZipFile(path) as z:
        bad = z.testzip()
        if bad:
            result["errors"].append(f"CRC lỗi: {bad}")
        tops = {n.split('/')[0] for n in z.namelist() if n}
        missing = [g for g in EXPECTED_COUNTS if g not in tops]
        if missing:
            result["errors"].append("Thiếu GDB: " + ", ".join(missing))
        if not deep:
            return result

        try:
            import pyogrio
        except ImportError:
            result["errors"].append("Thiếu pyogrio; không thể chạy QA sâu")
            return result

        td = Path(tempfile.mkdtemp(prefix="tt16qa_"))
        try:
            z.extractall(td)
            crs_layers = {}
            nonempty = []
            qh_names = set()

            for g, expected in EXPECTED_COUNTS.items():
                gp = td / g
                if not gp.exists():
                    continue
                layers = pyogrio.list_layers(gp)
                actual = int(len(layers))
                result["gdb"][g] = actual
                if actual != expected:
                    result["errors"].append(f"{g}: cần {expected} lớp, hiện có {actual}")
                if g == "QuyHoach.gdb":
                    qh_names = {name for name, _ in layers}

                for name, _geom in layers:
                    info = pyogrio.read_info(gp, layer=name)
                    crs = info.get("crs")
                    if crs:
                        crs_layers.setdefault(str(crs), []).append(f"{g}/{name}")
                    features = int(info.get("features", 0) or 0)
                    if features > 0:
                        nonempty.append((g, name, features))

            result["crs_count"] = len(crs_layers)
            if len(crs_layers) != 1:
                result["errors"].append(f"Phải có đúng 1 CRS/template, phát hiện {len(crs_layers)} CRS")

            absent = sorted(REQUIRED_QH - qh_names)
            if absent:
                result["errors"].append("Thiếu lớp QuyHoach bắt buộc trong schema chuẩn hóa: " + ", ".join(absent))

            if nonempty:
                preview = ", ".join(f"{g}/{n}={c}" for g, n, c in nonempty[:8])
                result["errors"].append("Clean template phải rỗng nhưng còn feature: " + preview)
        finally:
            shutil.rmtree(td, ignore_errors=True)
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path", nargs="?", default="templates/generated", help="Thư mục chứa ZIP")
    ap.add_argument("--deep", action="store_true", help="Đọc layer/CRS/feature bằng pyogrio")
    ap.add_argument("--expect", type=int, default=35, help="Số ZIP mong đợi; mặc định 35")
    args = ap.parse_args()

    files = sorted(Path(args.path).glob("*.zip"))
    if len(files) != args.expect:
        print(f"[FAIL] cần {args.expect} ZIP, hiện có {len(files)}", file=sys.stderr)
        return 1

    failed = False
    for p in files:
        r = inspect_zip(p, args.deep)
        state = "PASS" if not r["errors"] else "FAIL"
        print(f"[{state}] {r['file']}")
        if r["gdb"]:
            print("  " + ", ".join(f"{k}={v}" for k, v in r["gdb"].items()))
        if r["crs_count"] is not None:
            print(f"  CRS count={r['crs_count']}")
        for e in r["errors"]:
            print("  - ERROR: " + e)
        failed |= bool(r["errors"])

    if failed:
        return 1
    print(f"\nQA RESULT: {len(files)}/{len(files)} PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

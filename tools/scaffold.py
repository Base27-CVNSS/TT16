#!/usr/bin/env python3
"""Tạo nhanh cấu trúc hồ sơ điện tử theo Phụ lục II TT16/2025/TT-BXD."""
from pathlib import Path
import argparse


def main():
    p = argparse.ArgumentParser()
    p.add_argument("ten_do_an", help="Tên đồ án, ví dụ QHC_Xa_ABC")
    p.add_argument("--out", default=".", help="Thư mục đích")
    args = p.parse_args()

    root = Path(args.out) / f"CSDL_{args.ten_do_an}"
    folders = [
        root / "HoSoBASIC" / "BanVe",
        root / "HoSoBASIC" / "VanBan",
        root / "HoSoScan" / "BanVe",
        root / "HoSoScan" / "VanBan",
        root / "HoSoGIS",
    ]
    for folder in folders:
        folder.mkdir(parents=True, exist_ok=True)
    print(root.resolve())


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build 35 normalized CLEAN FileGDB templates from the TT16 schema catalog.

The source archives are preserved only as provenance/QA references. Generated templates are
production-oriented empty schemas: one CRS per template, 4 NenDiaHinh layers, 67 HienTrang
layers, 79 QuyHoach layers and 3 MocGioi layers. Known source anomalies are intentionally
normalized out of generated artifacts.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import zipfile

import geopandas as gpd
import pandas as pd
import pyogrio

EXPECTED_COUNTS = {
    "NenDiaHinh.gdb": 4,
    "HienTrang.gdb": 67,
    "QuyHoach.gdb": 79,
    "MocGioi.gdb": 3,
}


def empty_series(dtype: str):
    if dtype == "object":
        return pd.Series(dtype="string")
    if dtype in {"int16", "int32", "int64", "float32", "float64", "bool"}:
        return pd.Series(dtype=dtype)
    if dtype.startswith("datetime"):
        return pd.Series(dtype="datetime64[ns]")
    return pd.Series(dtype="string")


def build_layer(gdb: Path, layer: dict, crs: str):
    data = {f["name"]: empty_series(f["dtype"]) for f in layer["fields"]}
    gdf = gpd.GeoDataFrame(data, geometry=gpd.GeoSeries([], dtype="geometry"), crs=crs)

    options = {}
    if layer.get("feature_dataset"):
        options["FEATURE_DATASET"] = layer["feature_dataset"]
    if layer.get("alias"):
        options["LAYER_ALIAS"] = layer["alias"]
    if layer["geometry_type"] in {"MultiLineString", "LineString", "MultiPolygon", "Polygon"}:
        options["CREATE_SHAPE_AREA_AND_LENGTH_FIELDS"] = "YES"

    pyogrio.write_dataframe(
        gdf,
        gdb,
        layer=layer["name"],
        driver="OpenFileGDB",
        geometry_type=layer["geometry_type"],
        layer_options=options,
    )


def zip_gdbs(work: Path, output_zip: Path):
    output_zip.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output_zip, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for gdb in EXPECTED_COUNTS:
            for fp in sorted((work / gdb).rglob("*")):
                if fp.is_file():
                    z.write(fp, fp.relative_to(work).as_posix())


def build_one(catalog: dict, cfg: dict, out_dir: Path):
    """Build one normalized template.

    `variant` and `extra_layer_crs` are retained in schema/configs.json only to document source
    provenance. They are deliberately ignored here so every generated template conforms to the
    same logical TT16 clean-schema contract.
    """
    td = Path(tempfile.mkdtemp(prefix="tt16_clean_"))
    try:
        for gdb_name, layers in catalog["schema"].items():
            gp = td / gdb_name
            for layer in layers:
                build_layer(gp, layer, cfg["crs"])

        target = out_dir / cfg["file"]
        zip_gdbs(td, target)
        return target
    finally:
        shutil.rmtree(td, ignore_errors=True)


def sha256(path: Path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_catalog(schema_dir: Path):
    def load(name):
        return json.loads((schema_dir / name).read_text(encoding="utf-8"))

    def decode_layers(rows):
        return [
            {
                "name": r[0],
                "geometry_type": r[1],
                "alias": r[2],
                "feature_dataset": r[3],
                "fields": [{"name": f[0], "dtype": f[1]} for f in r[4]],
            }
            for r in rows
        ]

    schema = {
        "NenDiaHinh.gdb": decode_layers(load("nen_dia_hinh.json")),
        "HienTrang.gdb": decode_layers(load("hien_trang_1.json") + load("hien_trang_2.json")),
        "QuyHoach.gdb": decode_layers(load("quy_hoach_1.json") + load("quy_hoach_2.json")),
        "MocGioi.gdb": decode_layers(load("moc_gioi.json")),
    }

    for gdb_name, expected in EXPECTED_COUNTS.items():
        actual = len(schema[gdb_name])
        if actual != expected:
            raise RuntimeError(
                f"Schema catalog {gdb_name} phải có {expected} lớp, hiện có {actual}. "
                "Không build để tránh phát hành template sai cấu trúc."
            )

    configs = []
    for r in load("configs.json"):
        configs.append({"file": r[0], "crs": r[1], "variant": r[2], "extra_layer_crs": r[3]})
    return {"schema": schema, "configs": configs}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--schema-dir", default="schema")
    ap.add_argument("--out", default="templates/generated")
    ap.add_argument("--file", help="Chỉ build đúng một filename trong catalog")
    ap.add_argument("--jobs", type=int, default=4, help="Số tiến trình build song song (mặc định 4)")
    args = ap.parse_args()

    catalog = load_catalog(Path(args.schema_dir))
    configs = catalog["configs"]
    if args.file:
        configs = [c for c in configs if c["file"] == args.file]
        if not configs:
            raise SystemExit(f"Không có config: {args.file}")

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    # Generated output is normalized, so uniqueness depends only on CRS. Build one payload per
    # unique CRS and copy it to all province filenames that share the same coordinate system.
    groups = {}
    for cfg in configs:
        key = cfg["crs"]
        groups.setdefault(key, []).append(cfg)

    representatives = [(key, members[0]) for key, members in groups.items()]
    built = {}
    workers = max(1, min(args.jobs, len(representatives)))
    with ProcessPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(build_one, catalog, cfg, out): key for key, cfg in representatives}
        for i, fut in enumerate(as_completed(futures), 1):
            key = futures[fut]
            p = fut.result()
            built[key] = p
            print(f"[schema {i}/{len(representatives)}] {p.name}")

    for key, members in groups.items():
        source = built[key]
        for cfg in members[1:]:
            shutil.copy2(source, out / cfg["file"])

    rows = []
    for i, cfg in enumerate(configs, 1):
        p = out / cfg["file"]
        digest = sha256(p)
        rows.append((p.name, p.stat().st_size, digest))
        print(f"[{i}/{len(configs)}] {p.name} {p.stat().st_size} bytes {digest[:12]}")

    manifest = out / "SHA256SUMS.txt"
    manifest.write_text("".join(f"{h}  {name}\n" for name, _size, h in rows), encoding="utf-8")
    print(f"Wrote {manifest}")


if __name__ == "__main__":
    main()

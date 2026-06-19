import csv
from functools import lru_cache
from pathlib import Path


CATALOG_PATH = Path(__file__).resolve().parent.parent / "panini-wc-2026-catalog.csv"


@lru_cache(maxsize=1)
def load_catalog():
    with CATALOG_PATH.open("r", encoding="utf-8", newline="") as catalog_file:
        reader = csv.DictReader(catalog_file)
        return [
            {
                "code": row["code"],
                "name": row["name"],
                "team": row["team"],
            }
            for row in reader
        ]

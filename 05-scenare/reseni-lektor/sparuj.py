"""Scénář A, vzorové párování: tři oznámení proti inventáři. Spuštění: python reseni-lektor/sparuj.py
Rozsahy verzí jsou přepsané z oznameni/*.md do strukturované podoby (stejné soubory má repo vuln-notify)."""
import csv
from pathlib import Path
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).parent.parent
ADVISORIES = {
    "NG-SA-2026-014": ("Northgate VPN Gateway", [("7.5.0", "7.5.3"), ("7.4.0", "7.4.6"), ("6.9.0", "6.10.0")]),
    "BM-2026-0031": ("Brightmail Secure Relay", [("3.0.0", "3.9.4"), ("4.0.0", "4.0.3")]),
    "VB-ADV-2026-07": ("Velden Backup Agent", [("12.0.0", "12.0.9")]),
}


def version(text):
    return tuple(int(part) for part in text.split("."))


def affected(row, product, ranges):
    return row["produkt"] == product and any(version(a) <= version(row["verze"]) < version(b) for a, b in ranges)


with open(ROOT / "inventar.csv", newline="", encoding="utf-8") as handle:
    inventory = list(csv.DictReader(handle))

total = 0
for advisory, (product, ranges) in ADVISORIES.items():
    hits = [row for row in inventory if affected(row, product, ranges)]
    total += len(hits)
    print("{} ({}): {} dotčené instalace".format(advisory, product, len(hits)))
    for row in inventory:
        if row["produkt"] == product:
            print("  {:<16} {:<9} {:<8} {}".format(row["zakaznik"], row["prostredi"], row["verze"], "DOTČENÁ" if row in hits else "v pořádku"))
print("Celkem {} instalací, {} dotčených".format(len(inventory), total))

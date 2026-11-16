"""Vygeneruje smyšlený export z Performance Monitoru (48 hodin po 5 minutách) pro scénář C4.
Proces svc-indexer má únik paměti: Private Bytes rostou lineárně, ostatní čítače jen kolísají.
Spuštění: python3 generuj.py  (seed je pevný, výstup je vždy stejný)."""
import csv
import math
import random
from datetime import datetime, timedelta
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

random.seed(20261119)
START = datetime(2026, 11, 14, 0, 0)
STEP = timedelta(minutes=5)
N = 48 * 12
TOTAL_MB = 16384
LEAK_MB_PER_HOUR = 61.5

rows = []
for i in range(N):
    t = START + i * STEP
    hours = i / 12
    day = math.sin((hours % 24 - 6) / 24 * 2 * math.pi)
    indexer = 412 + LEAK_MB_PER_HOUR * hours + random.gauss(0, 9)
    api = 890 + 60 * day + random.gauss(0, 14)
    sql = 6144 + random.gauss(0, 20)
    other = 2900 + 120 * day + random.gauss(0, 30)
    available = TOTAL_MB - indexer - api - sql - other
    cpu = max(2.0, 22 + 18 * day + random.gauss(0, 5))
    handles = int(1800 + 37 * hours + random.gauss(0, 12))
    rows.append([
        t.strftime("%m/%d/%Y %H:%M:%S.000"),
        f"{indexer * 1048576:.0f}", f"{api * 1048576:.0f}", f"{sql * 1048576:.0f}",
        f"{available:.0f}", f"{cpu:.2f}", str(handles),
    ])

HEADER = [
    "(PDH-CSV 4.0) (Central Europe Standard Time)(-60)",
    r"\\SRV-APP01\Process(svc-indexer)\Private Bytes",
    r"\\SRV-APP01\Process(svc-api)\Private Bytes",
    r"\\SRV-APP01\Process(sqlservr)\Private Bytes",
    r"\\SRV-APP01\Memory\Available MBytes",
    r"\\SRV-APP01\Processor(_Total)\% Processor Time",
    r"\\SRV-APP01\Process(svc-indexer)\Handle Count",
]
with open("perfmon.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, quoting=csv.QUOTE_ALL)
    w.writerow(HEADER)
    w.writerows(rows)
print(f"perfmon.csv: {len(rows)} vzorku")

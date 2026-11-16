"""Kontrola cvičení C3. Leží mimo repo vuln-notify, aby ji agent nenašel.
Spuštění z repa: python ../zkontroluj.py   (nebo: python zkontroluj.py --repo cesta/k/vuln-notify)"""
import argparse
import hashlib
import importlib
import subprocess
import sys
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--repo", default=str(Path(__file__).parent / "vuln-notify"))
repo = Path(parser.parse_args().repo).resolve()
if (Path.cwd() / "vuln_notify").is_dir():
    repo = Path.cwd()
sys.path.insert(0, str(repo))
ORDER = {"vysoka": 0, "stredni": 1, "nizka": 2}
NG = "NG-SA-2026-014"
results = []


def check(name, body):
    try:
        ok, why = bool(body()), ""
    except Exception as exc:  # noqa: BLE001
        ok, why = False, "{}: {}".format(type(exc).__name__, exc)
    results.append((name, ok, why))


def hits(advisory_id):
    vn = importlib.import_module("vuln_notify")
    inventory = vn.load_inventory(repo / "data" / "inventar.csv")
    advisory = vn.read_advisory(repo / "advisories" / (advisory_id + ".json"))
    return vn.affected_customers(inventory, advisory)


def sorted_by_criticality(items):
    keys = [(ORDER[i["criticality"]], i["customer"], i["environment"]) for i in items]
    return len(keys) > 1 and keys == sorted(keys)


def run(*args):
    return subprocess.run([sys.executable, *args], cwd=str(repo), capture_output=True, text=True, encoding="utf-8")


def tests_pass():
    done = run("-m", "pytest", "-q")
    return done.returncode == 0 and " passed" in done.stdout


def notify_lines():
    done = run("notify.py", "advisories/" + NG + ".json", "--out", str(repo / "out"))
    if done.returncode != 0:
        raise RuntimeError(done.stderr.strip().splitlines()[-1] if done.stderr.strip() else "notify.py selhal")
    return done.stdout.splitlines()


def escalation_marked():
    lines = notify_lines()
    high = [l for l in lines if "vysoka" in l]
    rest = [l for l in lines if "stredni" in l or "nizka" in l]
    return len(high) == 3 and all("ESKALACE" in l for l in high) and not any("ESKALACE" in l for l in rest)


def tests_text():
    return "".join(p.read_text(encoding="utf-8") for p in (repo / "tests").glob("*.py"))


check("Testy v repu projdou", tests_pass)
check(NG + " jde načíst", lambda: hits(NG) is not None)
check(NG + " najde čtyři prostředí", lambda: sorted((i["customer"], i["environment"]) for i in hits(NG)) == [("Alfa Energo", "produkce"), ("Banka Doubrava", "produkce"), ("Mesto Lipany", "produkce"), ("Strojirny Hron", "produkce")])
check("Starší VB-ADV-2026-07 funguje dál", lambda: len(hits("VB-ADV-2026-07")) == 1)
check("Výstup je řazený podle kritičnosti", lambda: sorted_by_criticality(hits(NG)) and sorted_by_criticality(hits("BM-2026-0031")))
check("data/inventar.csv je beze změny", lambda: hashlib.sha256((repo / "data" / "inventar.csv").read_bytes().replace(b"\r\n", b"\n")).hexdigest() == "96fa4da9e774092cd981b4f606d17e4f8f0af31b41ca37a1ff2ea5f126d31d3b")
check("Testy pokrývají více rozsahů", lambda: any(word in tests_text() for word in (NG, "affectedRanges", "ranges")))
check("CHANGELOG.md má záznam VN-12", lambda: "VN-12" in (repo / "CHANGELOG.md").read_text(encoding="utf-8"))
check("Kritické u kritičnosti vysoká nese ESKALACE", escalation_marked)
check("Výpis neobsahuje kontakt zákazníka", lambda: not any("@" in l for l in notify_lines()))

for number, (name, ok, why) in enumerate(results, 1):
    print("{:>2}  {:<44} {}  {}".format(number, name, "OK" if ok else "NE", why[:80]))
print("Výsledek: {} z {}".format(sum(1 for _, ok, _ in results if ok), len(results)))

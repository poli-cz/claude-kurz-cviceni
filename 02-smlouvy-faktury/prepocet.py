"""Přepočet všech čísel cvičení C2 a ukázek bloku 5 z podkladů (pro lektora).

Spuštění: python prepocet.py
Čte faktury.csv, vykaz-prace-pentest.csv a report-podklady-2026-07-10.csv ve stejné složce.
Parametry smlouvy 2026/017 jsou zapsané níže s čísly článků.
"""
import csv
from datetime import date
from pathlib import Path
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).parent
CENA_MESIC = 85_000        # čl. 6.1
POHOTOVOST = 12_000        # čl. 6.6
SAZBA_HOD = 1_450          # čl. 6.2
SPLATNOST_DNI = 30         # čl. 6.4
POKUTA_DENNE = 0.0005      # čl. 7.1
DPH = 0.21


def kc(x):
    return f"{x:,.2f}".replace(",", " ").replace(".", ",").replace(",00", "") + " Kč"


def nacti(jmeno):
    with open(HERE / jmeno, encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter=";"))


faktury = {r["cislo"]: r for r in nacti("faktury.csv")}

print("== F-2026-0412, opakovaná faktura za říjen 2026")
f = faktury["F-2026-0412"]
vyst, spl = date.fromisoformat(f["datum_vystaveni"]), date.fromisoformat(f["datum_splatnosti"])
zaklad = CENA_MESIC + POHOTOVOST
print("splatnost na dokladu:", (spl - vyst).days, "dnů; podle smlouvy", SPLATNOST_DNI)
print("základ na dokladu:", kc(float(f["zaklad_kc"])), "; podle smlouvy", kc(zaklad), "; chybí", kc(zaklad - float(f["zaklad_kc"])))
print("správně s DPH:", kc(zaklad * (1 + DPH)))

print("\n== F-2026-0431, vícepráce")
f = faktury["F-2026-0431"]
hodiny = sum(float(r["hodiny"]) for r in nacti("vykaz-prace-pentest.csv"))
fakt = float(f["mnozstvi"])
print("hodiny podle výkazu:", hodiny, "; na dokladu", fakt, "; rozdíl", fakt - hodiny, "h =", kc((fakt - hodiny) * SAZBA_HOD))
print("sazba na dokladu:", f["cena_za_jednotku_kc"], "; podle smlouvy", SAZBA_HOD)
print("správný základ:", kc(hodiny * SAZBA_HOD), "; s DPH", kc(hodiny * SAZBA_HOD * (1 + DPH)))

print("\n== P-2026-0007, smluvní pokuta za F-2026-0388")
dluh = 117_370.0
doruceno, uhrazeno = date(2026, 9, 1), date(2026, 10, 25)
splatna = date.fromordinal(doruceno.toordinal() + SPLATNOST_DNI)
dny = (uhrazeno - splatna).days
print("doručena", doruceno, "; splatná", splatna, "; uhrazena", uhrazeno, "; dnů prodlení", dny)
print("pokuta správně:", kc(dluh * POKUTA_DENNE * dny), "; na dokladu (30 dnů)", kc(dluh * POKUTA_DENNE * 30))

print("\n== Report červenec až říjen 2026")
radky = nacti("report-podklady-2026-07-10.csv")
mesice = [r for r in radky if r["mesic"] != "celkem"]
celkem = next(r for r in radky if r["mesic"] == "celkem")
soucty = {}
for sloupec in [k for k in celkem if k != "mesic"]:
    s = sum(float(r[sloupec]) for r in mesice)
    soucty[sloupec] = s
    stav = "sedí" if s == float(celkem[sloupec]) else f"NESEDÍ, uvedeno {kc(float(celkem[sloupec]))}, rozdíl {kc(float(celkem[sloupec]) - s)}"
    print(f"{sloupec}: součet {s:,.0f}".replace(",", " "), "|", stav)
trzby = soucty["trzby_pausal_kc"] + soucty["trzby_jednorazove_kc"]
print("tržby celkem:", kc(trzby), "; podíl jednorázových", f"{soucty['trzby_jednorazove_kc'] / trzby:.1%}")
print("říjen jednorázové:", mesice[-1]["trzby_jednorazove_kc"], "=", float(mesice[-1]["trzby_jednorazove_kc"]) / SAZBA_HOD, "hodin při sazbě", SAZBA_HOD)

print("\n== Konec smlouvy při výpovědi doručené 20. 11. 2026 (čl. 8.2)")
print("lhůta běží od 1. 12. 2026, tři měsíce, konec 28. 2. 2027; chybný výpočet od doručení dá 20. 2. 2027")
print("lhůta pro oznámení nezájmu o prodloužení (čl. 2.2): 90 dnů před 31. 12. 2027 je", date.fromordinal(date(2027, 12, 31).toordinal() - 90))

# vuln-notify

Smyšlený nástroj bezpečnostního týmu. Z oznámení o zranitelnosti (JSON) a inventáře zákaznických prostředí (CSV)
vybere dotčená prostředí a připraví koncept oznámení pro každého zákazníka. Odeslání dělá člověk.

Všechna data jsou vymyšlená, domény končí na `.example`.

## Struktura

| Cesta | Co tam je |
|---|---|
| `vuln_notify/core.py` | načtení inventáře a oznámení, porovnání verzí, výběr dotčených, text oznámení |
| `notify.py` | spuštění nad jedním oznámením, koncepty ukládá do `out/` |
| `data/inventar.csv` | export inventáře zákaznických prostředí z CMDB |
| `advisories/` | oznámení o zranitelnostech ve formátu týmu |
| `templates/` | šablona textu pro zákazníka |
| `tests/` | testy v pytestu |
| `docs/tickets/` | zadání úloh |
| `CHANGELOG.md` | přehled změn |

## Spuštění

Potřebujete Python 3.9 nebo novější a pytest (`python -m pip install pytest`). Na macOS a Linuxu se Python
obvykle spouští příkazem `python3`, na Windows `python` nebo `py`.

```
python -m pytest
python notify.py advisories/VB-ADV-2026-07.json
```

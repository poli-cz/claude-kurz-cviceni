# C4: Praktický scénář (45 minut)

Vyberte si jeden ze tří scénářů. U všech platí stejný postup z 2. dne: nejdřív plán, potom malé kroky,
výsledek dává skript nebo test a poslední slovo má člověk. Všechna data ve složce jsou smyšlená.

Před začátkem: čistá pracovní kopie (`git status`), Claude Code spuštěný ve složce `05-scenare`
(u scénáře B ve složce `03-claude-md/vuln-notify`), režim oprávnění Manual (nová session startuje v režimu auto,
klávesami Shift+Tab přepněte do Manual, agent se pak ptá před úpravou souborů a před příkazy). Příkazy v zadání fungují stejně v terminálu Windows i v bashi;
Python se na Windows spouští příkazem `python` nebo `py`, na macOS a Linuxu `python3`.

## Scénář A: oznámení o zranitelnostech

Podklady: `oznameni/*.md` (tři oznámení výrobců), `inventar.csv` (14 instalací u pěti zákazníků).

1. Nechte agenta z každého oznámení vytáhnout dotčené verze, opravenou verzi a dočasné opatření do souboru
   `vystup/oznameni.json`. Ke každému údaji chtějte citaci věty z oznámení.
2. Nechte agenta napsat skript `sparuj.py`, který podle `oznameni.json` a `inventar.csv`
   vypíše dotčené instalace. Párování verzí dělá skript, agent ho jen píše.
3. Zkontrolujte výstup skriptu ručně na jednom zákazníkovi.
4. Nechte agenta připravit návrh oznámení pro jednoho zákazníka do `vystup/navrh-<zakaznik>.md`.
   Nic se neodesílá, návrh schvaluje člověk.

Kontrola: skript má najít 4 dotčené instalace u NG-SA-2026-014, 3 u BM-2026-0031 a 1 u VB-ADV-2026-07
(vzorové párování lektora: `python reseni-lektor/sparuj.py`).
Pozor na větev 6.9.x bez opravy, na verzi 7.5.3, která už je opravená, a na verze 11.x, kterých se třetí
oznámení netýká.

## Scénář B: refactoring a rozšíření skriptu s testy jako záchrannou sítí

Podklady: repo `../03-claude-md/vuln-notify` (Python, testy v pytestu), zadání `docs/tickets/VN-14.md`.
Potřebujete Python 3 a pytest (`python -m pip install pytest`; na macOS a Linuxu `python3`).

1. Spusťte testy: `python -m pytest`. Musí projít dřív, než se cokoli změní (11 testů).
2. Nechte agenta navrhnout plán podle VN-14 (nejdřív vyčlenit funkci `matches`, potom nový parametr).
   Plán schvalte nebo upravte.
3. Refactoring po malých krocích, po každém kroku testy. Počet testů se nemění a všechny procházejí.
4. Rozšíření: nejdřív testy pro `min_criticality`, které padají, potom implementace.
5. Projděte `git diff` a zkontrolujte, že agent neupravil dosavadní testy, aby prošly, a nesáhl do `data/`.

Kontrola: původních 11 testů prochází beze změny, přibyly testy nového parametru (ve vzorovém průběhu lektora
3 nové, po kroku 4 tedy „3 failed, 11 passed“, po kroku 5 „14 passed“), `git diff --stat` nemění `data/inventar.csv`.

Stejný postup platí pro vaše vlastní skripty v jakémkoli jazyce včetně PowerShellu: nejdřív testy, které popisují
dnešní chování, potom změna.

## Scénář C: analýza logu z Performance Monitoru

Podklady: `perfmon/perfmon.csv` (48 hodin po 5 minutách, 576 vzorků, formát PDH-CSV), generátor `perfmon/generuj.py`.

1. Zeptejte se agenta, co je příčinou ubývající paměti, a nedovolte mu číst celý soubor do kontextu.
   Chtějte analytický skript.
2. Skript má pro každý čítač spočítat trend (směrnici za hodinu) a kvalitu proložení.
3. Nechte agenta odhadnout, kdy dostupná paměť klesne pod 500 MB, a ukázat výpočet.
4. Ověřte jedno číslo ručně v tabulkovém procesoru.

Kontrola: roste jediný proces `svc-indexer`, zhruba o 61,5 MB za hodinu, spolu s počtem handlů (37 za hodinu).
Dostupná paměť klesne pod 500 MB přibližně 90 hodin od začátku měření.

## Co odevzdat

Do `vystup/` soubor `postup.md`: co dělal agent, co skript a co jste rozhodli vy, a jedno místo, kde jste
agenta museli zastavit nebo opravit.

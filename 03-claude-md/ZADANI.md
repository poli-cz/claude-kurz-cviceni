# Cvičení C3: Naučte agenta váš projekt (30 minut)

Repo `vuln-notify` je malý nástroj bezpečnostního týmu v Pythonu. Agent v něm úlohu VN-12 napoprvé
udělá „skoro správně“, protože část pravidel tým nikde nezapsal. Vaším úkolem je pravidla zapsat tak, aby je
agent dostal: do `CLAUDE.md`, do skillu, nebo do hooku.

## Co potřebujete

- Claude Code a přihlášený účet.
- Python 3.9 nebo novější a pytest: `python -m pip install pytest`.
- Git (kvůli čistému startu mezi běhy).

Python se na Windows spouští příkazem `python` nebo `py`, na macOS a Linuxu většinou `python3`. Příkazy níže
jsou psané s `python`; fungují stejně v terminálu Windows i v bashi.

## Co ví tým (a v kódu to není)

1. Soubory v `data/` jsou exporty z CMDB. Nikdo je ručně neupravuje, ani agent.
2. Verze se porovnávají po částech jako čísla (funkce `parse_version`), nikdy jako text (jinak je 7.4.10 menší než 7.4.9).
3. Výstup se řadí podle kritičnosti prostředí (`vysoka`, `stredni`, `nizka`) a teprve potom podle zákazníka.
4. Kritické oznámení (`Critical`) u prostředí s kritičností `vysoka` se eskaluje: řádek ve výpisu `notify.py` končí
   slovem `ESKALACE`. Jiné řádky ho nemají.
5. Kontaktní e-mail zákazníka se nikdy nevypisuje do konzole ani do logu.
6. Každá nová větev logiky má vlastní řádek v tabulce testů (`pytest.mark.parametrize`). Testy se pouští `python -m pytest`.
7. Formát oznámení se mění opatrně: starší oznámení musí fungovat dál.
8. Každá úloha přidá jeden řádek do `CHANGELOG.md`, začíná číslem úlohy (`VN-12: …`).

## Postup

1. **Před (7 min).** V čistém repu spusťte Claude Code a zadejte: `Implementuj docs/tickets/VN-12.md.`
   Po dokončení spusťte kontrolu: `python ../zkontroluj.py` a zapište si výsledek z 10.
2. **Rozbor (3 min).** Které body kontroly neprošly? Ke každému najděte řádek v seznamu „Co ví tým“.
3. **CLAUDE.md (7 min).** Vraťte repo do čistého stavu (dva příkazy po sobě: `git restore .` a `git clean -fd`).
   Napište `CLAUDE.md` v kořeni: krátce, každé pravidlo ověřitelné příkazem nebo v diffu. Příkaz `/init` vám dá kostru.
   Pravidla, která mají platit u každé úlohy, napište i do oddílu „hotovo znamená“ jako příkaz, kterým se ověří.
4. **Skill (5 min).** Postup „nové pole v oznámení“ zabalte do `.claude/skills/add-advisory-field/SKILL.md`.
5. **Hook (3 min).** Pravidlo 1 vynuťte hookem `PreToolUse`, který odmítne úpravu souborů v `data/`.
   Hook je skript v Pythonu, který dostane JSON na standardní vstup; bash nepotřebuje.
6. **Po (5 min).** Nová session, stejné zadání, stejná kontrola. Cíl je 10 z 10.

Ve zkušebních bězích lektora (16. 11. 2026, Claude Code 2.1.325, model Sonnet 5.5) dal agent bez znalostí týmu
třikrát 8 z 10 (chybělo řazení a eskalace) a se vzorovými soubory třikrát 10 z 10. S první verzí `CLAUDE.md`,
kde řazení a eskalace byly jen dvě věty mezi pravidly a chyběly v kritériích hotovo, je dva běhy ze tří vynechaly.
Váš výsledek se může lišit.

## Co si odnést

Která znalost patřila do `CLAUDE.md`, která do skillu a která do hooku? Vzorové řešení ukáže lektor po cvičení.
Víc správných odpovědí je v pořádku, pokud umíte říct proč.

Stejný postup platí pro vaše vlastní skripty v jakémkoli jazyce, včetně PowerShellu. Mění se jen příkazy v `CLAUDE.md`.

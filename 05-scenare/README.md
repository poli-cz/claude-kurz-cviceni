# 05 Scénáře (blok 13, cvičení C4)

Smyšlené podklady ke třem scénářům: oznámení o zranitelnostech, refactoring a rozšíření skriptu s testy
(nad repem `../03-claude-md/vuln-notify` v Pythonu), analýza logu z Performance Monitoru. Zadání je v `ZADANI.md`.

- `inventar.csv` je zdroj pravdy inventáře zákaznických prostředí pro celý 2. den; kopie jsou v
  `../03-claude-md/vuln-notify/data/` a `../04-mcp-inventar/`.
- `reseni-lektor/sparuj.py` je vzorové párování scénáře A (4, 3 a 1 dotčená instalace, celkem 8 ze 14).
- `perfmon/generuj.py` vygeneruje `perfmon.csv` (pevný seed).

Ověřeno 16. 11. 2026 na macOS (Python 3.12, pytest). Na Windows nezkoušeno.

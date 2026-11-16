# Ukázka: vlastní MCP server nad inventářem zákaznických prostředí

Ukázka lektora k bloku 11 (Integrace) a podklad k bloku 10 (Bezpečnost agentů). Dá se zopakovat po kurzu.
Data jsou smyšlená: pět zákazníků, tři produkty, čtrnáct řádků v `inventar.csv`
(sloupce `zakaznik, prostredi, produkt, verze, kontakt, kriticnost`). Stejný inventář používá repo `vuln-notify`
v `03-claude-md` a scénáře v `05-scenare`; zdroj pravdy je `05-scenare/inventar.csv`.

Ověřeno 16. 11. 2026 na macOS: Python 3.12, balíček `mcp` 2.3.0, Claude Code 2.1.325. Na Windows ukázka zkoušená nebyla.

## 1. Prostředí

Potřebujete Python 3.10 nebo novější. Balíček `mcp` 2.x používá třídu `MCPServer`; starší návody s `FastMCP` na něm skončí chybou.

macOS a Linux:

```
cd 04-mcp-inventar
python3 -m venv .venv
.venv/bin/pip install "mcp==2.3.0"
```

Windows (PowerShell nebo cmd, bez bashe):

```
cd 04-mcp-inventar
py -m venv .venv
.venv\Scripts\python -m pip install "mcp==2.3.0"
```

Dál je `PY` cesta k interpretu: `.venv/bin/python` na macOS a Linuxu, `.venv\Scripts\python.exe` na Windows.

## 2. Server

`server.py` má 35 řádků a dva nástroje, oba jen pro čtení:

- `seznam_produktu()` vrátí abecední seznam produktů,
- `prostredi_s_produktem(produkt)` vrátí řádky inventáře k jednomu produktu. Verze neporovnává a celý inventář najednou nevydá.

## 3. Ověření bez agenta

```
PY -c "import server; print(server.seznam_produktu())"
PY -c "import server; print(server.prostredi_s_produktem('Northgate'))"
PY -c "import server; server.prostredi_s_produktem('a')"
```

Třetí příkaz má skončit chybou `ValueError`.

## 4. Registrace v Claude Code

Server se registruje s absolutní cestou k interpretu a k souboru `server.py`.

macOS a Linux:

```
claude mcp add --transport stdio inventar -- "$PWD/.venv/bin/python" "$PWD/server.py"
```

Windows (cesty nahraďte svými):

```
claude mcp add --transport stdio inventar -- "C:\kurz\04-mcp-inventar\.venv\Scripts\python.exe" "C:\kurz\04-mcp-inventar\server.py"
```

Kontrola je všude stejná:

```
claude mcp list
claude mcp get inventar
```

Server se zapíše do rozsahu `local` (soubor `.claude.json` v domovské složce, jen pro tuto složku). Odebrání: `claude mcp remove inventar -s local`.

## 5. Dotaz

V této složce spusťte `claude` a zeptejte se:

> Kteří zákazníci provozují Northgate VPN Gateway ve verzi starší než 7.5.3? Použij nástroje serveru inventar a odpověz tabulkou.

Správná odpověď: Mesto Lipany (6.9.8), Alfa Energo (7.4.2), Banka Doubrava (7.5.1) a Strojirny Hron (7.5.0), vše v produkci.
Alfa Energo má v testu 7.6.0 a Nemocnice Javor v testu přesně 7.5.3, ty do výsledku nepatří.
V přípravě: čtyři tahy, jedenáct sekund, 0,24 USD (`claude -p`, model Claude Opus 5.5).

## Ukázky k bloku 10

- `ukazka-injekce/advisory-2026-1187.html`: smyšlené podvržené oznámení o zranitelnosti se skrytým pokynem v komentáři HTML
  (jiný výrobce než v inventáři, záměrně).
  Strukturovaná extrakce (v přípravě dva tahy, 0,28 USD, výstup bez stopy po vloženém pokynu). Příkaz pro macOS a Linux:

  ```
  cd ukazka-injekce
  cat advisory-2026-1187.html | claude -p "Vytáhni z oznámení produkt, dotčené verze, opravu a CVSS." \
    --output-format json --json-schema "$(cat advisory.schema.json)" --allowedTools "Read" > vysledek.json
  ```

  Na Windows spusťte `claude` ve složce `ukazka-injekce` a zadejte stejný pokyn s odkazem na soubor.

- `ukazka-hook/`: hook `PreToolUse` v Pythonu (`.claude/hooks/net.py`), který zakáže `curl`, `wget` a `nc` mimo povolené domény.
  Zkouška: ve složce `ukazka-hook` spusťte `claude` a požádejte o `curl -s https://example.org/`. Příkaz se nespustí a agent ocituje důvod z hooku.
  Hook je porovnání řetězce, slouží jako záchranná síť a zdroj auditu, síťovou kontrolu nenahrazuje.

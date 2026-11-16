# Claude a Claude Code: podklady ke cvičením

Podklady k dvoudennímu kurzu Claude a Claude Code. Všechna data jsou smyšlená: dodavatel Severka IT s.r.o.,
objednatel Lesní družstvo Borovina, smlouva číslo 2026/017, pět zákazníků v inventáři a tři oznámení o zranitelnostech.

| složka | den a blok | co v ní je |
|---|---|---|
| `01-zadani` | 1. den, blok 2, cvičení C1 | smlouva o správě IT (Markdown, Word, PDF), zadání a hodnoticí mřížka |
| `02-smlouvy-faktury` | 1. den, blok 5, cvičení C2 | faktury, výkaz práce, podklady k reportu, stav zakázek, tři nabídky |
| `03-claude-md` | 2. den, blok 7, cvičení C3 | repo `vuln-notify` (Python, pytest), zadání a kontrolní skript |
| `04-mcp-inventar` | 2. den, bloky 10 a 11, ukázka | MCP server nad inventářem zákaznických prostředí |
| `05-scenare` | 2. den, blok 13, cvičení C4 | oznámení o zranitelnostech, inventář, log z Performance Monitoru |

## Co potřebujete

1. den stačí účet Claude a prohlížeč nebo desktopová aplikace.

2. den:

- Claude Code a přihlášený účet,
- Git,
- Python 3.9 nebo novější a pytest (`python -m pip install pytest`),
- pro ukázku MCP serveru Python 3.10 nebo novější a balíček `mcp` (postup je v `04-mcp-inventar/README.md`).

Python se na Windows spouští příkazem `python` nebo `py`, na macOS a Linuxu většinou `python3`.

## Jak začít

```
git clone https://github.com/poli-cz/claude-kurz-cviceni.git
cd claude-kurz-cviceni
```

Kontrola prostředí před 2. dnem:

```
cd 03-claude-md/vuln-notify
python -m pytest
```

Testy mají projít. Zadání každého cvičení je v souboru `ZADANI.md` v jeho složce.

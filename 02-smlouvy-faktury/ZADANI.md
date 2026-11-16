# C2: Revize smlouvy do tabulky s citacemi (25 minut)

Podklady jsou smyšlené (Severka IT s.r.o. jako Dodavatel, Lesní družstvo Borovina jako Objednatel, smlouva číslo 2026/017). Pracujete v aplikaci Claude (chat nebo Project), bez programování.

## Cíl

Z plného znění smlouvy ve složce `../01-zadani/` získat tabulku povinností, kterou lze zkontrolovat proti textu.

## Postup

1. Nahrajte smlouvu do nové konverzace. Zadejte jednou větou: „Vypiš povinnosti ze smlouvy.“ Výsledek si uložte.
2. Začněte novou konverzaci. Napište zadání s pěti částmi (kontext, cíl, omezení, formát výstupu, kritéria kontroly).
   Vyžádejte tabulku se sloupci: povinnost, kdo ji má, lhůta nebo datum, sankce, článek smlouvy, doslovná citace.
3. Vyberte tři řádky tabulky a ověřte je proti textu smlouvy. Hledejte hlavně lhůty, počátek jejich běhu a částky.
4. Zeptejte se nad smlouvou: „Kdy nejdříve smlouva skončí, když výpověď doručíme 20. 11. 2026?“ Odpověď ověřte podle článku 8.2.
5. Porovnejte oba výstupy se sousedem. Co v prvním chybělo a co bylo navíc?

## Hotovo

Máte tabulku, ve které má každý řádek článek a citaci, tři řádky ověřené proti textu a odpověď na otázku z kroku 4.

## Navíc

- Zkontrolujte doklady z `faktury.md` proti výtahu `parametry-smlouvy.md` a výkazu `vykaz-prace-pentest.csv`. Najdete čtyři nesrovnalosti?
- Nechte Clauda přepočítat smluvní pokutu kódem a porovnejte s vyúčtováním P-2026-0007.
- V souboru `report-podklady-2026-07-10.csv` jeden součet nesedí. Nechte ho najít výpočtem.
- V souboru `zakazky-delivery.csv` je stav pěti zakázek k 31. 10. 2026. Které z nich potřebují zásah, i když součet čerpání vypadá dobře?
- Uložte své zadání jako Skill nebo jako pokyny Projectu a vyzkoušejte ho na jiné smlouvě.

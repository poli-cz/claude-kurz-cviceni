# Cvičení C1: slabé a dobré zadání

1. den, blok 2. Čas 25 až 30 minut, ve dvojicích. Jeden z dvojice zadává slabé zadání, druhý dobré.

## Cíl

Zjistit, co všechno model u slabého zadání rozhodl za vás, a o kolik se výsledek zlepší, když zadání má všech pět částí: kontext, cíl, omezení, formát výstupu a kritéria kontroly.

## Podklady

- `smlouva-sprava-it.pdf` (totéž jako `.docx` a `.md`): smyšlená smlouva o správě IT mezi dodavatelem Severka IT s.r.o. a objednatelem Lesní družstvo Borovina. Žádná skutečná data.
- `hodnotici-mrizka.md`: sedm kritérií, podle kterých oba výsledky ohodnotíte.

## Postup

1. **Nová konverzace** v aplikaci Claude. Nahrajte smlouvu. (2 min)
2. **Slabé zadání** (první z dvojice). Vložte přesně tuto větu a nic dalšího:

   ```
   Shrň mi povinnosti z této smlouvy.
   ```

   Na doplňující otázky modelu odpovězte „rozhodni sám“. Výsledek si uložte. (5 min)
3. **Dobré zadání** (druhý z dvojice, vlastní nová konverzace). Vložte zadání níže. (8 min)

   ```
   Kontext: Jsem bezpečnostní konzultant dodavatele (Severka IT). Přebírám po kolegovi
   zákazníka a potřebuji vědět, co musíme plnit. Smlouva je v příloze.

   Cíl: Vypiš všechny povinnosti Dodavatele, které mají lhůtu nebo sankci.

   Omezení: Vycházej jen z přiložené smlouvy. Nic nedomýšlej z obecné praxe.
   Když údaj ve smlouvě není, napiš „nenalezeno“. Povinnosti Objednatele vynech.

   Formát výstupu: Tabulka se sloupci Povinnost | Lhůta | Sankce | Článek | Citace.
   Jeden řádek je jedna povinnost. Ve sloupci Citace doslovná věta ze smlouvy.

   Kontrola: Pod tabulku napiš, kolik povinností jsi našel, a které dva řádky
   jsou podle tebe nejméně jisté a proč.
   ```

4. **Ověření** (oba). U dobrého zadání vyberte tři řádky tabulky a dohledejte citaci v dokumentu (Ctrl+F). Položte kontrolní otázku: „Jaká je sankce za pozdní předání měsíční zprávy?“ (5 min)
5. **Hodnocení** podle mřížky, každý svůj výsledek, potom porovnání ve dvojici. (7 min)

## Co odevzdáte

Vyplněnou mřížku pro obě zadání a seznam rozhodnutí, která model u slabého zadání udělal sám (čí povinnosti, jaký formát, jak podrobně, co s chybějícími údaji).

## Hotovo, když

umíte říct, které části dobrého zadání změnily výsledek nejvíc, a máte tři citace ověřené proti dokumentu.

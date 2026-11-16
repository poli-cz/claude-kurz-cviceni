"""MCP server nad inventářem zákaznických prostředí. Dva nástroje, oba jen pro čtení."""
import csv
from pathlib import Path

from mcp.server.mcpserver import MCPServer
from mcp.types import ToolAnnotations

INVENTAR = Path(__file__).with_name("inventar.csv")
mcp = MCPServer("inventar")
JEN_CTENI = ToolAnnotations(read_only_hint=True)


def radky() -> list[dict]:
    with INVENTAR.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


@mcp.tool(annotations=JEN_CTENI)
def seznam_produktu() -> list[str]:
    """Vrátí abecední seznam produktů, které zákazníci provozují. Použij jako první krok, když neznáš přesný název produktu."""
    return sorted({r["produkt"] for r in radky()})


@mcp.tool(annotations=JEN_CTENI)
def prostredi_s_produktem(produkt: str) -> list[dict]:
    """Najde zákaznická prostředí, kde běží daný produkt. `produkt` je název nebo jeho část, například "Northgate".
    Vrací zákazníka, prostředí, verzi, kontakt a kritičnost. Verze neporovnává, to je úkol volajícího."""
    hledany = produkt.strip().lower()
    if len(hledany) < 3:
        raise ValueError("Zadej aspoň tři znaky názvu produktu.")
    return [r for r in radky() if hledany in r["produkt"].lower()]


if __name__ == "__main__":
    mcp.run()

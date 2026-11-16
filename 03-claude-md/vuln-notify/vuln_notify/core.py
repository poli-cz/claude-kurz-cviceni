import csv
import json
from pathlib import Path
from typing import Dict, List, Tuple

Version = Tuple[int, ...]


def parse_version(text: str) -> Version:
    return tuple(int(part) for part in text.strip().split("."))


def load_inventory(path) -> List[Dict]:
    rows = []
    with open(path, newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            rows.append(
                {
                    "customer": row["zakaznik"],
                    "environment": row["prostredi"],
                    "product": row["produkt"],
                    "version": parse_version(row["verze"]),
                    "contact": row["kontakt"],
                    "criticality": row["kriticnost"],
                }
            )
    return rows


def read_advisory(path) -> Dict:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    for field in ("id", "product", "severity", "affected"):
        if field not in raw:
            raise ValueError(f"Advisory {path} is missing field '{field}'")
    return {
        "id": raw["id"],
        "product": raw["product"],
        "severity": raw["severity"],
        "title": raw.get("title", ""),
        "from": parse_version(raw["affected"]["from"]),
        "before": parse_version(raw["affected"]["before"]),
        "action": raw.get("action", ""),
    }


def is_affected(version: Version, start: Version, before: Version) -> bool:
    return start <= version < before


def affected_customers(inventory: List[Dict], advisory: Dict) -> List[Dict]:
    hits = [
        item
        for item in inventory
        if item["product"] == advisory["product"]
        and is_affected(item["version"], advisory["from"], advisory["before"])
    ]
    return sorted(hits, key=lambda item: (item["customer"], item["environment"]))


def render_notification(item: Dict, advisory: Dict, template_path) -> str:
    text = Path(template_path).read_text(encoding="utf-8")
    values = {
        "{{Customer}}": item["customer"],
        "{{Environment}}": item["environment"],
        "{{Product}}": item["product"],
        "{{Version}}": ".".join(str(part) for part in item["version"]),
        "{{AdvisoryId}}": advisory["id"],
        "{{Title}}": advisory["title"],
        "{{Severity}}": advisory["severity"],
        "{{Action}}": advisory["action"],
    }
    for key, value in values.items():
        text = text.replace(key, value)
    return text

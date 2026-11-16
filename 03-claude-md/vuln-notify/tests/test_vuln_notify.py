from pathlib import Path

import pytest

from vuln_notify import affected_customers, is_affected, load_inventory, parse_version, read_advisory, render_notification

ROOT = Path(__file__).parent.parent


@pytest.fixture(scope="module")
def inventory():
    return load_inventory(ROOT / "data" / "inventar.csv")


def test_inventory_reads_all_rows(inventory):
    assert len(inventory) == 14


def test_inventory_reads_criticality(inventory):
    assert {item["criticality"] for item in inventory} == {"vysoka", "stredni", "nizka"}


def test_inventory_parses_versions(inventory):
    assert inventory[0]["version"] == (7, 4, 2)


@pytest.mark.parametrize(
    "version, start, before, expected",
    [
        ("12.0.4", "12.0.0", "12.0.9", True),
        ("12.0.0", "12.0.0", "12.0.9", True),
        ("12.0.9", "12.0.0", "12.0.9", False),
        ("11.8.0", "12.0.0", "12.0.9", False),
        ("12.1.0", "12.0.0", "12.0.9", False),
        ("12.0.10", "12.0.0", "12.0.9", False),
    ],
)
def test_is_affected(version, start, before, expected):
    assert is_affected(parse_version(version), parse_version(start), parse_version(before)) is expected


def test_vb_advisory_finds_one_environment(inventory):
    advisory = read_advisory(ROOT / "advisories" / "VB-ADV-2026-07.json")
    hits = affected_customers(inventory, advisory)
    assert [(item["customer"], item["environment"]) for item in hits] == [("Banka Doubrava", "produkce")]


def test_notification_fills_every_placeholder(inventory):
    advisory = read_advisory(ROOT / "advisories" / "VB-ADV-2026-07.json")
    item = affected_customers(inventory, advisory)[0]
    text = render_notification(item, advisory, ROOT / "templates" / "notification.cs.txt")
    assert "{{" not in text
    assert "VB-ADV-2026-07" in text

import argparse
import re
from pathlib import Path

from vuln_notify import affected_customers, load_inventory, read_advisory, render_notification
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).parent


def main() -> None:
    parser = argparse.ArgumentParser(description="Draft customer notifications for one advisory.")
    parser.add_argument("advisory")
    parser.add_argument("--inventory", default=str(ROOT / "data" / "inventar.csv"))
    parser.add_argument("--template", default=str(ROOT / "templates" / "notification.cs.txt"))
    parser.add_argument("--out", default=str(ROOT / "out"))
    args = parser.parse_args()

    advisory = read_advisory(args.advisory)
    hits = affected_customers(load_inventory(args.inventory), advisory)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    for item in hits:
        name = "{}_{}_{}.txt".format(advisory["id"], re.sub(r"\W", "", item["customer"]), item["environment"])
        (out_dir / name).write_text(render_notification(item, advisory, args.template), encoding="utf-8")
        version = ".".join(str(part) for part in item["version"])
        print("{:<16} {:<9} {:<24} {:<8} {}".format(item["customer"], item["environment"], item["product"], version, item["criticality"]))
    print("{}: {} affected environments, drafts in {}".format(advisory["id"], len(hits), out_dir))


if __name__ == "__main__":
    main()

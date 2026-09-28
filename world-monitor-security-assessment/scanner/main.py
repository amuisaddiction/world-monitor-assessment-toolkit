"""
Entry point for the World Monitor security scanner.

Runs every check module in checks/ against the target and aggregates the
results into a single findings.json file matching the schema in
docs/design.md.

Usage:
    python main.py --target http://localhost:3000 --out ../dashboard/data/findings.json
"""
import argparse
import json
import uuid
from datetime import datetime, timezone

from checks import (
    auth_checks,
    authz_checks,
    input_validation_checks,
    api_checks,
    client_checks,
    transport_checks,
)

# Each check module must expose a `run(target: str) -> list[dict]` function
# that returns findings matching the schema in docs/design.md.
CHECK_MODULES = [
    auth_checks,
    authz_checks,
    input_validation_checks,
    api_checks,
    client_checks,
    transport_checks,
]


def run_all_checks(target: str) -> list[dict]:
    findings = []
    for module in CHECK_MODULES:
        try:
            findings.extend(module.run(target))
        except Exception as exc:  # noqa: BLE001 - a failing check shouldn't kill the scan
            findings.append({
                "id": f"ERR-{module.__name__}",
                "title": f"Check module {module.__name__} failed to run",
                "category": "info",
                "severity": "info",
                "cvss_score": 0.0,
                "affected_component": module.__name__,
                "description": str(exc),
                "reproduction_steps": [],
                "evidence": "",
                "remediation": "Fix the check module or investigate the target's availability.",
                "status": "open",
            })
    return findings


def main():
    parser = argparse.ArgumentParser(description="World Monitor security scanner")
    parser.add_argument("--target", required=True, help="Base URL of the LOCAL target instance")
    parser.add_argument("--out", default="findings.json", help="Path to write findings.json")
    args = parser.parse_args()

    findings = run_all_checks(args.target)

    output = {
        "scan_id": str(uuid.uuid4()),
        "target": args.target,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "findings": findings,
    }

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print(f"Scan complete. {len(findings)} findings written to {args.out}")


if __name__ == "__main__":
    main()

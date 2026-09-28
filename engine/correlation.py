from typing import List
from scanner.finding import Finding

def deduplicate_findings(findings: List[Finding]) -> List[Finding]:
    unique = {}
    for f in findings:
        key = f"{f.category}-{f.title}-{f.affected_component}"
        if key not in unique or f.cvss_score > unique[key].cvss_score:
            unique[key] = f
    return list(unique.values())

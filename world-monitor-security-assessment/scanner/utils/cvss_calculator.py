"""
Lightweight helper for recording CVSS context alongside a finding.

This does NOT compute a CVSS score for you — use the official calculator
(https://www.first.org/cvss/calculator/3.1) and paste the resulting vector
string and score here for traceability. Auto-generating CVSS scores without
review tends to produce numbers judges will (rightly) question.
"""

SEVERITY_BANDS = {
    "critical": (9.0, 10.0),
    "high": (7.0, 8.9),
    "medium": (4.0, 6.9),
    "low": (0.1, 3.9),
    "info": (0.0, 0.0),
}


def severity_from_score(score: float) -> str:
    for severity, (low, high) in SEVERITY_BANDS.items():
        if low <= score <= high:
            return severity
    return "info"


def build_cvss_record(vector_string: str, score: float) -> dict:
    return {
        "vector": vector_string,
        "score": score,
        "severity": severity_from_score(score),
    }

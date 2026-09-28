def generate_local_fallback_report(findings: list) -> str:
    if not findings:
        return "# World Monitor Security Assessment Report\n\nNo security findings were generated during this assessment."
        
    critical = [f for f in findings if f.get('severity') == 'Critical']
    high = [f for f in findings if f.get('severity') == 'High']
    medium = [f for f in findings if f.get('severity') == 'Medium']
    low = [f for f in findings if f.get('severity') == 'Low']
    
    report = "# World Monitor Security Assessment Report\n\n"
    report += "## 1. Executive Summary\n"
    report += f"This report outlines the findings of the automated security assessment. "
    report += f"A total of {len(findings)} issues were discovered: "
    report += f"{len(critical)} Critical, {len(high)} High, {len(medium)} Medium, and {len(low)} Low severity issues.\n\n"
    
    report += "## 2. Detailed Findings\n"
    for idx, f in enumerate(findings):
        report += f"### {idx+1}. {f.get('title')} ({f.get('severity')})\n"
        report += f"- **ID**: {f.get('id')}\n"
        report += f"- **Category**: {f.get('category')}\n"
        report += f"- **CVSS Score**: {f.get('cvss_score')}\n"
        report += f"- **Description**: {f.get('description')}\n"
        report += f"- **Impact**: {f.get('impact')}\n"
        report += f"- **Remediation**: {f.get('remediation')}\n\n"
        
    report += "## 3. Conclusion\n"
    report += "Please address all High and Critical issues immediately. Medium and Low issues can be scheduled for future sprints.\n"
    return report

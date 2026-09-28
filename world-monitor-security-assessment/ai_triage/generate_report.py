"""
Reads findings.json, calls an LLM to enrich each finding with a polished
writeup + remediation, and writes per-finding Markdown files to
reports/findings/.

Swap `call_llm()` for whichever provider you're using (Claude API or
Gemini Pro, per docs/techstack.md) — this file intentionally leaves the
API call as a stub so you can wire in your own key/SDK.
"""
import json
import os
from pathlib import Path

FINDINGS_PATH = Path("../dashboard/data/findings.json")
OUTPUT_DIR = Path("../reports/findings")
PROMPT_TEMPLATE_PATH = Path("prompts/finding_writeup_prompt.txt")


def call_llm(prompt: str) -> str:
    """
    TODO: wire this up to your LLM provider.

    Example (Gemini Pro, pseudocode):
        import google.generativeai as genai
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        model = genai.GenerativeModel("gemini-pro")
        return model.generate_content(prompt).text

    Example (Claude API, pseudocode):
        import anthropic
        client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        msg = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}],
        )
        return msg.content[0].text
    """
    raise NotImplementedError("Wire up your LLM provider here (see docstring).")


def main():
    findings_data = json.loads(FINDINGS_PATH.read_text(encoding="utf-8"))
    template = PROMPT_TEMPLATE_PATH.read_text(encoding="utf-8")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for finding in findings_data.get("findings", []):
        prompt = template.format(finding_json=json.dumps(finding, indent=2))
        try:
            writeup = call_llm(prompt)
        except NotImplementedError:
            writeup = (
                "*(LLM writeup not generated — wire up call_llm() in "
                "generate_report.py, then re-run.)*\n\n"
                f"Raw finding data:\n```json\n{json.dumps(finding, indent=2)}\n```"
            )

        out_path = OUTPUT_DIR / f"{finding['id']}.md"
        out_path.write_text(
            f"# {finding['title']} ({finding['id']})\n\n"
            f"**Severity:** {finding['severity']} | **CVSS:** {finding['cvss_score']}\n"
            f"**Affected component:** {finding['affected_component']}\n\n"
            f"{writeup}\n",
            encoding="utf-8",
        )
        print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()

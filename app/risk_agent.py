import json

from search import load_knowledge_base, load_embedding_model, search_chunks
from llm import ask_llm
from risk_scoring import (
    calculate_risk_score,
    calculate_overall_score,
    calculate_risk_level
)
from category_normalizer import normalize_risks
from compliance_checker import run_compliance_checks
from report_generator import generate_report, save_report
from logger import logger


def build_context(results: list[dict]) -> str:
    """Build evidence context from retrieved contract chunks."""

    context_parts = []

    for result in results:
        context_parts.append(
            f"[Page {result['page']} | {result['chunk_id']}]\n"
            f"{result['text']}"
        )

    return "\n\n".join(context_parts)


def analyze_contract_risk(
    question: str,
    knowledge_base: list[dict] | None = None
) -> dict:
    """
    Retrieve relevant contract evidence and use Qwen3
    to identify potential compliance or operational risks.
    """

    logger.info("Starting contract risk analysis")

    if knowledge_base is None:
        logger.info("Loading knowledge base")
        knowledge_base = load_knowledge_base()

    logger.info(
        f"Knowledge base available: {len(knowledge_base)} chunks"
    )

    model = load_embedding_model()

    logger.info("Running compliance checks")

    compliance_checks = run_compliance_checks(
        knowledge_base
    )

    logger.info("Running semantic search")

    results = search_chunks(
        question,
        knowledge_base,
        model,
        top_k=5
    )

    logger.info(
        f"Retrieved {len(results)} relevant chunks"
    )

    context = build_context(results)

    prompt = f"""
You are a contract risk extraction system.

Your task is to extract risks ONLY from the CONTRACT EVIDENCE below.

OUTPUT REQUIREMENT:
Return exactly one valid JSON object.
The first character of your response must be {{
The last character of your response must be }}
Do not write anything before or after the JSON object.

Required JSON structure:

{{
  "risks": [
    {{
      "category": "Information Security",
      "severity": "HIGH",
      "finding": "Contractual security gap",
      "evidence": "Supporting contract evidence",
      "page": 1,
      "recommendation": "Recommended contractual improvement"
    }}
  ]
}}

RULES:

1. Use ONLY the Contract Evidence.
2. Do NOT use outside knowledge.
3. Do NOT mention GDPR, CCPA, ISO, NIST, SEC, FINRA,
   laws, regulations, standards, fines, or statistics.
4. Do NOT claim legal non-compliance.
5. A missing contractual requirement can be reported as a
   contractual gap only if the evidence supports that gap.
6. Every risk must contain evidence from the Contract Evidence.
7. severity must be exactly HIGH, MEDIUM, or LOW.
8. page must be a number.
9. Every risk must contain a recommendation.
10. Do not add explanations, summaries, conclusions, headings,
    Markdown, bullet points, or commentary.
11. Do not use ```json or ``` markers.
12. Return only the JSON object.
13. If no supported risks exist, return:
    {{"risks": []}}

CONTRACT EVIDENCE:
{context}

ANALYSIS REQUEST:
{question}

RETURN JSON:
"""

    logger.info("Sending contract analysis request to LLM")

    response = ask_llm(prompt)

    logger.info("Risk analysis response received from LLM")

    try:
        risk_data = json.loads(response)

    except json.JSONDecodeError as e:
        logger.error(
            f"Invalid JSON returned by LLM: {e}"
        )

        raise ValueError(
            f"Qwen3 returned invalid JSON: {e}\n\n"
            f"Raw response:\n{response}"
        )

    if "risks" not in risk_data:
        logger.error(
            "LLM response missing 'risks' field"
        )

        raise ValueError(
            "Invalid risk response: missing 'risks' field."
        )

    logger.info(
        f"Risks extracted by LLM: "
        f"{len(risk_data['risks'])}"
    )

    normalized_risks = normalize_risks(
        risk_data["risks"]
    )

    scored_risks = calculate_risk_score(
        normalized_risks
    )

    overall_score = calculate_overall_score(
        scored_risks
    )

    overall_level = calculate_risk_level(
        overall_score
    )

    logger.info(
        f"Risk analysis completed | "
        f"Score: {overall_score} | "
        f"Level: {overall_level}"
    )

    return {
        "risks": scored_risks,
        "overall_score": overall_score,
        "overall_level": overall_level,
        "compliance_checks": compliance_checks
    }


if __name__ == "__main__":

    logger.info("Starting Enterprise Contract Risk Agent")

    print("=" * 70)
    print("ENTERPRISE CONTRACT RISK AGENT")
    print("=" * 70)

    question = (
        "Identify potential compliance and operational risks "
        "related to data protection and security."
    )

    print("\nAnalysis Request:")
    print(question)

    print("\nAnalyzing contract...")

    result = analyze_contract_risk(question)

    print("\nStructured Risk Analysis:")

    for index, risk in enumerate(
        result["risks"],
        start=1
    ):

        print(f"\nRisk #{index}")
        print(f"Category       : {risk['category']}")
        print(f"Severity       : {risk['severity']}")
        print(f"Score          : {risk['score']}")
        print(f"Finding        : {risk['finding']}")
        print(f"Evidence       : {risk['evidence']}")
        print(f"Page           : {risk['page']}")
        print(
            f"Recommendation : "
            f"{risk['recommendation']}"
        )

    print("\n" + "-" * 70)

    print(
        f"OVERALL RISK SCORE: "
        f"{result['overall_score']}"
    )

    print(
        f"OVERALL RISK LEVEL: "
        f"{result['overall_level']}"
    )

    print("\n" + "=" * 70)
    print("COMPLIANCE CHECKS")
    print("=" * 70)

    for check in result["compliance_checks"]:

        print(f"\nCheck   : {check['check']}")
        print(f"Status  : {check['status']}")
        print(f"Message : {check['message']}")

    print("\n")

    report = generate_report(result)

    print(report)

    save_report(
        report,
        "data/processed/contract_risk_report.txt"
    )

    logger.info(
        "Contract risk report generated successfully"
    )
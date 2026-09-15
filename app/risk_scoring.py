SEVERITY_SCORES = {
    "HIGH": 3,
    "MEDIUM": 2,
    "LOW": 1
}


def calculate_risk_score(risks: list[dict]) -> list[dict]:
    """
    Add a numeric score to each risk based on severity.
    """

    scored_risks = []

    for risk in risks:
        severity = risk["severity"].upper()

        score = SEVERITY_SCORES.get(severity, 0)

        scored_risks.append({
            **risk,
            "score": score
        })

    return scored_risks


def calculate_overall_score(risks: list[dict]) -> int:
    """
    Calculate the total risk score for the contract.
    """

    return sum(risk["score"] for risk in risks)

def calculate_risk_level(overall_score: int) -> str:
    """
    Convert the overall risk score into a risk level.
    """

    if overall_score >= 6:
        return "HIGH"
    elif overall_score >= 3:
        return "MEDIUM"
    else:
        return "LOW"

if __name__ == "__main__":

    sample_risks = [
        {
            "category": "Information Security",
            "severity": "HIGH",
            "finding": "Missing security requirements",
            "evidence": "Security requirements are not specified.",
            "page": 1,
            "recommendation": "Define minimum security requirements."
        },
        {
            "category": "Data Retention",
            "severity": "MEDIUM",
            "finding": "No defined deletion period",
            "evidence": "No specific deletion period is established.",
            "page": 2,
            "recommendation": "Define a deletion period."
        }
    ]

    scored_risks = calculate_risk_score(sample_risks)

    print("=" * 70)
    print("RISK SCORING TEST")
    print("=" * 70)

    for risk in scored_risks:
        print(f"\nCategory : {risk['category']}")
        print(f"Severity : {risk['severity']}")
        print(f"Score    : {risk['score']}")

    overall_score = calculate_overall_score(scored_risks)

    overall_level = calculate_risk_level(
        overall_score
    )

    print(f"\nOverall Risk Score: {overall_score}")
    print(f"Overall Risk Level: {overall_level}")

    print("\n" + "=" * 70)
    print("RISK SCORING TEST SUCCESSFUL!")
    print("=" * 70)
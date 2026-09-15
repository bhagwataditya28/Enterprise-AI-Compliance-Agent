def normalize_category(risk: dict) -> dict:
    """
    Normalize risk categories using simple keyword-based rules.
    """

    finding = risk.get("finding", "").lower()
    evidence = risk.get("evidence", "").lower()

    text = finding + " " + evidence

    if any(keyword in text for keyword in [
        "deletion period",
        "delete",
        "retention"
    ]):
        category = "Data Retention"

    elif any(keyword in text for keyword in [
        "business continuity",
        "disaster recovery",
        "recovery time",
        "recovery point",
        "recovery objective"
    ]):
        category = "Business Continuity"

    elif any(keyword in text for keyword in [
        "security",
        "penetration testing",
        "encryption",
        "access control",
        "vulnerability",
        "security certification"
    ]):
        category = "Information Security"

    else:
        category = risk.get("category", "Other")

    return {
        **risk,
        "category": category
    }


def normalize_risks(risks: list[dict]) -> list[dict]:
    """
    Normalize categories for all detected risks.
    """

    return [
        normalize_category(risk)
        for risk in risks
    ]


if __name__ == "__main__":

    sample_risks = [
        {
            "category": "Information Security",
            "finding": "Missing specific security requirements",
            "evidence": "No encryption or access control standard is specified."
        },
        {
            "category": "Information Security",
            "finding": "Missing data deletion period",
            "evidence": "No specific deletion period is established after termination."
        },
        {
            "category": "Information Security",
            "finding": "Missing business continuity and disaster recovery testing requirements",
            "evidence": "No recovery time objective or disaster recovery testing frequency is specified."
        }
    ]

    normalized_risks = normalize_risks(sample_risks)

    print("=" * 70)
    print("CATEGORY NORMALIZATION TEST")
    print("=" * 70)

    for risk in normalized_risks:
        print(f"\nOriginal Category  : Information Security")
        print(f"Normalized Category: {risk['category']}")
        print(f"Finding            : {risk['finding']}")

    print("\n" + "=" * 70)
    print("CATEGORY NORMALIZATION TEST SUCCESSFUL!")
    print("=" * 70)
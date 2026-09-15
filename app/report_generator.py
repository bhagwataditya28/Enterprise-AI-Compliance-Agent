from datetime import datetime


def generate_report(result: dict) -> str:
    """
    Generate a professional contract risk report
    from the risk-agent results.
    """

    report = []

    report.append("=" * 80)
    report.append("ENTERPRISE CONTRACT RISK REPORT")
    report.append("=" * 80)

    report.append(
        f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    report.append(
        f"\nOverall Risk Score : {result['overall_score']}"
    )

    report.append(
        f"Overall Risk Level  : {result['overall_level']}"
    )

    report.append("\n" + "-" * 80)
    report.append("IDENTIFIED RISKS")
    report.append("-" * 80)

    for index, risk in enumerate(result["risks"], start=1):

        report.append(f"\nRisk #{index}")
        report.append(f"Category       : {risk['category']}")
        report.append(f"Severity       : {risk['severity']}")
        report.append(f"Score          : {risk['score']}")
        report.append(f"Finding        : {risk['finding']}")
        report.append(f"Evidence       : {risk['evidence']}")
        report.append(f"Contract Page  : {risk['page']}")
        report.append(
            f"Recommendation : {risk['recommendation']}"
        )

    report.append("\n" + "-" * 80)
    report.append("COMPLIANCE CHECKS")
    report.append("-" * 80)

    for check in result["compliance_checks"]:

        report.append(
            f"\n{check['check']}"
        )

        report.append(
            f"Status  : {check['status']}"
        )

        report.append(
            f"Message : {check['message']}"
        )

    report.append("\n" + "=" * 80)
    report.append("END OF REPORT")
    report.append("=" * 80)

    return "\n".join(report)

def save_report(report: str, output_path: str) -> None:
    """
    Save the generated report to a text file.
    """

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(report)

    print(f"\nReport saved to: {output_path}")


if __name__ == "__main__":

    sample_result = {
        "overall_score": 7,
        "overall_level": "HIGH",

        "risks": [
            {
                "category": "Information Security",
                "severity": "HIGH",
                "score": 3,
                "finding": "Missing specific security requirements",
                "evidence": "Specific security controls are not defined.",
                "page": 1,
                "recommendation": "Define minimum security requirements."
            },
            {
                "category": "Data Retention",
                "severity": "MEDIUM",
                "score": 2,
                "finding": "No defined data deletion period",
                "evidence": "No specific deletion period is established.",
                "page": 2,
                "recommendation": "Specify a deletion period."
            }
        ],

        "compliance_checks": [
            {
                "check": "Data Deletion",
                "status": "GAP",
                "message": "A specific data deletion period is not defined."
            },
            {
                "check": "Audit Rights",
                "status": "PASS",
                "message": "Audit rights are mentioned in the contract."
            }
        ]
    }

    print(generate_report(sample_result))
from risk_agent import analyze_contract_risk


def run_hallucination_test():
    print("=" * 70)
    print("CONTRACT RISK AGENT - UNSUPPORTED QUESTION TEST")
    print("=" * 70)

    question = (
        "Does the contract specify that the vendor has GDPR "
        "compliance certification?"
    )

    print("\nQuestion:")
    print(question)

    print("\nRunning agent...")

    result = analyze_contract_risk(question)

    print("\nAgent Result:")
    print("-" * 70)

    if not result["risks"]:
        print("No supported risks identified.")
        print("\nResult: PASS")
        print(
            "The agent did not invent a risk from unsupported evidence."
        )
    else:
        print(
            f"Risks returned: {len(result['risks'])}"
        )

        for index, risk in enumerate(
            result["risks"],
            start=1
        ):
            print(f"\nRisk #{index}")
            print(f"Category   : {risk['category']}")
            print(f"Severity   : {risk['severity']}")
            print(f"Finding    : {risk['finding']}")
            print(f"Evidence   : {risk['evidence']}")
            print(f"Page       : {risk['page']}")

        print("\nResult: REVIEW")
        print(
            "The agent returned a risk. Check whether "
            "the evidence actually supports it."
        )

    print("\n" + "=" * 70)
    print("UNSUPPORTED QUESTION TEST COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    run_hallucination_test()
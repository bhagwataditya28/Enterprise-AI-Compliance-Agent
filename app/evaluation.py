from risk_agent import analyze_contract_risk


TEST_CASES = [
    {
        "name": "Information Security",
        "question": (
            "Identify potential contractual risks related "
            "to information security."
        ),
        "expected": "Information Security"
    },
    {
        "name": "Data Retention",
        "question": (
            "Identify potential contractual risks related "
            "to data retention and deletion."
        ),
        "expected": "Data Retention"
    },
    {
        "name": "Business Continuity",
        "question": (
            "Identify potential contractual risks related "
            "to business continuity and disaster recovery."
        ),
        "expected": "Business Continuity"
    }
]


def run_evaluation():

    print("=" * 70)
    print("CONTRACT RISK AGENT - EVALUATION TEST")
    print("=" * 70)

    passed = 0
    total = len(TEST_CASES)

    for index, test_case in enumerate(
        TEST_CASES,
        start=1
    ):

        print("\n" + "-" * 70)

        print(
            f"TEST {index}: "
            f"{test_case['name']}"
        )

        print(
            f"\nQuestion: "
            f"{test_case['question']}"
        )

        print("\nRunning agent...")

        result = analyze_contract_risk(
            test_case["question"]
        )

        detected_categories = {
            risk["category"]
            for risk in result["risks"]
        }

        expected_category = test_case["expected"]

        print(
            f"\nExpected: "
            f"{expected_category}"
        )

        print(
            f"Detected: "
            f"{', '.join(sorted(detected_categories))}"
        )

        if expected_category in detected_categories:

            print("Result: PASS")
            passed += 1

        else:

            print("Result: FAIL")

    accuracy = (
        passed / total
    ) * 100

    print("\n" + "=" * 70)

    print(
        f"Tests passed : {passed}/{total}"
    )

    print(
        f"Evaluation accuracy: {accuracy:.1f}%"
    )

    print("=" * 70)

    if passed == total:
        print("ALL EVALUATION TESTS PASSED!")
    else:
        print("Some evaluation tests failed.")

    print("=" * 70)


if __name__ == "__main__":
    run_evaluation()
from search import load_knowledge_base


def get_contract_text(knowledge_base: list[dict]) -> str:
    """
    Combine all knowledge-base chunks into one searchable text.
    """

    return " ".join(
        chunk["text"]
        for chunk in knowledge_base
    ).lower()


def run_compliance_checks(knowledge_base: list[dict]) -> list[dict]:
    """
    Run simple deterministic contractual compliance checks.
    """

    contract_text = get_contract_text(knowledge_base)

    checks = []

    # 1. Security requirements
    security_present = any(keyword in contract_text for keyword in [
        "security certification",
        "penetration-testing",
        "encryption",
        "access-control"
    ])

    checks.append({
        "check": "Security Requirements",
        "status": "PASS" if security_present else "GAP",
        "message": (
            "Specific security requirements are mentioned."
            if security_present
            else "Specific security requirements are not clearly defined."
        )
    })

    # 2. Incident notification
    incident_present = any(keyword in contract_text for keyword in [
        "security incident",
        "incident notification",
        "notify company"
    ])

    checks.append({
        "check": "Security Incident Notification",
        "status": "PASS" if incident_present else "GAP",
        "message": (
            "Security incident notification requirements are present."
            if incident_present
            else "Security incident notification requirements are not clearly defined."
        )
    })

        # 3. Data deletion
    deletion_gap = any(keyword in contract_text for keyword in [
        "no specific deletion period",
        "no specific data deletion",
        "for as long as vendor considers necessary"
    ])

    deletion_present = any(keyword in contract_text for keyword in [
        "specific deletion period is established",
        "delete company data within",
        "return or destroy company data"
    ])

    if deletion_gap:
        deletion_status = "GAP"
        deletion_message = (
            "A specific data deletion period is not defined."
        )
    elif deletion_present:
        deletion_status = "PASS"
        deletion_message = (
            "A specific data deletion requirement is defined."
        )
    else:
        deletion_status = "GAP"
        deletion_message = (
            "A specific data deletion period is not clearly defined."
        )

    checks.append({
        "check": "Data Deletion",
        "status": deletion_status,
        "message": deletion_message
    })

    # 4. Audit rights
    audit_present = any(keyword in contract_text for keyword in [
        "audit rights",
        "right to audit",
        "audit"
    ])

    checks.append({
        "check": "Audit Rights",
        "status": "PASS" if audit_present else "GAP",
        "message": (
            "Audit rights are mentioned in the contract."
            if audit_present
            else "Audit rights are not clearly defined."
        )
    })

        # 5. Business continuity
    continuity_gap = any(keyword in contract_text for keyword in [
        "do not establish mandatory recovery time objectives",
        "do not establish",
        "no recovery time objective",
        "no recovery point objective"
    ])

    continuity_present = any(keyword in contract_text for keyword in [
        "recovery time objective is",
        "recovery point objective is",
        "disaster recovery testing frequency is defined"
    ])

    if continuity_gap:
        continuity_status = "GAP"
        continuity_message = (
            "Specific business continuity and disaster recovery requirements "
            "are not adequately defined."
        )
    elif continuity_present:
        continuity_status = "PASS"
        continuity_message = (
            "Specific business continuity requirements are defined."
        )
    else:
        continuity_status = "GAP"
        continuity_message = (
            "Specific business continuity requirements are not clearly defined."
        )

    checks.append({
        "check": "Business Continuity",
        "status": continuity_status,
        "message": continuity_message
    })
    
    return checks


if __name__ == "__main__":

    print("=" * 70)
    print("CONTRACT COMPLIANCE CHECKER TEST")
    print("=" * 70)

    knowledge_base = load_knowledge_base()

    print(f"\nKnowledge base loaded: {len(knowledge_base)} chunks")

    checks = run_compliance_checks(
        knowledge_base
    )

    print("\nCompliance Checks:")

    for check in checks:
        print("\n" + "-" * 70)
        print(f"Check   : {check['check']}")
        print(f"Status  : {check['status']}")
        print(f"Message : {check['message']}")

    print("\n" + "=" * 70)
    print("COMPLIANCE CHECKER TEST COMPLETE!")
    print("=" * 70)
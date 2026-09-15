import streamlit as st

from build_knowledge_base import build_knowledge_base
from risk_agent import analyze_contract_risk
from report_generator import generate_report


st.set_page_config(
    page_title="Enterprise Contract Risk Agent",
    page_icon="🔎",
    layout="wide"
)


st.title("Enterprise Contract Risk Agent")

st.write(
    "AI-powered contract compliance and risk analysis "
    "using RAG and Generative AI."
)

st.divider()

st.subheader("Contract Analysis")

uploaded_file = st.file_uploader(
    "Upload a contract PDF",
    type=["pdf"]
)

if uploaded_file is not None:

    st.success(
        f"Uploaded: {uploaded_file.name}"
    )

    if st.button("Analyze Contract"):

        try:

            with st.spinner(
                "Processing contract and running risk analysis..."
            ):

                uploaded_pdf_path = (
                    "data/documents/uploaded_contract.pdf"
                )

                with open(
                    uploaded_pdf_path,
                    "wb"
                ) as file:
                    file.write(
                        uploaded_file.getbuffer()
                    )

                knowledge_base = build_knowledge_base(
                    pdf_file=uploaded_pdf_path,
                    output_file=(
                        "data/processed/"
                        "uploaded_knowledge_base.json"
                    )
                )

                result = analyze_contract_risk(
                    question=(
                        "Identify potential compliance and "
                        "operational risks related to "
                        "data protection, security, "
                        "business continuity, audit rights, "
                        "and data retention."
                    ),
                    knowledge_base=knowledge_base
                )

        except Exception as e:

            st.error(
                "Contract analysis could not be completed."
            )

            st.info(
                "Please check that the PDF contains readable "
                "text and that Ollama is running with the "
                "configured model."
            )

            st.exception(e)

            st.stop()

        st.success("Contract analysis completed!")

        st.divider()

        st.subheader("Overall Risk")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Risk Score",
                result["overall_score"]
            )

        with col2:
            st.metric(
                "Risk Level",
                result["overall_level"]
            )

        st.divider()

        st.subheader("Identified Risks")

        for index, risk in enumerate(
            result["risks"],
            start=1
        ):

            with st.expander(
                f"Risk #{index} — {risk['category']}"
            ):

                st.write(
                    f"**Severity:** {risk['severity']}"
                )

                st.write(
                    f"**Score:** {risk['score']}"
                )

                st.write(
                    f"**Finding:** {risk['finding']}"
                )

                st.write(
                    f"**Evidence:** {risk['evidence']}"
                )

                st.write(
                    f"**Contract Page:** {risk['page']}"
                )

                st.write(
                    f"**Recommendation:** "
                    f"{risk['recommendation']}"
                )

        st.divider()

        st.subheader("Compliance Checks")

        for check in result["compliance_checks"]:

            if check["status"] == "PASS":
                st.success(
                    f"{check['check']}: PASS — "
                    f"{check['message']}"
                )

            else:
                st.warning(
                    f"{check['check']}: GAP — "
                    f"{check['message']}"
                )
        st.divider()

        st.subheader("Risk Report")

        report = generate_report(result)

        st.download_button(
            label="📄 Download Risk Report",
            data=report,
            file_name="contract_risk_report.txt",
            mime="text/plain"
        )
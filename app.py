import os
import streamlit as st

from admission_crew import run_admission_crew


st.set_page_config(
    page_title="AI University Admission Advisor",
    page_icon="🎓",
    layout="wide",
)

st.title("🎓 AI University Admission Advisor")
st.caption("Multi-agent admission analysis powered by CrewAI + Groq GPT-OSS 120B")

with st.sidebar:
    st.header("Applicant Information")

    applicant_name = st.text_input("Applicant name", placeholder="e.g. Ali Khan")
    qualification = st.text_input(
        "Latest qualification",
        placeholder="e.g. FSc Pre-Medical / A-Levels / ICS",
    )
    marks = st.number_input(
        "Overall marks / percentage",
        min_value=0.0,
        max_value=100.0,
        value=70.0,
        step=0.1,
    )
    subjects = st.text_area(
        "Major subjects",
        placeholder="e.g. Biology, Chemistry, Physics",
        height=100,
    )
    entry_test = st.text_input(
        "Entry test result",
        placeholder="e.g. MDCAT 82%, ECAT 78%, N/A",
    )
    domicile = st.text_input(
        "Domicile / region",
        placeholder="e.g. Punjab",
    )
    preferred_fields = st.text_area(
        "Preferred fields / interests",
        placeholder="e.g. Biotechnology, Microbiology, Bioinformatics",
        height=100,
    )

st.subheader("University / Program Requirements")

requirements = st.text_area(
    "Paste the official admission requirements here",
    height=240,
    placeholder=(
        "Example:\n"
        "BS Biotechnology\n"
        "- Minimum 50% in FSc/A-Level equivalent\n"
        "- Biology required\n"
        "- Chemistry required\n"
        "- Entry test minimum 50%\n\n"
        "BS Microbiology\n"
        "- Minimum 55%\n"
        "- Biology required\n"
        "- Chemistry required"
    ),
)

additional_notes = st.text_area(
    "Additional information (optional)",
    placeholder="Any special quota, gap year, subject deficiency, or other relevant information.",
    height=120,
)

analyze = st.button("🔍 Analyze Admission", type="primary", use_container_width=True)

if analyze:
    if not os.getenv("GROQ_API_KEY"):
        st.error("GROQ_API_KEY is not configured. Add it in Streamlit Cloud → Settings → Secrets.")
        st.stop()

    if not qualification.strip():
        st.warning("Please enter your latest qualification.")
        st.stop()

    if not requirements.strip():
        st.warning("Please paste the university/program admission requirements.")
        st.stop()

    applicant = {
        "name": applicant_name.strip() or "Applicant",
        "qualification": qualification.strip(),
        "marks_percentage": marks,
        "subjects": subjects.strip() or "Not provided",
        "entry_test": entry_test.strip() or "Not provided",
        "domicile": domicile.strip() or "Not provided",
        "preferred_fields": preferred_fields.strip() or "Not provided",
        "additional_notes": additional_notes.strip() or "None",
    }

    with st.spinner("The admission agents are analyzing your application..."):
        try:
            result = run_admission_crew(
                applicant=applicant,
                requirements=requirements.strip(),
            )
        except Exception as exc:
            st.error("The admission analysis could not be completed.")
            st.exception(exc)
            st.stop()

    st.success("Admission analysis completed.")

    st.subheader("📋 Final Admission Report")
    st.markdown(result["final_report"])

    with st.expander("🔎 View individual agent analyses"):
        tabs = st.tabs(
            [
                "Requirements",
                "Eligibility",
                "Programs",
                "Advisor",
            ]
        )

        with tabs[0]:
            st.markdown(result["requirements_analysis"])

        with tabs[1]:
            st.markdown(result["eligibility_analysis"])

        with tabs[2]:
            st.markdown(result["program_recommendation"])

        with tabs[3]:
            st.markdown(result["final_report"])
else:
    st.info(
        "Enter the applicant profile and paste the university's official requirements. "
        "The system will analyze them through four specialized CrewAI agents."
    )

st.divider()
st.caption(
    "Important: This is an AI advisory system. Final admission decisions must be confirmed "
    "with the university's official admissions office."
)

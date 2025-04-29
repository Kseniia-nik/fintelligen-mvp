# app.py — финальная улучшенная версия с современным графиком

import streamlit as st
import fitz  # PyMuPDF
import pandas as pd
import spacy
import docx
import uuid
import matplotlib.pyplot as plt

# Загрузка модели spaCy
import en_core_web_sm
nlp = en_core_web_sm.load()

# ----------------------- СТИЛЬ: ЛЁГКИЙ ФОН -----------------------
st.markdown(
    """
    <style>
        body { background-color: #f5f5f5; }
        .css-18e3th9 { background-color: #f5f5f5; }
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------------- ШАПКА: ЛОГО + БРЕНД -----------------------
col1, col2 = st.columns([1, 4])

with col1:
    st.image("https://raw.githubusercontent.com/Kseniia-nik/fintelligen-mvp/main/images/Goldman-Sachs.png", width=140)

with col2:
    st.markdown(
        """
        <h1 style='text-align: center; color: #004080;'>🧠 Fintelligen</h1>
        <h4 style='text-align: center; color: gray;'>AI Resume Evaluator</h4>
        <p style='text-align: center; color: darkred;'>Powered by Goldman Sachs Australia Graduate Criteria</p>
        """,
        unsafe_allow_html=True
    )

# ----------------------- INFO БЛОК -----------------------
st.info(
    "Upload one or more resumes (PDF or DOCX).\n\n"
    "This tool anonymizes personal information and evaluates key competencies aligned with Goldman Sachs Australia's graduate hiring criteria.\n\n"
    "**Scoring Methodology:**\n"
    "- Each mandatory skill match = 2 points\n"
    "- Each optional skill match = 1 point"
)

# ----------------------- СКИЛЛЫ -----------------------
mandatory_skills = [
    "financial analysis", "excel", "data analysis", "problem solving",
    "communication", "teamwork", "attention to detail",
    "critical thinking", "python", "valuation"
]

optional_skills = [
    "SQL", "powerpoint", "financial modeling", "presentation skills",
    "project management", "statistics", "machine learning",
    "risk management", "corporate finance", "investment banking knowledge"
]

# ----------------------- ФУНКЦИИ -----------------------
def extract_text_from_pdf(file):
    text = ""
    pdf = fitz.open(stream=file.read(), filetype="pdf")
    for page in pdf:
        text += page.get_text()
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join(p.text for p in doc.paragraphs)

def anonymize_text(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ in ['PERSON', 'GPE', 'ORG', 'DATE', 'LOC', 'EMAIL', 'PHONE', 'NORP']:
            text = text.replace(ent.text, f'[{ent.label_}]')
    return text

def find_skills(text, mandatory_skills, optional_skills):
    found_mandatory = [s for s in mandatory_skills if s.lower() in text.lower()]
    found_optional = [s for s in optional_skills if s.lower() in text.lower()]
    return found_mandatory, found_optional

# ----------------------- ЗАГРУЗКА РЕЗЮМЕ -----------------------
uploaded_files = st.file_uploader("Upload resumes", type=["pdf", "docx"], accept_multiple_files=True)

if uploaded_files:
    results = []
    for uploaded_file in uploaded_files:
        if uploaded_file.name.endswith(".pdf"):
            text = extract_text_from_pdf(uploaded_file)
        else:
            text = extract_text_from_docx(uploaded_file)

        anonymized_text = anonymize_text(text)
        unique_id = str(uuid.uuid4())[:8]
        filename = f"Candidate_{unique_id}.pdf"

        with st.expander(f"🔍 View Anonymized Resume: {filename}"):
            st.code(anonymized_text, language='markdown')

        mandatory, optional = find_skills(anonymized_text, mandatory_skills, optional_skills)
        score = len(mandatory) * 2 + len(optional)

        st.success(f"✅ Total Skill Score for {filename}: {score}")

        results.append({
            "Anonymized Resume Name": filename,
            "Mandatory Skills Found": len(mandatory),
            "Optional Skills Found": len(optional),
            "Total Score": score
        })

    if results:
        df = pd.DataFrame(results)
        st.subheader("📊 Summary Table:")
        st.dataframe(df)

        # ----------------------- СОВРЕМЕННЫЙ ГРАФИК -----------------------
        df_sorted = df.sort_values(by="Total Score", ascending=True)
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.barh(df_sorted["Anonymized Resume Name"], df_sorted["Total Score"], color="#1f77b4")
        ax.set_title("📈 Top Candidates by Total Score", fontsize=18, fontweight="bold", loc="left", pad=15)
        ax.set_xlabel("Total Score", fontsize=12)
        ax.set_ylabel("Candidate", fontsize=12)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(axis='x', linestyle='--', alpha=0.4)
        for bar in bars:
            ax.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height()/2, f"{int(bar.get_width())}", va='center', fontsize=11)
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10)
        st.pyplot(fig)

        # ----------------------- СКАЧАТЬ CSV -----------------------
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Summary CSV", csv, "resume_skill_evaluation_summary.csv", mime="text/csv")

# ----------------------- FAQ -----------------------
st.markdown("---")
st.subheader("📘 FAQ: Frequently Asked Questions")
with st.expander("🔹 What is considered a mandatory skill?"):
    st.write("Mandatory skills are core competencies such as financial analysis, data analysis, teamwork, communication, etc., required for success in Goldman Sachs Australia's graduate programs.")
with st.expander("🔹 How is the score calculated?"):
    st.write("Each mandatory skill match earns 2 points. Each optional skill match earns 1 point.")
with st.expander("🔹 What types of personal data are anonymized?"):
    st.write("Names, locations, organizations, email addresses, phone numbers, dates, and nationalities are anonymized to ensure unbiased evaluation.")

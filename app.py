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
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def anonymize_text(text):
    doc = nlp(text)
    anonymized_text = text
    for ent in doc.ents:
        if ent.label_ in ['PERSON', 'GPE', 'ORG', 'DATE', 'LOC', 'EMAIL', 'PHONE', 'NORP']:
            anonymized_text = anonymized_text.replace(ent.text, f'[{ent.label_}]')
    return anonymized_text

def find_skills(text, mandatory_skills, optional_skills):
    found_mandatory = []
    found_optional = []
    text_lower = text.lower()
    for skill in mandatory_skills:
        if skill.lower() in text_lower:
            found_mandatory.append(skill)
    for skill in optional_skills:
        if skill.lower() in text_lower:
            found_optional.append(skill)
    return found_mandatory, found_optional

# ----------------------- ФАЙЛЫ -----------------------
uploaded_files = st.file_uploader("Upload resumes", type=["pdf", "docx"], accept_multiple_files=True)

if uploaded_files:
    results = []

    for uploaded_file in uploaded_files:
        # Извлечение текста
        if uploaded_file.name.endswith(".pdf"):
            text = extract_text_from_pdf(uploaded_file)
        elif uploaded_file.name.endswith(".docx"):
            text = extract_text_from_docx(uploaded_file)
        else:
            st.warning(f"Unsupported file type: {uploaded_file.name}")
            continue

        anonymized_text = anonymize_text(text)
        unique_id = str(uuid.uuid4())[:8]
        anonymized_filename = f"Candidate_{unique_id}.pdf"

        with st.expander(f"🔍 View Anonymized Resume: {anonymized_filename}"):
            st.code(anonymized_text, language='markdown')

        mandatory, optional = find_skills(anonymized_text, mandatory_skills, optional_skills)
        score = len(mandatory) * 2 + len(optional)

        st.success(f"✅ Total Skill Score for {anonymized_filename}: {score}")

        results.append({
            "Anonymized Resume Name": anonymized_filename,
            "Mandatory Skills Found": len(mandatory),
            "Optional Skills Found": len(optional),
            "Total Score": score
        })

    if results:
        df = pd.DataFrame(results)
        st.subheader("📊 Summary Table:")
        st.dataframe(df)

        # BAR CHART
        st.subheader("📈 Top Candidates by Total Score")
        df_sorted = df.sort_values(by="Total Score", ascending=False)

        plt.figure(figsize=(10, 5))
        plt.barh(df_sorted["Anonymized Resume Name"], df_sorted["Total Score"], color='#0e6ba8')
        plt.xlabel("Total Score")
        plt.ylabel("Candidate")
        plt.title("Skill Match Comparison")
        plt.gca().invert_yaxis()
        st.pyplot(plt)

        # DOWNLOAD CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Summary CSV",
            data=csv,
            file_name='resume_skill_evaluation_summary.csv',
            mime='text/csv',
        )

# ----------------------- FAQ -----------------------
st.markdown("---")
st.subheader("📘 FAQ: Frequently Asked Questions")

with st.expander("🔹 What is considered a mandatory skill?"):
    st.write("Mandatory skills are core competencies such as financial analysis, data analysis, teamwork, communication, etc., required for success in Goldman Sachs Australia's graduate programs.")

with st.expander("🔹 How is the score calculated?"):
    st.write("Each mandatory skill match earns 2 points. Each optional skill match earns 1 point.")

with st.expander("🔹 What types of personal data are anonymized?"):
    st.write("Names, locations, organizations, email addresses, phone numbers, dates, and nationalities are anonymized to ensure unbiased evaluation.")

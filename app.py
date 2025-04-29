import streamlit as st
import fitz  # PyMuPDF
import pandas as pd
import spacy
import docx
import uuid  # для генерации уникальных ID

# Загрузка модели spaCy
import en_core_web_sm
nlp = en_core_web_sm.load()

# Навыки для оценки
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

# Функция извлечения текста из PDF
def extract_text_from_pdf(file):
    text = ""
    pdf = fitz.open(stream=file.read(), filetype="pdf")
    for page in pdf:
        text += page.get_text()
    return text

# Функция извлечения текста из DOCX
def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

# Анонимизация текста
def anonymize_text(text):
    doc = nlp(text)
    anonymized_text = text
    for ent in doc.ents:
        if ent.label_ in ['PERSON', 'GPE', 'ORG', 'DATE', 'LOC', 'EMAIL', 'PHONE', 'NORP']:
            anonymized_text = anonymized_text.replace(ent.text, f'[{ent.label_}]')
    return anonymized_text

# Поиск навыков
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

# Интерфейс Streamlit
st.markdown(
    """
    <h1 style='text-align: center; color: #004080;'>🧠 Fintelligen – Resume Anonymizer & Skill Evaluator</h1>
    <p style='text-align: center; color: darkred; font-weight: bold;'>
    Powered by Goldman Sachs Australia Graduate Hiring Criteria
    </p>
    """,
    unsafe_allow_html=True
)

st.info(
    "Upload one or more resumes (PDF or DOCX).\n\n"
    "This tool anonymizes personal information and evaluates key competencies aligned with Goldman Sachs Australia's graduate hiring criteria.\n\n"
    "**Scoring Methodology:**\n"
    "- Each mandatory skill match = 2 points\n"
    "- Each optional skill match = 1 point"
)

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

        # Генерация уникального анонимизированного имени
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
        st.subheader("Summary Table:")
        st.dataframe(df)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Summary CSV",
            data=csv,
            file_name='resume_skill_evaluation_summary.csv',
            mime='text/csv',
        )

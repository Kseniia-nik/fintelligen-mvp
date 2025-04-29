import streamlit as st
import fitz  # PyMuPDF
import pandas as pd
import spacy
import docx  # для .docx файлов

# Загрузка модели spaCy
import en_core_web_sm
nlp = en_core_web_sm.load()

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

# Анонимизация
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

# Основной интерфейс
st.title("Resume Anonymizer & Skill Evaluator - Fintelligen MVP")

uploaded_files = st.file_uploader("Choose resume files (PDF or DOCX)", type=["pdf", "docx"], accept_multiple_files=True)

if uploaded_files:
    results = []

    for uploaded_file in uploaded_files:
        if uploaded_file.name.endswith(".pdf"):
            text = extract_text_from_pdf(uploaded_file)
        elif uploaded_file.name.endswith(".docx"):
            text = extract_text_from_docx(uploaded_file)
        else:
            st.warning(f"Unsupported file type: {uploaded_file.name}")
            continue

        anonymized_text = anonymize_text(text)

        st.subheader(f"Anonymized Text Preview: {uploaded_file.name}")
        st.text_area("Anonymized Text", anonymized_text, height=300, key=uploaded_file.name)

        # Оценка навыков
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

        mandatory, optional = find_skills(anonymized_text, mandatory_skills, optional_skills)
        score = len(mandatory) * 2 + len(optional)

        results.append({
            "Resume": uploaded_file.name,
            "Mandatory Skills Found": mandatory,
            "Optional Skills Found": optional,
            "Score": score
        })

    df = pd.DataFrame(results)
    st.subheader("Summary Table:")
    st.dataframe(df)

    # Кнопка скачать CSV
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Summary CSV",
        data=csv,
        file_name='resume_skill_evaluation_summary.csv',
        mime='text/csv',
    )

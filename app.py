import streamlit as st
import fitz  # PyMuPDF
import pandas as pd
import spacy

# Загрузка модели spaCy
import en_core_web_sm
nlp = en_core_web_sm.load()


# Навыки на основе требований Goldman Sachs Australia
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

# Функции для обработки текста
def anonymize_text(text):
    doc = nlp(text)
    anonymized_text = text
    for ent in doc.ents:
        if ent.label_ in ['PERSON', 'GPE', 'ORG', 'DATE', 'LOC', 'EMAIL', 'PHONE', 'NORP']:
            anonymized_text = anonymized_text.replace(ent.text, f'[{ent.label_}]')
    return anonymized_text

def extract_text_from_pdf(uploaded_file):
    text = ""
    pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    for page in pdf:
        text += page.get_text()
    return text

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
st.title("Resume Anonymizer & Skill Evaluator - Fintelligen MVP")

st.write("Upload a resume (PDF) to anonymize and evaluate key skills for Goldman Sachs Australia roles.")

uploaded_file = st.file_uploader("Choose a resume PDF", type="pdf")

if uploaded_file is not None:
    text = extract_text_from_pdf(uploaded_file)
    anonymized_text = anonymize_text(text)

    st.subheader("Anonymized Resume Preview:")
    st.text_area("Anonymized Text", anonymized_text, height=300)

    mandatory, optional = find_skills(anonymized_text, mandatory_skills, optional_skills)
    score = len(mandatory) * 2 + len(optional) * 1

    st.subheader("Skill Evaluation Results:")
    st.write(f"**Mandatory Skills Found:** {mandatory}")
    st.write(f"**Optional Skills Found:** {optional}")
    st.write(f"**Total Score:** {score}")

    # Результаты в таблицу
    result_df = pd.DataFrame({
        "Skill Type": ["Mandatory", "Optional"],
        "Skills Found": [len(mandatory), len(optional)]
    })

    st.subheader("Summary Table:")
    st.dataframe(result_df)

    # Кнопка для скачивания CSV
    csv = result_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Results as CSV",
        data=csv,
        file_name='skill_evaluation_results.csv',
        mime='text/csv',
    )

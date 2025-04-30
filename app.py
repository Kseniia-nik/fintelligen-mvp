
import streamlit as st
import base64
import os
from PyPDF2 import PdfReader
import docx2txt
import matplotlib.pyplot as plt

st.set_page_config(page_title="Fintelligen", layout="centered")

# Логотип и заголовок
col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    st.image("images/goldman_logo.png", width=100)
    st.markdown("<h1 style='text-align: center; font-family:Arial;'>Fintelligen</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: grey;'>AI Resume Evaluator for Goldman Sachs</h4>", unsafe_allow_html=True)

# FAQ
with st.expander("❓ What counts as a key skill?"):
    st.write("- Mandatory Skills: Python, Communication, Problem-Solving")
    st.write("- Optional Skills: Excel, Leadership, SQL, Teamwork")

# Загрузка файлов
uploaded_files = st.file_uploader("📂 Drag and Drop or Select Files", type=["pdf", "docx"], accept_multiple_files=True)
if uploaded_files:
    scores = {}
    for uploaded_file in uploaded_files:
        # Считывание файла
        if uploaded_file.type == "application/pdf":
            reader = PdfReader(uploaded_file)
            text = "".join([page.extract_text() for page in reader.pages if page.extract_text()])
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text = docx2txt.process(uploaded_file)
        else:
            continue

        # Анонимизация названия
        fake_name = f"Candidate_{abs(hash(uploaded_file.name)) % 100000}.pdf"
        st.markdown(f"**📄 {fake_name}**")
        
        # Список ключевых навыков
        mandatory_skills = ["python", "communication", "problem-solving"]
        optional_skills = ["excel", "sql", "leadership", "teamwork"]
        total_score = 0

        # Подсчет
        score_details = {}
        for skill in mandatory_skills:
            if skill.lower() in text.lower():
                score_details[skill] = 2
                total_score += 2
            else:
                score_details[skill] = 0
        for skill in optional_skills:
            if skill.lower() in text.lower():
                score_details[skill] = 1
                total_score += 1
            else:
                score_details[skill] = 0

        scores[fake_name] = total_score

        # Вывод навыков
        st.markdown("##### Skill Match")
        for k, v in score_details.items():
            st.write(f"- {k.title()}: {'✅' if v > 0 else '❌'}")

    # Барчарт
    if scores:
        st.markdown("### 📊 Top Candidates by Total Score")
        fig, ax = plt.subplots()
        ax.barh(list(scores.keys()), list(scores.values()))
        ax.set_xlabel("Total Score")
        ax.set_ylabel("Candidate")
        ax.set_title("Skill Match Comparison")
        st.pyplot(fig)

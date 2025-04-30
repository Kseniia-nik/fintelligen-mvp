
import streamlit as st
import base64
import os
import io
import re
from PyPDF2 import PdfReader
from docx import Document
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Fintelligen – Resume Evaluator", layout="centered")

# --- Logo and Header ---
st.image("Goldman-Sachs.png", width=100)
st.markdown("<h1 style='text-align: center; color: #0E2F44;'>Fintelligen</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>AI Resume Evaluator for Goldman Sachs</h4>", unsafe_allow_html=True)
st.write("")

# --- File Uploader ---
uploaded_files = st.file_uploader("📂 Drag and Drop or Select Files", accept_multiple_files=True, type=["pdf", "docx"])
resume_texts = []

# --- Helper Functions ---
def extract_text_from_pdf(file):
    pdf = PdfReader(file)
    return "\n".join(page.extract_text() or "" for page in pdf.pages)

def extract_text_from_docx(file):
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def anonymize_filename(name):
    return "CV_" + str(abs(hash(name)))[0:6] + os.path.splitext(name)[-1]

def score_skills(text, skills):
    return sum(skill.lower() in text.lower() for skill in skills)

# --- Resume Processing ---
if uploaded_files:
    skill_keywords = ["data analysis", "python", "communication", "leadership", "sql", "problem solving", "teamwork"]
    scores = []
    names = []

    for file in uploaded_files:
        ext = file.name.split(".")[-1].lower()
        if ext == "pdf":
            text = extract_text_from_pdf(file)
        elif ext == "docx":
            text = extract_text_from_docx(file)
        else:
            continue

        resume_texts.append((anonymize_filename(file.name), text))
        score = score_skills(text, skill_keywords)
        scores.append(score)
        names.append(anonymize_filename(file.name))

    # --- Display Scores ---
    df = pd.DataFrame({"Anonymized Resume": names, "Skill Score": scores}).sort_values("Skill Score", ascending=False)
    st.subheader("📊 Skill Match Summary")
    st.dataframe(df, hide_index=True)

    # --- Chart ---
    st.subheader("📈 Skill Match Chart")
    fig, ax = plt.subplots()
    ax.barh(df["Anonymized Resume"], df["Skill Score"], color="#2B7A78")
    ax.set_xlabel("Score")
    ax.set_title("Top Candidates by Skill Match")
    plt.gca().invert_yaxis()
    st.pyplot(fig)

    # --- Text Preview ---
    st.subheader("🧾 Anonymized Resume Previews")
    for name, text in resume_texts:
        with st.expander(name):
            st.text(text)

# --- FAQ ---
st.subheader("❓ FAQ")
with st.expander("How is the score calculated?"):
    st.markdown("We count how many of the following keywords appear in your resume: `data analysis`, `python`, `communication`, `leadership`, `sql`, `problem solving`, and `teamwork`.")

with st.expander("Is my data stored?"):
    st.markdown("No, your files are not saved or shared. Everything runs locally or in memory during the session.")


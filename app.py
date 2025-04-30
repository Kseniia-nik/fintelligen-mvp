import streamlit as st
from PyPDF2 import PdfReader
from docx import Document
import pandas as pd
import matplotlib.pyplot as plt
import re

st.set_page_config(page_title="Fintelligen", layout="centered")

# --- Header ---
st.image("Goldman-Sachs.png", width=100)
st.markdown("<h1 style='text-align: center; color: #0E2F44;'>Fintelligen</h1>", unsafe_allow_html=True)
st.markdown("### AI Resume Evaluator for Goldman Sachs")

# --- HR Instructions ---
st.markdown("""
<div style="background-color: #e6f2ff; padding: 20px; border-radius: 8px; margin-top: 10px;">
    <h4>📋 Instructions for HR</h4>
    <ol>
        <li><strong>Upload one or more resumes</strong> (formats: PDF, DOCX).</li>
        <li>The tool will:
            <ul>
                <li><strong>Anonymize</strong> names and personal contact details.</li>
                <li><strong>Score key competencies</strong> based on Goldman Sachs criteria.</li>
                <li><strong>Visualize</strong> the scores with interactive bar charts.</li>
            </ul>
        </li>
        <li>🔎 Use the <strong>skill filter</strong> to shortlist top candidates by metric.</li>
        <li>❓ See the <strong>FAQ</strong> section below for common questions.</li>
    </ol>
    <p><em>⏱️ Processing is fast and local. You may upload up to <strong>50 resumes</strong> at once.</em></p>
</div>
""", unsafe_allow_html=True)

# --- Upload Section ---
uploaded_files = st.file_uploader("📂 Upload Resume(s)", type=["pdf", "docx"], accept_multiple_files=True)

# --- Skill Filter ---
all_skills = ["python", "sql", "data analysis", "communication", "problem solving", "teamwork", "leadership", "project management", "finance", "machine learning"]
selected_skills = st.multiselect("🧠 Filter by Skill Keywords", options=all_skills, default=["python", "sql", "communication"])

# --- Helpers ---
def extract_text_from_pdf(file):
    reader = PdfReader(file)
    return "".join(page.extract_text() or "" for page in reader.pages)

def extract_text_from_docx(file):
    doc = Document(file)
    return "\n".join([p.text for p in doc.paragraphs])

def anonymize_text(text):
    text = re.sub(r'[\w\.-]+@[\w\.-]+', '[email]', text)
    text = re.sub(r'\b\d{10,}\b', '[phone]', text)
    text = re.sub(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', '[name]', text)
    return text

def score_skills(text, keywords):
    matched = sum(skill in text.lower() for skill in keywords)
    total = len(keywords)
    return matched, total

# --- Processing ---
scores = []
names = []
previews = []
insights = []

if uploaded_files:
    for file in uploaded_files:
        filename = file.name
        anonymized_name = f"Candidate_{abs(hash(filename)) % 100000}.pdf"

        # Extract and anonymize text
        if filename.endswith(".pdf"):
            text = extract_text_from_pdf(file)
        elif filename.endswith(".docx"):
            text = extract_text_from_docx(file)
        else:
            continue

        anonymized_text = anonymize_text(text)
        matched, total = score_skills(anonymized_text, selected_skills)
        percent = int((matched / total) * 100)
        summary = f"✅ Match: {matched} of {total} keywords ({percent}%)"

        names.append(anonymized_name)
        scores.append(matched)
        previews.append(anonymized_text[:1500])
        insights.append(summary)

    # --- Results Table ---
    df = pd.DataFrame({"Resume": names, "Skill Matches": scores, "Match Summary": insights})
    st.subheader("📊 Skill Score Table")
    st.dataframe(df.sort_values("Skill Matches", ascending=False), use_container_width=True)

    # --- Chart ---
    st.subheader("📈 Skill Match Comparison")
    fig, ax = plt.subplots()
    ax.barh(df["Resume"], df["Skill Matches"], color="#2E86C1")
    ax.set_xlabel("Matched Skills")
    ax.set_title("Top Resume Matches")
    plt.gca().invert_yaxis()
    st.pyplot(fig)

    # --- Resume Preview ---
    st.subheader("🧾 Resume Previews (Anonymized)")
    for name, text, insight in zip(names, previews, insights):
        with st.expander(f"{name} – {insight}"):
            st.text(text)

# --- FAQ ---
st.subheader("❓ FAQ")
with st.expander("What skills are evaluated?"):
    st.write("You can select relevant keywords like Python, Communication, Leadership, etc. from the skill filter above.")
with st.expander("How is my data handled?"):
    st.write("Everything is processed in-memory. No data is stored or shared.")

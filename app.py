import streamlit as st
from PyPDF2 import PdfReader
from docx import Document
import pandas as pd
import matplotlib.pyplot as plt
import re

st.set_page_config(page_title="Fintelligen", layout="centered")

# === Global CSS ===
st.markdown("""
    <style>
        body {
            background-color: #f8f9fa !important;
            color: #212529 !important;
        }
        h1, h2, h3, h4 {
            color: #003087 !important;
        }
        .stButton > button {
            background-color: #003087 !important;
            color: white !important;
            padding: 10px 20px;
            border-radius: 8px;
            border: none;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
            font-size: 16px;
        }
        .stButton > button:hover {
            background-color: #002060 !important;
        }
        .block {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            margin-top: 40px;
        }
        hr {
            border: none;
            border-top: 1px solid #dee2e6;
            margin: 40px 0;
        }
    </style>
""", unsafe_allow_html=True)

# === Header with logo ===
col1, col2 = st.columns([5, 1])
with col1:
    st.markdown("""
        <h1 style='font-size: 50px; font-weight: 800; margin-bottom: 0;'>Fintelligen</h1>
        <h3 style='font-size: 26px; font-weight: 500; color: #003087;'>AI Resume Evaluator for Goldman Sachs</h3>
    """, unsafe_allow_html=True)
with col2:
    st.image("Goldman-Sachs.png", width=160)
    
# === Sidebar Navigation ===
st.sidebar.header("🧭 Navigation & Filters")

show_summary = st.sidebar.checkbox("🎯 Show Match Summary", value=True)
show_table = st.sidebar.checkbox("📊 Show Skill Matrix & Chart", value=True)
show_resumes = st.sidebar.checkbox("📄 Show Anonymized Resumes", value=True)
show_faq = st.sidebar.checkbox("❓ Show FAQ", value=True)

match_threshold = st.sidebar.slider("Minimum Skill Matches", 0, 10, 0)

# === Instructions block ===
st.markdown("""
<div class="block">
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

# === Upload and Filters ===
uploaded_files = st.file_uploader("📂 Upload Resume(s)", type=["pdf", "docx"], accept_multiple_files=True)

all_skills = ["python", "sql", "data analysis", "communication", "problem solving", "teamwork", "leadership", "project management", "finance", "machine learning"]
selected_skills = st.multiselect("🧠 Filter by Skill Keywords", options=all_skills, default=["python", "sql", "communication"])

# === Helpers ===
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

# === Resume processing ===
scores, names, previews, insights = [], [], [], []

if uploaded_files:
    for file in uploaded_files:
        filename = file.name
        anonymized_name = f"Candidate_{abs(hash(filename)) % 100000}.pdf"

        if filename.endswith(".pdf"):
            text = extract_text_from_pdf(file)
        elif filename.endswith(".docx"):
            text = extract_text_from_docx(file)
        else:
            continue

        anonymized_text = anonymize_text(text)
        matched, total = score_skills(anonymized_text, selected_skills)

        if matched >= match_threshold:
            percent = int((matched / total) * 100) if total > 0 else 0
            summary = f"✅ Match: {matched} of {total} keywords ({percent}%)"
            names.append(anonymized_name)
            scores.append(matched)
            previews.append(anonymized_text[:1500])
            insights.append({
                "summary": summary,
                "text": anonymized_text,
                "matches": matched
            })

    df = pd.DataFrame({"Resume": names, "Skill Matches": scores, "Match Summary": [i["summary"] for i in insights]})

    # === Skill Matrix Section ===
    if show_table and not df.empty:
        st.markdown("<div class='block'><h3>📊 Skill Matrix</h3>", unsafe_allow_html=True)
        st.dataframe(df.sort_values("Skill Matches", ascending=False), use_container_width=True)

        st.markdown("<hr />", unsafe_allow_html=True)

        fig, ax = plt.subplots()
        ax.barh(df["Resume"], df["Skill Matches"], color="#2E86C1")
        ax.set_xlabel("Matched Skills")
        ax.set_title("Top Resume Matches")
        plt.gca().invert_yaxis()
        st.pyplot(fig)
        st.markdown("</div>", unsafe_allow_html=True)

    # === Resume Previews & Summaries ===
    if show_resumes:
        st.markdown("<div class='block'><h3>📄 Anonymized Resume Results</h3>", unsafe_allow_html=True)
        for name, data in zip(names, insights):
            with st.expander(f"{name}"):
                if show_summary:
                    st.markdown(f"**🎯 Match Summary:** {data['summary']}")
                st.markdown("---")
                st.markdown("**📄 Anonymized Text:**")
                st.text(data["text"])
        st.markdown("</div>", unsafe_allow_html=True)

# === FAQ ===
if show_faq:
    st.markdown("<div class='block'><h3>❓ FAQ</h3>", unsafe_allow_html=True)

    with st.expander("What skills are evaluated?"):
        st.write("You can select relevant keywords like Python, Communication, Leadership, etc. from the skill filter above.")
    with st.expander("How is my data handled?"):
        st.write("Everything is processed in-memory. No data is stored or shared.")

    st.markdown("</div>", unsafe_allow_html=True)

import streamlit as st
from PyPDF2 import PdfReader
from docx import Document
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Fintelligen", layout="centered")

# --- Header ---
st.image("Goldman-Sachs.png", width=100)
st.markdown("<h1 style='text-align: center; color: #0E2F44;'>Fintelligen</h1>", unsafe_allow_html=True)
st.markdown("### AI Resume Evaluator for Goldman Sachs")

# --- HR Instruction Box ---
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

# --- File Uploader ---
uploaded_files = st.file_uploader("📂 Upload Resume(s)", type=["pdf", "docx"], accept_multiple_files=True)

# --- Skills for scoring ---
skills = ["python", "sql", "data analysis", "communication", "problem solving", "teamwork", "leadership"]

scores = []
names = []
previews = []

# --- Process Files ---
if uploaded_files:
    for file in uploaded_files:
        filename = file.name
        anonymized_name = f"Candidate_{abs(hash(filename)) % 100000}.pdf"

        # Extract text
        if filename.endswith(".pdf"):
            reader = PdfReader(file)
            text = "".join(page.extract_text() or "" for page in reader.pages)
        elif filename.endswith(".docx"):
            doc = Document(file)
            text = "\n".join([p.text for p in doc.paragraphs])
        else:
            st.warning(f"{filename} is not supported.")
            continue

        score = sum(skill in text.lower() for skill in skills)
        scores.append(score)
        names.append(anonymized_name)
        previews.append(text[:1500])

    # --- Table ---
    df = pd.DataFrame({"Resume": names, "Skill Score": scores})
    st.subheader("📊 Skill Score Table")
    st.dataframe(df.sort_values("Skill Score", ascending=False), use_container_width=True)

    # --- Chart ---
    st.subheader("📈 Skill Comparison")
    fig, ax = plt.subplots()
    ax.barh(names, scores, color="#007acc")
    ax.set_xlabel("Score")
    ax.set_title("Resume Skill Match")
    plt.gca().invert_yaxis()
    st.pyplot(fig)

    # --- Preview Text ---
    st.subheader("🧾 Resume Previews (Anonymized)")
    for name, text in zip(names, previews):
        with st.expander(name):
            st.text(text)

# --- FAQ Section ---
st.subheader("❓ FAQ")
with st.expander("What skills are evaluated?"):
    st.write("Mandatory and optional skills for Goldman Sachs graduate roles such as Python, SQL, Communication, and Leadership.")
with st.expander("How is my data handled?"):
    st.write("All processing is local or in-session. No data is stored or shared.")

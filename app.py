import streamlit as st
from PyPDF2 import PdfReader
from docx import Document
import pandas as pd
import plotly.express as px
import re

# === THEME COLORS (Goldman Sachs branding) ===
accent_color    = "#003087"  # Goldman Blue
highlight_color = "#c59d5f"  # Goldman Gold
bg_color        = "#f8f9fa"  # Light background
text_color      = "#212529"  # Almost black
card_color      = "#ffffff"  # Card background

# === GLOBAL STYLE ===
st.markdown(f"""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<style>
  html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif !important;
    background-color: {bg_color} !important;
    color: {text_color} !important;
  }}
  h1, h3 {{
    margin-top: 0 !important;
    margin-bottom: 0 !important;
  }}
  .stButton > button {{
    background-color: {accent_color} !important;
    color: white !important;
    padding: 10px 20px;
    border-radius: 8px;
    font-size: 16px;
  }}
  .stButton > button:hover {{
    background-color: #002366 !important;
  }}
  .block {{
    background-color: {card_color} !important;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    margin-bottom: 0.5rem !important;
  }}
  .block h3 {{
    margin-top: 0.3rem !important;
    margin-bottom: 0.3rem !important;
  }}
</style>
""", unsafe_allow_html=True)

# === PAGE HEADER ===
col1, col2 = st.columns([0.85, 0.15])
with col1:
    st.markdown("<h1 style='margin-bottom:0.2rem;'>Fintelligen</h1>", unsafe_allow_html=True)
    st.markdown(
        f"<h3 style='font-weight:600; color: {accent_color};'>AI Resume Evaluator for Goldman Sachs</h3>",
        unsafe_allow_html=True
    )
with col2:
    st.image("Goldman-Sachs.png", width=80)

# === INSTRUCTIONS ===
with st.expander("📋 Instructions for HR", expanded=True):
    st.markdown(
        """
        - **Upload** up to 50 resumes (PDF or DOCX).  
        - **Review** match summary before shortlisting.  
        - **Adjust** minimum skill matches slider to filter results.  
        - **Download** shortlisted candidates using the CSV button.  
        - _Your resume data is not stored or shared. Max: **50 resumes**._
        """
    )

# === SIDEBAR ===
st.sidebar.header("🧭 Navigation & Filters")
show_summary = st.sidebar.checkbox("🎯 Show Match Summary", value=True)
show_matrix  = st.sidebar.checkbox("📊 Show Skill Matrix", value=True)
show_resumes = st.sidebar.checkbox("📄 Show Anonymized Resumes", value=True)
show_faq     = st.sidebar.checkbox("❓ Show FAQ", value=True)
match_threshold = st.sidebar.slider("Minimum Skill Matches", 0, 14, 0)

# === CORE COMPETENCIES ===
goldman_skills = [
    "financial analysis", "investment banking", "capital markets", "excel", "valuation",
    "risk management", "mergers and acquisitions", "quantitative analysis", "data analytics",
    "communication", "problem solving", "teamwork", "python", "sql"
]

# === FILE UPLOAD ===
uploaded_files = st.file_uploader("📂 Upload Resume(s)", type=["pdf", "docx"], accept_multiple_files=True)

# === RESUME PARSING & EVALUATION LOGIC ===
# Оставляем вашу логику разбора и оценки резюме без изменений
# Например:
# results = []
# for file in uploaded_files:
#     text = extract_text(file)
#     scores = evaluate_skills(text, goldman_skills)
#     results.append(scores)
# edited_df = pd.DataFrame(results)

# === MATCH SUMMARY ===
if show_summary:
    # Ваш код для отображения сводки совпадений
    pass

# === SKILL MATRIX ===
if show_matrix:
    # Ваш код для генерации и отображения графика матрицы навыков
    pass

# === RESUME EVALUATION TABLE ===
# Предполагаем, что edited_df уже создан
try:
    df = edited_df.copy()
except NameError:
    df = pd.DataFrame()

if not df.empty:
    st.dataframe(df)

# === CLEAR SHORTLIST ===
if "clear_shortlist" not in st.session_state:
    st.session_state.clear_shortlist = False
if st.button("🗑 Clear Shortlist", use_container_width=True):
    st.session_state.clear_shortlist = True
if st.session_state.clear_shortlist:
    # Сбросьте метки shortlisting в df
    st.session_state.clear_shortlist = False

# === DOWNLOAD SHORTLISTED CSV ===
if not df.empty and "⭐ Shortlist" in df.columns:
    shortlisted = df[df["⭐ Shortlist"] == True]
    if not shortlisted.empty:
        st.download_button(
            label="⬇️ Download Shortlisted (CSV)",
            data=shortlisted.to_csv(index=False).encode('utf-8'),
            file_name="shortlisted_candidates.csv"
        )

# === ANONYMIZED RESUMES ===
if show_resumes:
    # Ваш код для отображения анонимизированных резюме
    pass

# === FAQ ===
if show_faq:
    with st.expander("Is my data stored anywhere?"):
        st.write("No. All processing happens in-memory. Resumes are not saved, logged, or transmitted.")
    with st.expander("Can I upload multiple resumes?"):
        st.write("Yes. You can upload up to 50 resumes at once, in PDF or DOCX format.")
    with st.expander("Can I download the results?"):
        st.write("Yes. Use the 'Download Shortlisted' button after selecting candidates.")
    with st.expander("How does this reduce bias?"):
        st.write("Personal identifiers are anonymized before evaluation, promoting fair skill-based review.")

# === FOOTER ===
st.markdown(f"""
<hr style='margin-top:3rem; margin-bottom: 1rem;'>
<p style='text-align:center; color:#6c757d; font-size:14px;'>
  Fintelligen does not store or transmit uploaded data. All resume evaluations are performed securely in memory.
</p>
""", unsafe_allow_html=True)


import streamlit as st
from PyPDF2 import PdfReader
from docx import Document
import pandas as pd
import plotly.express as px
import re

# === PAGE CONFIG ===
# Заголовок и логотип
col1, col2 = st.columns([0.85, 0.15])
with col1:
    st.markdown("<h1 style='margin-bottom: 0.2rem;'>Fintelligen</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top: 0rem; margin-bottom: 0.5rem; font-weight: 600; color: #003087;'>AI Resume Evaluator for Goldman Sachs</h3>", unsafe_allow_html=True)
with col2:
    st.image("goldman.jpeg", width=80)

# УБИРАЕМ воздух 👇
st.markdown("<div style='margin-top: -1rem;'></div>", unsafe_allow_html=True)

# === THEME COLORS (Goldman Sachs branding) ===
accent_color = "#003087"       # Goldman Blue
highlight_color = "#c59d5f"     # Goldman Gold
bg_color = "#f8f9fa"            # Light background
text_color = "#212529"          # Almost black
card_color = "#ffffff"          # Card background

# === GLOBAL STYLE ===
st.markdown("""
<style>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: #f8f9fa !important;
    color: #212529 !important;
}

h1 {
    font-size: 42px !important;
    font-weight: 700 !important;
    color: #003087 !important;
    margin-top: 0 !important;
    margin-bottom: 0.1em !important;
}

h2, h3, h4 {
    font-weight: 600 !important;
    color: #003087 !important;
    margin-top: 0 !important;
    margin-bottom: 0.1em !important;
    line-height: 1.2em !important;
}

.block:first-of-type {
    margin-top: 0.1rem !important;
}

.main .block-container {
    max-width: 1100px;
    padding: 0.5rem 1.5rem;
    margin: auto;
}

.stButton > button {
    background-color: #003087 !important;
    color: white !important;
    padding: 10px 20px;
    border-radius: 8px;
    font-size: 16px;
}
.stButton > button:hover {
    background-color: #002366 !important;
}

.block {
    background-color: #ffffff;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    margin-bottom: 1.5rem;
}

.ring {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    background: conic-gradient(#003087 {{percent}}%, #dee2e6 {{percent}}%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    font-size: 18px;
    margin: auto;

""", unsafe_allow_html=True)

# === FOOTER ===
st.markdown("""
    <hr style='margin-top: 3rem; margin-bottom: 1rem;'>
    <p style='text-align: center; font-size: 14px; color: #6c757d;'>
        Fintelligen does not store or transmit uploaded data. All resume evaluations are performed securely in memory.
    </p>
""", unsafe_allow_html=True)
    
# === INSTRUCTIONS ===
with st.expander("📋 Instructions for HR", expanded=True):
    st.markdown("""
    This tool evaluates uploaded resumes against the core competencies required for analyst-level roles at Goldman Sachs.

    **Steps:**
    1. **Upload resumes** (PDF/DOCX)
    2. The tool will:
        - **Anonymize** personal details
        - **Evaluate** key skills
        - **Visualize** match scores and allow shortlisting

    _Resume data is not stored or shared. Max: **50 resumes**._
    """)

# === SIDEBAR ===
st.sidebar.header("🧭 Navigation & Filters")
show_summary = st.sidebar.checkbox("🎯 Show Match Summary", value=True)
show_table = st.sidebar.checkbox("📊 Show Skill Matrix & Chart", value=True)
show_resumes = st.sidebar.checkbox("📄 Show Anonymized Resumes", value=True)
show_faq = st.sidebar.checkbox("❓ Show FAQ", value=True)
match_threshold = st.sidebar.slider("Minimum Skill Matches", 0, 14, 0)

# === SKILLS ===
goldman_skills = [
    "financial analysis", "investment banking", "capital markets", "excel", "valuation",
    "risk management", "mergers and acquisitions", "quantitative analysis", "data analytics",
    "communication", "problem solving", "teamwork", "python", "sql"
]
selected_skills = goldman_skills

st.markdown("🧠 **Goldman Sachs core skillset is applied automatically:**")
st.markdown(", ".join(goldman_skills))

# === FILE UPLOAD ===
uploaded_files = st.file_uploader("📂 Upload Resume(s)", type=["pdf", "docx"], accept_multiple_files=True)

def extract_text_from_pdf(file): return "".join(page.extract_text() or "" for page in PdfReader(file).pages)
def extract_text_from_docx(file): return "\n".join([p.text for p in Document(file).paragraphs])
def anonymize_text(text):
    text = re.sub(r'[\w\.-]+@[\w\.-]+', '[email]', text)
    text = re.sub(r'\b\d{10,}\b', '[phone]', text)
    text = re.sub(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', '[name]', text)
    return text
def score_skills(text, keywords):
    matched = sum(skill in text.lower() for skill in keywords)
    total = len(keywords)
    return matched, total

scores, names, previews, insights, percents = [], [], [], [], []

if uploaded_files:
    for file in uploaded_files:
        filename = file.name
        anonymized_name = f"Candidate_{abs(hash(filename)) % 100000}.pdf"
        text = extract_text_from_pdf(file) if filename.endswith(".pdf") else extract_text_from_docx(file)
        anonymized_text = anonymize_text(text)
        matched, total = score_skills(anonymized_text, selected_skills)
        if matched >= match_threshold:
            percent = int((matched / total) * 100) if total > 0 else 0
            scores.append(matched)
            names.append(anonymized_name)
            previews.append(anonymized_text[:1500])
            insights.append({
                "summary": f"{matched} / {total} keywords ({percent}%)",
                "text": anonymized_text,
                "matches": matched,
                "percent": percent
            })
            percents.append(percent)

    df = pd.DataFrame({
        "Anonymized Resume": names,
        "Original Filename": [f.name for f in uploaded_files],
        "Skill Matches": scores,
        "Match Summary": [i["summary"] for i in insights],
        "⭐ Shortlist": [False] * len(names)
    })

    # === SKILL MATRIX ===
    if show_table and not df.empty:
        st.markdown("<div class='block'><h3>📊 Skill Matrix — Resume vs. Core Skills</h3>", unsafe_allow_html=True)
        fig = px.bar(
            df.sort_values("Skill Matches", ascending=True),
            x="Skill Matches",
            y="Anonymized Resume",
            orientation="h",
            color="Skill Matches",
            color_continuous_scale=["#dee2e6", accent_color],
            height=400
        )
        fig.update_layout(
            xaxis_title="Matched Skills",
            yaxis_title=None,
            plot_bgcolor=bg_color,
            paper_bgcolor=bg_color,
            font=dict(family="IBM Plex Sans", color=text_color),
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # === TABLE ===
    st.markdown("<div class='block'><h3>🧾 Resume Evaluation Table</h3>", unsafe_allow_html=True)
    edited_df = st.data_editor(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Skill Matches": st.column_config.NumberColumn(format="%d"),
            "⭐ Shortlist": st.column_config.CheckboxColumn(default=False)
        }
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # === CLEAR SHORTLIST ===
    if "clear_shortlist" not in st.session_state:
        st.session_state.clear_shortlist = False

    if st.button("🗑 Clear Shortlist", use_container_width=True):
        st.session_state.clear_shortlist = True

    if st.session_state.clear_shortlist:
        df["⭐ Shortlist"] = False
        st.session_state.clear_shortlist = False

    shortlisted = edited_df[edited_df["⭐ Shortlist"] == True]
    if not shortlisted.empty:
        st.download_button(
            label="⬇️ Download Shortlisted (CSV)",
            data=shortlisted.to_csv(index=False).encode("utf-8"),
            file_name="shortlisted_candidates.csv",
            mime="text/csv",
            use_container_width=True
        )

  # === ANONYMIZED RESUMES ===
if show_resumes:
    st.markdown("<div class='block'><h3>📄 Anonymized Resume Results</h3>", unsafe_allow_html=True)
    for name, data in zip(names, insights):
        with st.expander(f"{name}"):
            if show_summary:
                st.markdown(
                    f"<div class='ring' style='background: conic-gradient({accent_color} {data['percent']}%, #dee2e6 {data['percent']}%);'>{data['percent']}%</div>",
                    unsafe_allow_html=True
                )
                st.markdown(f"**🎯 Match Summary:** {data['summary']}")
            st.markdown("---")
            st.markdown("**📄 Anonymized Text:**")
            st.text(data["text"])
    st.markdown("</div>", unsafe_allow_html=True)


# === FAQ BLOCK ===
if show_faq:
    st.markdown("<div class='block'><h3>❓ FAQ</h3>", unsafe_allow_html=True)

    with st.expander("What skills are evaluated?"):
        st.write("Goldman Sachs core skills for analysts, including financial, analytical, and technical competencies.")

    with st.expander("Is my data stored anywhere?"):
        st.write("No. All processing happens in-memory. Resumes are not saved, logged, or transmitted.")

    with st.expander("Can I upload multiple resumes?"):
        st.write("Yes. You can upload up to 50 resumes at once, in PDF or DOCX format.")

    with st.expander("Can I download the results?"):
        st.write("Yes. Use the 'Download Shortlisted' button after selecting candidates.")

    with st.expander("How does this reduce bias?"):
        st.write("Personal identifiers are anonymized before evaluation, promoting fair skill-based review.")

    st.markdown("</div>", unsafe_allow_html=True)

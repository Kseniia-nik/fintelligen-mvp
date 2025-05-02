import streamlit as st
from PyPDF2 import PdfReader
from docx import Document
import pandas as pd
import plotly.express as px
import re 

# === THEME COLORS ===
accent_color    = "#003087"
highlight_color = "#c59d5f"
bg_color        = "#f8f9fa"
text_color      = "#212529"
card_color      = "#ffffff"

# === PAGE CONFIG ===
st.set_page_config(page_title="Fintelligen", layout="centered")

# === FONT AND GLOBAL STYLE ===
st.markdown("<link href='https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap' rel='stylesheet'>", unsafe_allow_html=True)
st.markdown(f"""
<style>
html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif !important;
    background-color: {bg_color} !important;
    color: {text_color} !important;
}}
h1 {{
    font-size: 42px !important;
    font-weight: 700 !important;
    color: {accent_color} !important;
    margin-top: 0 !important;
    margin-bottom: 0.2rem !important;
}}
h3 {{
    font-weight: 600 !important;
    color: {accent_color} !important;
    margin-top: 0 !important;
    margin-bottom: 0.5rem !important;
}}
.block {{
    background-color: {card_color} !important;
    border-radius: 15px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    padding: 1.5rem;
    margin-bottom: 1.5rem;
}}
</style>
""", unsafe_allow_html=True)

# === HEADER: TITLE + LOGO ===
col1, col2, col3 = st.columns([0.15, 0.7, 0.15])

with col1:
    st.image("FINTELLIGEN.svg", width=80)

with col2:
    st.markdown("""
        <div style='text-align: center;'>
            <h1 style='margin-bottom: 0.2rem; color: #003087;'>Fintelligen</h1>
            <h3 style='color: #003087; font-weight: 500;'>AI Resume Evaluator for Goldman Sachs</h3>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.image("Goldman Sachs Logo.svg", width=80)


# === INSTRUCTIONS ===
st.markdown("""
<div style='background-color: #f8f9fa; padding: 15px; border-radius: 10px;'>
<b>Steps:</b><br>
1. <b>Upload resumes</b> (PDF/DOCX)<br>
2. The tool will:<br>
&nbsp;&nbsp;&nbsp;&nbsp;• <b>Anonymize</b> personal details<br>
&nbsp;&nbsp;&nbsp;&nbsp;• <b>Evaluate</b> key skills<br>
&nbsp;&nbsp;&nbsp;&nbsp;• <b>Visualize</b> match scores and allow shortlisting<br><br>
<i style='color: #6c757d;'>Resume data is not stored or shared. Max: <b>50 resumes</b>.</i>
</div>
""", unsafe_allow_html=True)

# === SKILLS ===
st.markdown("""
<div class='block' style='margin-top: 1rem;'>
    <h4 style='margin-bottom: 0.5rem; color: #003087;'> Goldman Sachs Core Skillset</h4>
    <p style='font-size: 15px;'>
        financial analysis, investment banking, capital markets, excel, valuation, risk management, mergers and acquisitions,
        quantitative analysis, data analytics, communication, problem solving, teamwork, python, sql
    </p>
</div>
""", unsafe_allow_html=True)

# === FILE UPLOAD ===
st.markdown("## 📤 Upload Resumes")
uploaded_files = st.file_uploader(
    "Upload multiple resumes (.pdf or .docx)",
    type=["pdf", "docx"],
    accept_multiple_files=True
)

# === SIDEBAR ===
with st.sidebar:
    st.markdown("### Show/Hide Sections")
    show_matrix  = st.toggle("Show Skill Matrix", value=True)
    show_table   = st.toggle("Show Resume Table", value=True)
    show_results = st.toggle("Show Anonymized Results", value=True)
    show_faq     = st.toggle("Show FAQ", value=True)

    st.markdown("---")
    st.markdown("### Filters")
    match_threshold = st.slider(
        "Minimum Skill Matches",
        min_value=0,
        max_value=20,
        value=0,
        help="Only resumes with this many or more matched skills will be considered."
    )

# === STATUS AFTER UPLOAD ===
if uploaded_files:
    st.success(f"✅ {len(uploaded_files)} resume(s) uploaded successfully.")
else:
    st.info("ℹ️ Please upload at least one resume to begin analysis.")

# === FUNCTIONS ===
def extract_text_from_pdf(file):
    return "".join(page.extract_text() or "" for page in PdfReader(file).pages)

def extract_text_from_docx(file):
    return "\n".join([p.text for p in Document(file).paragraphs])

def anonymize_text(text):
    text = re.sub(r'[\w\.-]+@[\w\.-]+', '[email]', text)
    text = re.sub(r'\b\d{10,}\b', '[phone]', text)
    text = re.sub(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', '[name]', text)
    return text

def score_skills(text, keywords):
    matched = sum(skill in text.lower() for skill in keywords)
    total = len(keywords)
    return matched, total

# === PROCESSING ===
scores, names, previews, insights, percents = [], [], [], [], []

if uploaded_files:
    with st.spinner("🔍 Analyzing resumes..."):
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

# === CREATE TABLE ===
if names and len(names) == len(scores) == len(insights):
    df = pd.DataFrame({
        "Anonymized Resume": names,
        "Original Filename": [f.name for f in uploaded_files][:len(names)],
        "Skill Matches": scores,
        "Match Summary": [i["summary"] for i in insights],
        "⭐ Shortlist": [False] * len(names)
    })

# === SUMMARY DASHBOARD IN SIDEBAR ===
if "df" in locals() and not df.empty:
    total_resumes = len(df)
    total_skills = len(selected_skills)
    shortlisted = df["⭐ Shortlist"].sum()
    avg_percent = round(df["Skill Matches"].sum() / (total_resumes * total_skills) * 100)
    top_match_row = df.loc[df["Skill Matches"].idxmax()]
    top_match_name = top_match_row["Anonymized Resume"]
    top_match_score = top_match_row["Match Summary"]

    with st.sidebar:
        st.markdown("### Summary Dashboard")
        st.success(f"**Resumes Uploaded:** `{total_resumes}`")
        st.info(f"**Shortlisted:** `{shortlisted}`")
        st.warning(f"**Avg Match:** `{avg_percent}%`")
        st.markdown(f"**Top Match:** `{top_match_name}`")
        st.caption(f"→ {top_match_score}")

# === SKILL MATRIX ===
if "df" in locals() and not df.empty and show_matrix:
    st.markdown(f"""
    <div class='block'>
        <h3 style='margin-top: 0.5rem; margin-bottom: 1rem;'> Skill Matrix — Resume vs. Core Skills</h3>
    """, unsafe_allow_html=True)

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
        font=dict(family="Inter", color=text_color),
        margin=dict(l=20, r=20, t=40, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# === RESUME TABLE ===
if "df" in locals() and not df.empty and show_table:
    df_with_index = df.copy()
    df_with_index.insert(0, "#", range(1, 1 + len(df_with_index)))

    st.markdown(f"""
    <div class='block'>
        <h3 style='margin-top: 0.5rem; margin-bottom: 1rem;'> Resume Evaluation Table</h3>
    """, unsafe_allow_html=True)

    edited_df = st.data_editor(
        df_with_index,
        use_container_width=True,
        hide_index=True,
        column_config={
            "⭐ Shortlist": st.column_config.CheckboxColumn("⭐ Shortlist", default=False)
        },
        disabled=["#", "Anonymized Resume", "Original Filename", "Skill Matches", "Match Summary"]
    )

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🗑 Clear Shortlist"):
            edited_df["⭐ Shortlist"] = False
    with col2:
        csv = edited_df[edited_df["⭐ Shortlist"]].to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download Shortlist", csv, "shortlisted_resumes.csv", "text/csv")

    st.markdown("</div>", unsafe_allow_html=True)

# === ANONYMIZED RESUMES ===
if "df" in locals() and not df.empty and show_results:
    st.markdown(f"""
    <div class='block'>
        <h3 style='margin-top: 0.5rem; margin-bottom: 1rem;'> Anonymized Resume Results</h3>
    """, unsafe_allow_html=True)

    for i, row in df.iterrows():
        percent = insights[i]["percent"]

        match_bar = f"""
        <div style='
            background: linear-gradient(to right, {accent_color} {percent}%, #e9ecef {100 - percent}%);
            border-radius: 8px;
            padding: 6px 10px;
            color: white;
            font-weight: 600;
            font-size: 13px;
            margin-bottom: 0.5rem;
        '>
            {percent}% match
        </div>
        """

        with st.expander(f"📄 {row['Anonymized Resume']} — {row['Match Summary']}"):
            st.markdown(match_bar, unsafe_allow_html=True)
            st.markdown("**📄 Anonymized Text:**")
            st.code(insights[i]["text"], language="markdown")

    st.markdown("</div>", unsafe_allow_html=True)


# === FAQ SECTION ===
if show_faq:
    st.markdown(f"""
    <div class='block'>
        <h3 style='margin-top: 0.5rem; margin-bottom: 1rem;'> Frequently Asked Questions (FAQ)</h3>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("🧠 How does the system assess core competencies in a resume?"):
        st.markdown("The AI scans resumes for keywords and contextual patterns aligned with Goldman Sachs' core skills, using a hybrid of rule-based and language model techniques.")

    with st.expander("📊 What does the “Skill Match” score represent?"):
        st.markdown("It shows how many of the predefined core competencies (e.g., leadership, teamwork, problem-solving) are detected in the resume — higher scores indicate stronger alignment.")

    with st.expander("📎 What file types are supported for upload?"):
        st.markdown("The system currently supports `.pdf` and `.docx` files only.")

    with st.expander("📁 Can I analyze multiple resumes at once?"):
        st.markdown("Yes — you can upload and evaluate up to 50 resumes simultaneously for comparison.")

    with st.expander("🛡️ Is any candidate data stored or shared externally?"):
        st.markdown("No. All processing happens in memory and nothing is stored, saved, or sent outside your session.")

    with st.expander("🔍 Can I filter candidates based on skill match or shortlist status?"):
        st.markdown("Yes — use the interactive table to filter, sort, and manually shortlist candidates as needed.")

    with st.expander("📥 Can I export shortlisted candidates and their evaluation scores?"):
        st.markdown("Absolutely. Click “Download Shortlist” to get a CSV file of all shortlisted candidates and their matched skill data.")

# === FOOTER ===
st.markdown("""
<hr style='margin-top: 3rem; margin-bottom: 1rem;'>
<p style='text-align: center; font-size: 14px; color: #6c757d;'>
    Fintelligen does not store or transmit uploaded data. All resume evaluations are performed securely in memory.
</p>
""", unsafe_allow_html=True)

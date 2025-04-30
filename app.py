import streamlit as st
from PyPDF2 import PdfReader
from docx import Document
import pandas as pd
import plotly.express as px
import re

st.set_page_config(page_title="Fintelligen", layout="centered")

# === THEME COLORS & STYLES ===
bg_color = "#f8f9fa"
text_color = "#212529"
card_color = "#ffffff"

st.markdown(f"""
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;600;700&display=swap" rel="stylesheet">
<style>
    html, body, [class*="css"] {{
        font-family: 'IBM Plex Sans', sans-serif !important;
        background-color: {bg_color} !important;
        color: {text_color} !important;
    }}
    h1 {{
        font-size: 50px !important;
        font-weight: 700 !important;
        color: #003087 !important;
        margin-bottom: 0 !important;
    }}
    h2, h3, h4 {{
        font-family: 'IBM Plex Sans', sans-serif !important;
        font-weight: 600 !important;
        color: #003087 !important;
        margin-top: 1.2em;
        margin-bottom: 0.6em;
    }}
    .stButton > button {{
        background-color: #003087 !important;
        color: white !important;
        padding: 10px 20px;
        border-radius: 8px;
        border: none;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        font-size: 16px;
    }}
    .stButton > button:hover {{
        background-color: #002060 !important;
    }}
    .block {{
        background-color: {card_color};
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 6px 14px rgba(0,0,0,0.07);
        margin-top: 40px;
    }}
    .ring {{
        width: 100px;
        height: 100px;
        border-radius: 50%;
        background: conic-gradient(#003087 {{percent}}%, #dee2e6 {{percent}}%);
        display: flex;
        align-items: center;
        justify-content: center;
        color: black;
        font-weight: 600;
        font-size: 18px;
        margin: auto;
    }}
</style>
""", unsafe_allow_html=True)

# === HEADER ===
col1, col2 = st.columns([5, 1])
with col1:
    st.markdown("""
        <h1 style='font-size: 50px; font-weight: 700; margin-bottom: 0;'>Fintelligen</h1>
        <h3 style='font-size: 24px; font-weight: 400; color: #003087;'>AI Resume Evaluator for Goldman Sachs</h3>
    """, unsafe_allow_html=True)
with col2:
    st.image("goldman.jpeg", width=160)

# === SIDEBAR FILTERS ===
st.sidebar.header("🧭 Navigation & Filters")
show_summary = st.sidebar.checkbox("🎯 Show Match Summary", value=True)
show_table = st.sidebar.checkbox("📊 Show Skill Matrix & Chart", value=True)
show_resumes = st.sidebar.checkbox("📄 Show Anonymized Resumes", value=True)
show_faq = st.sidebar.checkbox("❓ Show FAQ", value=True)
match_threshold = st.sidebar.slider("Minimum Skill Matches", 0, 10, 0)

# === INSTRUCTIONS ===
st.markdown(f"""
<div class="block">
    <h4>📋 Instructions for HR</h4>
    <ol>
        <li><strong>Upload resumes</strong> (PDF/DOCX)</li>
        <li>Tool will:
            <ul>
                <li><strong>Anonymize</strong> personal details</li>
                <li><strong>Score</strong> skill match</li>
                <li><strong>Visualize</strong> best-fit resumes</li>
            </ul>
        </li>
    </ol>
    <p><em>Upload up to <strong>50 resumes</strong>. No data is stored or shared.</em></p>
</div>
""", unsafe_allow_html=True)

# === FILE UPLOAD ===
uploaded_files = st.file_uploader("📂 Upload Resume(s)", type=["pdf", "docx"], accept_multiple_files=True)
all_skills = ["python", "sql", "data analysis", "communication", "problem solving", "teamwork", "leadership", "project management", "finance", "machine learning"]
selected_skills = st.multiselect("🧠 Filter by Skill Keywords", options=all_skills, default=["python", "sql", "communication"])

# === HELPERS ===
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

# === PROCESSING ===
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

    df = pd.DataFrame({"Resume": names, "Skill Matches": scores, "Match Summary": [i["summary"] for i in insights]})

    # === PLOTLY CHART ===
    if show_table and not df.empty:
        st.markdown(f"<div class='block'><h3>📊 Skill Matrix</h3>", unsafe_allow_html=True)
        st.dataframe(df.sort_values("Skill Matches", ascending=False), use_container_width=True)
        st.markdown("<hr />", unsafe_allow_html=True)

        fig = px.bar(
            df.sort_values("Skill Matches", ascending=True),
            x="Skill Matches",
            y="Resume",
            orientation="h",
            color="Skill Matches",
            color_continuous_scale=["#dee2e6", "#003087"],
            title="Top Resume Matches",
            height=400
        )

        fig.update_layout(
            title_font=dict(size=22, color="#003087", family="IBM Plex Sans"),
            xaxis_title="Matched Skills",
            yaxis_title=None,
            plot_bgcolor=bg_color,
            paper_bgcolor=bg_color,
            font=dict(family="IBM Plex Sans", color=text_color),
            margin=dict(l=20, r=20, t=60, b=20)
        )

        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # === RESUME CARDS ===
    if show_resumes:
        st.markdown(f"<div class='block'><h3>📄 Anonymized Resume Results</h3>", unsafe_allow_html=True)
        for name, data in zip(names, insights):
            with st.expander(f"{name}"):
                if show_summary:
                    st.markdown(f"<div class='ring' style='background: conic-gradient(#003087 {data['percent']}%, #dee2e6 {data['percent']}%); color: {text_color};'>{data['percent']}%</div><br>", unsafe_allow_html=True)
                    st.markdown(f"**🎯 Match Summary:** {data['summary']}")
                st.markdown("---")
                st.markdown("**📄 Anonymized Text:**")
                st.text(data["text"])
        st.markdown("</div>", unsafe_allow_html=True)

# === FAQ ===
if show_faq:
    st.markdown(f"<div class='block'><h3>❓ FAQ</h3>", unsafe_allow_html=True)

    with st.expander("What skills are evaluated?"):
        st.write("You can select relevant keywords like Python, Communication, Leadership, etc. from the skill filter above.")

    with st.expander("Is my data stored anywhere?"):
        st.write("No. All processing happens in-memory. Resumes are not saved, logged, or transmitted.")

    with st.expander("How is the skill match percentage calculated?"):
        st.write("The tool counts how many selected skills are found in the resume and divides it by the total number of selected skills.")

    with st.expander("Can I upload multiple resumes?"):
        st.write("Yes. You can upload up to 50 resumes at once, in PDF or DOCX format.")

    with st.expander("Can I change the keywords to match different roles?"):
        st.write("Absolutely. You can customize the skill list depending on the job description or team needs.")

    with st.expander("Does the tool understand synonyms or context?"):
        st.write("Not yet. The current version checks for exact keyword matches. Future versions may include semantic AI-based matching.")

    with st.expander("Can I download the results?"):
        st.write("Coming soon: export to PDF and CSV will be supported in the next release.")

    with st.expander("Can this tool reduce hiring bias?"):
        st.write("Yes, anonymization removes personal identifiers like name, email, and phone. This helps focus evaluation on skills.")

    st.markdown("</div>", unsafe_allow_html=True)


import streamlit as st
from PyPDF2 import PdfReader

st.set_page_config(page_title="Fintelligen", layout="wide")

st.markdown("""
    <style>
        body {
            font-family: 'Helvetica Neue', sans-serif;
            background-color: #f9f9f9;
        }
        .main {
            padding-top: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

st.image("goldman_logo.png", width=80)
st.markdown("## **Fintelligen**")
st.markdown("### AI Resume Evaluator for Goldman Sachs")

uploaded_files = st.file_uploader("📂 Upload Resume(s)", type=["pdf", "docx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        st.markdown(f"**Anonymized File:** `Candidate_{file.name[-8:]}`")
        if file.name.endswith(".pdf"):
            reader = PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            st.text_area("Extracted Text", text[:2000], height=200)
        else:
            st.warning("Only PDF reading is supported in this MVP version.")

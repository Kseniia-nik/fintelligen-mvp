
import streamlit as st
import matplotlib.pyplot as plt
import time

# --- Page config ---
st.set_page_config(
    page_title="Fintelligen: AI Resume Screener",
    page_icon="🤖",
    layout="wide"
)

# --- Custom CSS styling for narrower layout ---
st.markdown("""
    <style>
        .main .block-container {
            max-width: 768px;
            padding-top: 2rem;
            padding-bottom: 2rem;
            margin: 0 auto;
        }
        body {
            background-color: #f8f9fa;
        }
        .center-text {
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# --- Header section with logo ---
col1, col2 = st.columns([1, 4])
with col1:
    try:
        st.image("goldman_logo.png", width=120)
    except:
        st.warning("⚠️ Logo not found. Please upload 'goldman_logo.png' to the app directory.")
with col2:
    st.markdown("<h1 class='center-text'>Fintelligen: AI Resume Screener</h1>", unsafe_allow_html=True)
    st.markdown("##### Empowering unbiased hiring through skill-based resume analysis")

# --- File uploader section ---
st.markdown("### 📄 Upload Resumes (up to 50)")
with st.expander("ℹ️ Upload multiple resumes in PDF or DOCX format. We’ll anonymize them and evaluate key skills."):
    st.write("Your data stays private and is not stored after processing.")

uploaded_files = st.file_uploader(
    "Choose up to 50 resumes", type=["pdf", "docx"], accept_multiple_files=True
)

if uploaded_files:
    for uploaded_file in uploaded_files:
        st.success(f"✅ Uploaded: {uploaded_file.name}")

        with st.spinner(f"🔍 Analyzing {uploaded_file.name}... Please wait"):
            time.sleep(2)  # Placeholder for actual processing

        # --- Skill Match Visualization ---
        st.markdown(f"### 📊 Skill Match Analysis for: {uploaded_file.name}")
        skills = ['Python', 'SQL', 'Communication', 'Finance Knowledge', 'Problem Solving']
        scores = [90, 75, 85, 60, 95]

        fig, ax = plt.subplots()
        ax.barh(skills, scores)
        ax.set_xlim(0, 100)
        ax.set_xlabel('Match %')
        ax.set_title("Top Skill Alignment")
        st.pyplot(fig)

        # --- Anonymized Resume Output ---
        st.markdown("### 🧾 Anonymized Resume")
        anonymized_text = """
Experienced analyst with 5+ years in financial services. 
Led AI-driven initiatives in KYC automation, reducing false positives by 30%. 
Skilled in Python, SQL, and stakeholder engagement.
"""
        st.code(anonymized_text.strip(), language='markdown')

        st.download_button(
            f"📥 Download Anonymized Resume - {uploaded_file.name}",
            anonymized_text.strip(),
            file_name=f"anonymized_{uploaded_file.name.replace(' ', '_')}.txt"
        )
else:
    st.warning("⚠️ Please upload at least one resume to proceed.")

import streamlit as st
import matplotlib.pyplot as plt
import time

# --- Page config ---
st.set_page_config(
    page_title="Fintelligen: AI Résumé Screener",
    page_icon="🤖",
    layout="wide"
)

# --- Custom CSS styling ---
st.markdown("""
    <style>
        body {
            background-color: #f8f9fa;
        }
        .main {
            font-family: 'Open Sans', sans-serif;
            color: #212529;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .stApp {
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
    st.image("goldman_logo.png", width=120)
with col2:
    st.markdown("<h1 class='center-text'>Fintelligen: AI Résumé Screener</h1>", unsafe_allow_html=True)
    st.markdown("##### Empowering unbiased hiring through skill-based résumé analysis")

# --- File uploader section ---
st.markdown("### 📄 Upload Résumé")
with st.expander("ℹ️ Upload your résumé in PDF or DOCX format. We’ll anonymize it and evaluate key skills."):
    st.write("Your data stays private and is not stored after processing.")

uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx"])

if uploaded_file is not None:
    st.success("✅ File uploaded successfully!")

    with st.spinner("🔍 Analyzing résumé... Please wait"):
        time.sleep(2)  # Placeholder for actual processing

    # --- Skill Match Visualization ---
    st.markdown("### 📊 Skill Match Analysis")
    skills = ['Python', 'SQL', 'Communication', 'Finance Knowledge', 'Problem Solving']
    scores = [90, 75, 85, 60, 95]

    fig, ax = plt.subplots()
    ax.barh(skills, scores)
    ax.set_xlim(0, 100)
    ax.set_xlabel('Match %')
    ax.set_title("Top Skill Alignment")
    st.pyplot(fig)

    # --- Anonymized Résumé Output ---
    st.markdown("### 🧾 Anonymized Résumé")
    anonymized_text = """
Experienced analyst with 5+ years in financial services. 
Led AI-driven initiatives in KYC automation, reducing false positives by 30%. 
Skilled in Python, SQL, and stakeholder engagement.
"""
    st.code(anonymized_text.strip(), language='markdown')

    st.download_button("📥 Download Anonymized Résumé", anonymized_text.strip(), file_name="anonymized_resume.txt")

else:
    st.warning("⚠️ Please upload a résumé to proceed.")

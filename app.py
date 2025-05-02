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

# === PAGE CONFIG ===
st.set_page_config(page_title="Fintelligen", layout="centered")

# === GLOBAL STYLE ===
st.markdown(f"""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
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
      margin-bottom: 0.1em !important;
  }}
  h2, h3, h4 {{
      font-weight: 600 !important;
      color: {accent_color} !important;
      margin-top: 0 !important;
      margin-bottom: 0.1em !important;
      line-height: 1.2em !important;
  }}

  .block {{
      background-color: {card_color};
      padding: 20px 25px;
      border-radius: 15px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.05);
      margin-bottom: 1.5rem;
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
</style>
""", unsafe_allow_html=True)

# === SIDEBAR ===
with st.sidebar:
    st.header("📁 Navigation")
    st.markdown("- Upload Resume")
    st.markdown("- Shortlist & Download")
    st.markdown("- Settings")

# === HEADER ===
col1, col2 = st.columns([0.85, 0.15])
with col1:
    st.markdown("<h1>Fintelligen</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color:{highlight_color}; margin-top: -0.5rem;'>AI Resume Evaluator for Goldman Sachs</h3>", unsafe_allow_html=True)
with col2:
    st.image("FINTELLIGEN.svg", width=80)

# === INSTRUCTIONS ===
with st.container():
    st.markdown("### 📋 Instructions", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="block">
            <h4>🧾 How to Use</h4>
            <p>This tool evaluates uploaded resumes against the core competencies required for analyst-level roles at <strong>Goldman Sachs</strong>.</p>
            <ol>
                <li><strong>Upload resumes</strong> (PDF/DOCX)</li>
                <li>The tool will extract content, compare it to target skills, and show match scores</li>
                <li>Use the results to shortlist top candidates</li>
            </ol>
        </div>
        """, unsafe_allow_html=True
    )

# === PLACEHOLDER: Skill Matrix Section ===
with st.container():
    st.markdown("### 📊 Skill Matrix", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="block">
            <p><em>Goldman Sachs core skillset is applied automatically:</em></p>
            <ul>
                <li>Financial analysis</li>
                <li>Excel / PowerPoint proficiency</li>
                <li>Data interpretation</li>
                <li>Communication & teamwork</li>
            </ul>
            <!-- Add actual matrix/table here -->
        </div>
        """, unsafe_allow_html=True
    )

# === PLACEHOLDER: Resume Evaluation Table ===
with st.container():
    st.markdown("### 📄 Resume Evaluation Table", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="block">
            <!-- Add actual DataFrame here -->
            <p>Table with all uploaded resumes and skill match scores will appear here.</p>
        </div>
        """, unsafe_allow_html=True
    )
    col_clear, col_download = st.columns([0.5, 0.5])
    with col_clear:
        st.button("🗑 Clear Shortlist")
    with col_download:
        st.download_button("⬇️ Download CSV", data="", file_name="shortlist.csv", disabled=True)

# === PLACEHOLDER: Anonymized Resume Viewer ===
with st.expander("📄 Anonymized Resume Results"):
    st.markdown("Here you will see anonymized text extracted from each resume.")
# === FAQ SECTION ===
with st.expander("❓ Frequently Asked Questions"):
    st.markdown(
        f"""
        <div class="block">
            <h4>What formats are supported?</h4>
            <p>You can upload resumes in PDF or DOCX format. The system automatically parses them for skill comparison.</p>

            <h4>How are skill matches calculated?</h4>
            <p>We use keyword matching and context-aware AI models to compare resume content to the Goldman Sachs core competencies.</p>

            <h4>Can I export the results?</h4>
            <p>Yes. After evaluation, you can download a CSV file with candidate names and their skill match scores.</p>

            <h4>Is the data stored?</h4>
            <p>No. All data is processed in-memory only. Nothing is stored on the server.</p>
        </div>
        """, unsafe_allow_html=True
    )

import streamlit as st
import base64
import os

st.set_page_config(
    page_title="Fintelligen – AI Resume Evaluator",
    layout="wide",
    initial_sidebar_state="auto"
)

# 💼 Кастомный стиль
st.markdown("""
    <style>
    body {
        background-color: #f8f9fa;
        font-family: 'Open Sans', sans-serif;
        color: #212529;
    }
    .big-title {
        text-align: center;
        font-size: 3em;
        font-weight: 800;
        margin-bottom: 0.1em;
        color: #0d1a26;
    }
    .subtitle {
        text-align: center;
        font-size: 1.3em;
        margin-bottom: 1.5em;
        color: #495057;
    }
    .instruction-box {
        background-color: #e9f2ff;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 2rem;
    }
    .card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 2rem;
    }
    .goldman-logo {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 120px;
        padding-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 🏦 Логотип
if os.path.exists("Goldman-Sachs.png"):
    with open("Goldman-Sachs.png", "rb") as f:
        image_data = f.read()
        encoded = base64.b64encode(image_data).decode()
        st.markdown(f"<img class='goldman-logo' src='data:image/png;base64,{encoded}'>", unsafe_allow_html=True)

# Заголовки
st.markdown("<div class='big-title'>Fintelligen</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>AI Resume Evaluator for Goldman Sachs</div>", unsafe_allow_html=True)

# 📋 Инструкции
with st.container():
    st.markdown("<div class='instruction-box'><h5>📋 Instructions for HR</h5><ul><li>Upload up to 50 resumes (.pdf or .docx)</li><li>Review anonymized previews</li><li>Filter by skill or role</li><li>See matching score and skill breakdown</li><li>Download matched resumes if needed</li></ul></div>", unsafe_allow_html=True)

# 🗂️ Загрузка файлов
uploaded_files = st.file_uploader("📎 Drag and drop or select resumes", type=["pdf", "docx"], accept_multiple_files=True)

# 👉 Здесь будут обработка, анонимизация, фильтрация, визуализация скиллов и отображение барчартов
# Добавьте свои функции обработки ниже...

# Пример вывода:
if uploaded_files:
    st.markdown("<div class='card'><b>🧾 Resume Previews (Anonymized)</b><br><i>Coming soon: skill analysis + smart matching</i></div>", unsafe_allow_html=True)

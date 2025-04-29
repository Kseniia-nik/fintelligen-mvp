# Fintelligen MVP – Resume Anonymizer and Skill Evaluator

This is a simple and functional Streamlit app designed as an MVP for automating the evaluation of resumes for graduate roles at Goldman Sachs Australia.

## 💼 Key Features

- 📄 Upload a resume (PDF)
- 🧼 Automatically anonymize personal information (e.g., name, email, phone, location)
- 🎯 Match the resume against mandatory and optional skill lists
- 📊 Display a skill-based score based on the number of relevant matches
- 📥 Download a summary table as a CSV file

---

## 🧠 Skill Evaluation Criteria

The app evaluates resumes based on two categories of skills:

### Mandatory Skills
- financial analysis
- excel
- data analysis
- problem solving
- communication
- teamwork
- attention to detail
- critical thinking
- python
- valuation

### Optional Skills
- SQL
- powerpoint
- financial modeling
- presentation skills
- project management
- statistics
- machine learning
- risk management
- corporate finance
- investment banking knowledge

---

## 🚀 How to Run Locally

1. Clone this repository:

   ```bash
   git clone https://github.com/YOUR_USERNAME/fintelligen-mvp.git
   cd fintelligen-mvp


2. Install dependencies:

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

3. Run the app:

```bash
streamlit run app.py
```

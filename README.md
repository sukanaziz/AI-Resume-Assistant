# 🤖 AI Resume Assistant

An AI-powered web app that analyzes resumes against job descriptions and generates tailored cover letters using Anthropic's Claude AI.

## Features
- Resume analysis with match score out of 100
- Identifies strengths and weaknesses
- Suggests specific bullet point rewrites
- Generates tailored cover letters
- Download results as PDF

## Tech Stack
- Python
- Streamlit
- Anthropic Claude API
- PyPDF2 & python-docx
- FPDF2

## How to Run
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Add your Anthropic API key to a `.env` file: `ANTHROPIC_API_KEY=your-key`
4. Run: `streamlit run app.py`

## Demo
Upload your resume and a job description to get instant AI feedback and a personalized cover letter.
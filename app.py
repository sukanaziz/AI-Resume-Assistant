import os #Python connects with OS
import anthropic #Anthopics AI library 
import PyPDF2 #Open and read pdf files 
import docx #Open and read docx files 
from fpdf import FPDF #Create and share pdf files
import streamlit as st #Streamlit for webs UI 
from dotenv import load_dotenv 

# Load the API key from env file
load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def extract_text_from_pdf(file):
    #Python reads the pdf file
    reader = PyPDF2.PdfReader(file)
    #Empty String to hold text
    text = ""
    #Add all text from pdf in text
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(file):
    #Python reads the docx file
    doc = docx.Document(file)
    #Empty string to hold all text
    text = ""
    #adds all text from docx in text
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def analyze_resume(resume_text, job_description):
    #Send a message to the AI
    response = client.messages.create(
        #ANTHROPICS AI Model
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system="You are an expert career coach and resume reviewer. Use only plain text in your response — no emojis, no arrows, no special symbols. Use dashes (-) for bullet points instead.",
        messages=[
            
            {
                "role": "user",
                "content": f"""Here is the candidate's resume:
{resume_text}

Here is the job description they are applying for:
{job_description}

Please provide:
1. A match score out of 100
2. Top 3 strengths of this resume for this role
3. Top 3 gaps or weaknesses
4. 3 specific bullet point rewrites to better match the job
5. A one paragraph overall recommendation

Be specific, honest, and actionable."""
            }
        ]
    )
    return response.content[0].text

#Prompt instructions for cover letter generation
def generate_cover_letter(resume_text, job_description):
    #Send a message to the AI
    response = client.messages.create(
        #ANTHROPICS AI MODEL
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system="You are an expert cover letter writer. Use only plain text in your response — no emojis, no arrows, no special symbols.",
        messages=[
            {
                "role": "user",
                "content": f"""Here is the candidate's resume:
{resume_text}

Here is the job description they are applying for:
{job_description}

- Is 3-4 paragraphs and between 250-400 words
- Strategically incorporates keywords from the job description
- Opens with a strong hook
- Highlights the most relevant experience and skills for this specific role
- Closes with enthusiasm and a call to action
- Sounds natural and human, not robotic"""

            }
        ]
    )
    return response.content[0].text

#Creates a pdf file of results
def create_pdf(text):
    # Remove characters that PDF font can't handle
    text = text.encode('latin-1', errors='replace').decode('latin-1')
    #Create pdf
    pdf = FPDF()
    #Add the page
    pdf.add_page()
    #Set Font
    pdf.set_font("Arial", size=12)
    #Write text into pdf. width=0 height=10
    pdf.multi_cell(0, 10, text)

    return bytes(pdf.output())


# Page config
st.set_page_config(
    page_title="AI Resume Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    /* Force dark mode */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e) !important;
    }
    * {
        color: white !important;
    }
    input, textarea {
        color: white !important;
        background: rgba(255, 255, 255, 0.07) !important;
    }
            
    /* Background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: white;
    }
    
    /* Title */
    h1 {
        text-align: center;
        font-size: 3em !important;
        background: linear-gradient(90deg, #00c6ff, #0072ff, #9b59b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 10px 0;
    }

    /* Subtitle */
    .subtitle {
        text-align: center;
        color: #a0a8c0;
        font-size: 1.1em;
        margin-bottom: 20px;
    }

    /* Cards */
    .card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        backdrop-filter: blur(10px);
        margin-bottom: 16px;
    }
            
    /* Result box */
    .result-box {
        background: rgba(255, 255, 255, 0.05);
        border-left: 5px solid #00c6ff;
        border-radius: 12px;
        padding: 24px;
        margin-top: 20px;
        color: white;
        line-height: 1.8;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.03);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Divider */
    hr {
        border-color: rgba(255, 255, 255, 0.1);
    }

    /* Text inputs */
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.07) !important;
        color: white !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
    }

    /* File uploader */
    [data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 10px;
        border: 1px dashed rgba(255, 255, 255, 0.2);
    }
    </style>
""", unsafe_allow_html=True)
#Header
st.title("🤖 AI Resume Assistant")
st.markdown('<p class="subtitle">Land your dream job with AI-powered resume analysis and cover letter generation ✨</p>', unsafe_allow_html=True)
st.divider()

# Create sidebar for assistance
with st.sidebar:
    st.header("📋 How to use")
    st.markdown("""
    1. 📄 Upload your resume (PDF or DOCX)
    2. 📝 Paste the job description
    3. 🔍 Click **Analyze My Resume** for feedback
    4. ✉️ Click **Generate Cover Letter** for a tailored cover letter
    """)
    st.divider()
    st.markdown("Built with Python & AI 🚀")

# Layout of main screen
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📄 Upload Your Resume")
    st.markdown("<div style='margin-top: 28px'>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose a PDF or DOCX file", type=["pdf", "docx"])
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.subheader("📝 Job Description")
    job_description = st.text_area("Paste the job description here", height=400)

st.divider()

#Align buttons
col3, col4, col5= st.columns([2, 1, 1])

with col3:
    analyze_button = st.button("🔍 Analyze My Resume")

with col5:
    cover_letter_button = st.button("✉️ Generate Cover Letter")

#Analyze logic
if analyze_button:
    #If not an uploaded file and job description print error
    if not uploaded_file or not job_description:
        st.warning("⚠️ Please upload a resume and paste a job description!")
    else:
        #Spinning animation
        with st.spinner("Analyzing your resume..."):
            if uploaded_file.name.endswith(".pdf"):
                resume_text = extract_text_from_pdf(uploaded_file)
            else:
                resume_text = extract_text_from_docx(uploaded_file)
            
            result = analyze_resume(resume_text, job_description)
            #Success Message
            st.success("✅ Analysis Complete!")
            #Print results and organizes text
            st.markdown(f'<div class="result-box">{result}</div>', unsafe_allow_html=True)

        pdf_data = create_pdf(result)
        st.download_button(
            label="📥 Download Analysis as PDF",
            data=pdf_data,
            file_name="resume_analysis.pdf",
            mime="application/pdf"
        )

# Cover letter logic 
if cover_letter_button:
    #If not an uploaded file and job description print error
    if not uploaded_file or not job_description:
        st.warning("⚠️ Please upload a resume and paste a job description!")
    else:
        #Spinning animation
        with st.spinner("Generating cover letter..."):
            if uploaded_file.name.endswith(".pdf"):
                resume_text = extract_text_from_pdf(uploaded_file)
            else:
                resume_text = extract_text_from_docx(uploaded_file)
            
            cover_letter = generate_cover_letter(resume_text, job_description)
            #Success Message
            st.success("✅ Cover Letter Generated!")
            #Print results and organizes text
            st.markdown(f'<div class="result-box">{cover_letter}</div>', unsafe_allow_html=True)
        
        #Align buttons
        col6, col7, col8= st.columns([2, 1, 1])
        with col6:
            pdf_data = create_pdf(cover_letter)
            st.download_button(
                label="📥 Download Cover Letter as PDF",
                data=pdf_data,
                file_name="cover_letter.pdf",
                mime="application/pdf"
            )
        with col8:
            st.button("📋 Copy to Clipboard", 
                on_click=lambda: st.write(
                    f'<script>navigator.clipboard.writeText(`{cover_letter}`)</script>', 
                    unsafe_allow_html=True
                )
            )
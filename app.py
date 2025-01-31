import streamlit as st
from resume_parser import extract_text
from job_matcher import analyze_resume_with_job
from compatibility import calculate_compatibility

# --------- PAGE CONFIGURATION ---------
st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")

# --------- CUSTOM STYLING ---------
st.markdown("""
    <style>
    body {
        background-color: #f5f5f5;
        font-family: 'Arial', sans-serif;
    }
    .title {
        color: #007bff;
        text-align: center;
        font-size: 36px;
        font-weight: bold;
    }
    .subtitle {
        color: #555;
        text-align: center;
        font-size: 20px;
        margin-bottom: 30px;
    }
    .stButton>button {
        background-color: #007bff;
        color: white;
        padding: 10px 20px;
        border-radius: 8px;
        font-size: 18px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #0056b3;
    }
    </style>
""", unsafe_allow_html=True)

# --------- HEADER ---------
st.markdown("<h1 class='title'>📄 AI Resume Compatibility Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Upload your resume and compare it with a job description!</p>", unsafe_allow_html=True)

# --------- LAYOUT SETUP ---------
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Upload Your Resume")
    resume_file = st.file_uploader("Choose a PDF or DOCX file", type=["pdf", "docx"])
    
    industry_options = [
        "ACCOUNTANT", "ADVOCATE", "AGRICULTURE", "APPAREL", "ARTS",
        "AUTOMOBILE", "AVIATION", "BANKING", "BPO", "BUSINESS-DEVELOPMENT",
        "CHEF", "CONSTRUCTION", "CONSULTANT", "DESIGNER", "DIGITAL-MEDIA",
        "ENGINEERING", "FINANCE", "FITNESS", "HEALTHCARE", "HR",
        "INFORMATION-TECHNOLOGY", "PUBLIC-RELATIONS", "SALES", "TEACHER"
    ]
    
    industry = st.selectbox("Select Industry", industry_options)

with col2:
    st.subheader("Paste the Job Description")
    job_description = st.text_area("Enter job details here...", height=200)

# --------- PROCESSING BUTTON ---------
if st.button("🔍 Analyze Resume"):
    if resume_file and job_description and industry:
        with st.spinner("Extracting text from resume..."):
            resume_text = extract_text(resume_file)

        if resume_text:
            with st.spinner("⏳ Analyzing your resume and job posting..."):
                analysis = analyze_resume_with_job(resume_text, job_description, industry)
            
            st.success("✅ Analysis Complete!")
            st.write("### AI-Powered Resume Analysis 🔍")
            st.write(analysis)
        else:
            st.error("❌ Could not extract text from the resume. Please upload a valid file.")
    else:
        st.warning("⚠️ Please upload a resume, enter a job description, and select an industry.")

import os
import logging
from functools import lru_cache
from mistralai import Mistral
from dotenv import load_dotenv
from resume_matcher import find_similar_resume

# Load API key
load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")

if not api_key:
    raise ValueError("❌ MISTRAL_API_KEY is missing. Make sure it's set.")

# Initialize Mistral client
client = Mistral(api_key=api_key)
model = "mistral-medium"  # Available: mistral-tiny, mistral-small, mistral-medium

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

@lru_cache(maxsize=10)  # Cache up to 10 previous results for faster reprocessing
def analyze_resume_with_job(resume_text, job_text,industry):
    """
    Optimized function to analyze resume-job compatibility using Mistral AI.
    Returns a compatibility score and improvement suggestions.
    """

    try:
        logging.info("🔍 Processing resume analysis...")

        # Trim input text to optimize response time
        resume_text = resume_text[:1200]
        job_text = job_text[:1200]

        similar_resume = find_similar_resume(resume_text, industry)

        # Construct the request prompt
        prompt = f"""
        Analyze the following resume for compatibility with this job.
        Identify missing skills and suggest improvements.

        Resume:
        {resume_text[:1500]}  # Trim text to fit model limits

        Job Description:
        {job_text[:1500]}

        High-Quality Example Resume from {industry}:
        {similar_resume[:1500] if similar_resume else "No example available"}

        Provide **a detailed response (at least 300 words)** covering:
        1. A **detailed** compatibility score (0-100%) with an explanation.
        - Explain why this score was given (e.g., matching skills, formatting, experience level, keyword match, etc.).
        - If applicable, mention any ATS (Applicant Tracking System) concerns.

        2. **Missing skills:**
        - Identify **specific** missing skills.
        - Suggest **resources** such as online courses, certifications, or practical exercises to gain these skills.
        - Provide **links** to well-known platforms like Coursera, Udemy, or official certifications.

        3. **Areas for improvement:**
        - Analyze **formatting issues** (e.g., inconsistent font sizes, alignment, bullet points usage).
        - Identify **spelling or grammatical errors**.
        - Evaluate if sentences follow a structured, concise, and **impactful** approach.

        4. **Suggested resume edits:**
        - Determine if this resume is **likely to pass an ATS screening**.
        - Recommend **structural changes** to improve readability and keyword optimization.
        - Emphasize that **skills should not be fabricated**; instead, suggest gaining foundational knowledge before listing skills.
        """

        chat_response = client.chat.complete(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=800,
        temperature=0.5,
        top_p=0.9,
        stop=None
)

        response_text = chat_response.choices[0].message.content
        logging.info("✅ Successfully generated resume analysis.")
        return response_text

    except Exception as e:
        logging.error(f"❌ Error processing resume: {str(e)}")
        return "⚠️ An error occurred. Please try again."

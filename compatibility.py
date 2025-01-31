import re

def calculate_compatibility(resume_text, job_text):
    """
    Computes a compatibility score based on keyword matches.
    """
    resume_words = set(re.findall(r'\w+', resume_text.lower()))
    job_words = set(re.findall(r'\w+', job_text.lower()))

    common_words = resume_words & job_words
    score = len(common_words) / len(job_words) * 100

    return round(score, 2)

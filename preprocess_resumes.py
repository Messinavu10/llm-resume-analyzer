import os
import pdfplumber
import json

# Path to your dataset
DATASET_PATH = "/Users/naveenkumar/Desktop/ResumeReviewer/data"

# Function to extract text from PDFs
def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file while preserving formatting."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            extracted_text = []
            for page in pdf.pages:
                text = page.extract_text(layout=True)  # Keep formatting
                if text:
                    extracted_text.append(text)
            return "\n".join(extracted_text)
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return None

# Dictionary to store extracted resume data
resume_data = {}

# Iterate through each industry folder
for industry in os.listdir(DATASET_PATH):
    industry_path = os.path.join(DATASET_PATH, industry)
    
    if os.path.isdir(industry_path):  # Ensure it's a folder
        print(f"Processing industry: {industry}")
        resume_data[industry] = []

        # Iterate through each resume file in the folder
        for file in os.listdir(industry_path):
            if file.endswith(".pdf"):  # Process only PDFs
                pdf_path = os.path.join(industry_path, file)
                resume_text = extract_text_from_pdf(pdf_path)

                if resume_text:
                    resume_data[industry].append({
                        "filename": file,
                        "text": resume_text
                    })

# Save extracted data to JSON
with open("resume_database.json", "w", encoding="utf-8") as json_file:
    json.dump(resume_data, json_file, indent=4)

print("Resume dataset successfully created and saved to resume_database.json")

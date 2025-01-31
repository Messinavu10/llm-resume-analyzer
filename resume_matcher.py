import json
import numpy as np

# Load extracted resume data
with open("resume_database.json", "r", encoding="utf-8") as json_file:
    resume_data = json.load(json_file)

# Function to find the most similar resume in a given industry
def find_similar_resume(user_resume_text, industry):
    """Find the most similar high-quality resume in the specified industry."""
    
    if industry not in resume_data:
        return None  # No data for this industry

    industry_resumes = resume_data[industry]
    
    # Simple similarity based on common words (can be replaced with embeddings)
    def text_similarity(text1, text2):
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        return len(words1 & words2) / len(words1 | words2)  # Jaccard similarity
    
    # Find the most similar resume
    similarities = [text_similarity(user_resume_text, r["text"]) for r in industry_resumes]
    best_match_index = np.argmax(similarities)

    return industry_resumes[best_match_index]["text"]

# Test function
if __name__ == "__main__":
    user_resume_sample = "Sample resume text here..."
    industry_sample = "ENGINEERING"

    similar_resume = find_similar_resume(user_resume_sample, industry_sample)
    if similar_resume:
        print(f"✅ Found a high-quality resume match in {industry_sample}")
        print(similar_resume[:500])  # Print the first 500 characters for preview
    else:
        print(f"No matching resumes found for {industry_sample}")

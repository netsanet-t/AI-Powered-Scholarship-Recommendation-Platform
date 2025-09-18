import pdfplumber
import spacy
import re

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text

def extract_skills(doc, skills):
    skill_tokens = {tuple(skill.lower().split()): skill for skill in skills}
    found_skills = set()
    
    # Lowercase all input tokens for case-insensitive comparison
    tokens = [token.text.lower() for token in doc]

    # Iterate through tokens using a sliding window
    for i in range(len(tokens)):
        for length in range(1, 5):  # Handle 2+ word majors
            phrase = tuple(tokens[i:i+length])
            if phrase in skill_tokens:
                found_skills.add(skill_tokens[phrase])
    
    return list(found_skills)

def extract_dob(cv_text):
    dob_match = re.search(r"(?:date of birth|dob)[\s:]*([\d]{1,2}[-/.\s]?\d{1,2}[-/.\s]?\d{2,4})", cv_text, re.I)
    if dob_match:
        return dob_match.group(1)  # Return the matched DOB
    return None

def extract_gpa(cv_text):
    gpa_match = re.search(r'(\d\.\d{1,2})\s*/\s*4\.0', cv_text)
    if gpa_match:
        return gpa_match.group(1)  # Return the matched GPA
    return None

def extract_university(doc):
    for ent in doc.ents:
        if ent.label_ == "ORG" and ("university" in ent.text.lower() or "college" in ent.text.lower()):
            return ent.text
    return None

def extract_gender(cv_text):
    gender_match = re.search(r'gender[:\s]*(male|female)', cv_text, re.I)
    if gender_match:
        return gender_match.group(1).capitalize()
    return None

def extract_nationality(doc):
    for ent in doc.ents:
        if ent.label_ == "GPE":
            return ent.text
    return None

def extract_graduation_year(cv_text):
    match = re.search(r'graduation\s*(year)?[:\s]*([\d]{4})', cv_text, re.I)
    if match:
        return match.group(2)
    return None

def extract_degree(cv_text):
    match = re.search(r'(bachelor|master|ph\.?d|msc|bsc)', cv_text, re.I)
    if match:
        return match.group(0)
    return None

def extract_major(doc, majors):
    major_tokens = {tuple(major.lower().split()): major for major in majors}
    found_majors = set()
    
    # Lowercase all input tokens for case-insensitive comparison
    tokens = [token.text.lower() for token in doc]

    # Iterate through tokens using a sliding window
    for i in range(len(tokens)):
        for length in range(2, 5):  # Handle 2+ word majors
            phrase = tuple(tokens[i:i+length])
            if phrase in major_tokens:
                found_majors.add(major_tokens[phrase])
    
    return list(found_majors)



if __name__ == "__main__":
    cv = extract_text_from_pdf("file.pdf")
    doc = nlp(cv)

    skills = ["python", "java", "c++", "machine learning", "deep learning", "data science", "nlp", "sql", "aws", "azure", "tensorflow", "keras", "reactjs"]
    majors = ["Computer Science and Engineering", "Information Technology", "Software Engineering", "Data Science", "Artificial Intelligence", "Natural Language Processing"]

    skills_found = extract_skills(doc, skills)
    print(skills_found)

    dob = extract_dob(cv)
    print(dob)

    gpa = extract_gpa(cv)
    print(gpa)

    university = extract_university(doc)
    print(university)

    gender = extract_gender(cv)
    print(gender)

    nationality = extract_nationality(doc)
    print(nationality)

    graduation_year = extract_graduation_year(cv)
    print(graduation_year)

    degree = extract_degree(cv)
    print(degree)

    major = extract_major(doc, majors)
    print(major)

# def extract_skills(doc, skills):
#   skill_tokens = {tuple(skill.lower().split()): skill for skill in skills}
#   found_skills = set()
  
#   # Lowercase all input tokens for case-insensitive comparison
#   tokens = [token.text.lower() for token in doc]

#   # Iterate through tokens using a sliding window
#   for i in range(len(tokens)):
#       for length in range(1, 5):  # Handle 2+ word majors
#           phrase = tuple(tokens[i:i+length])
#           if phrase in skill_tokens:
#               found_skills.add(skill_tokens[phrase])
  
#   return list(found_skills)

# def extract_dob(cv_text):
#     dob_match = re.search(r"(?:date of birth|dob)[\s:]*([\d]{1,2}[-/.\s]?\d{1,2}[-/.\s]?\d{2,4})", cv_text, re.I)
#     if dob_match:
#         return dob_match.group(1)  # Return the matched DOB
#     return None

# def extract_gpa(cv_text):
#     gpa_match = re.search(r'(\d\.\d{1,2})\s*/\s*4\.0', cv_text)
#     if gpa_match:
#         return gpa_match.group(1)  # Return the matched GPA
#     return None

# def extract_university(doc):
#     for ent in doc.ents:
#         if ent.label_ == "ORG" and ("university" in ent.text.lower() or "college" in ent.text.lower()):
#             return ent.text
#     return None

# def extract_gender(cv_text):
#     gender_match = re.search(r'gender[:\s]*(male|female)', cv_text, re.I)
#     if gender_match:
#         return gender_match.group(1).capitalize()
#     return None

# def extract_nationality(doc):
#     for ent in doc.ents:
#         if ent.label_ == "GPE":
#             return ent.text
#     return None

# def extract_graduation_year(cv_text):
#     match = re.search(r'graduation\s*(year)?[:\s]*([\d]{4})', cv_text, re.I)
#     if match:
#         return match.group(2)
#     return None

# def extract_degree(cv_text):
#     match = re.search(r'(bachelor|master|ph\.?d|msc|bsc)', cv_text, re.I)
#     if match:
#         return match.group(0)
#     return None

# def extract_major(doc, majors):
    major_tokens = {tuple(major.lower().split()): major for major in majors}
    found_majors = set()
    
    # Lowercase all input tokens for case-insensitive comparison
    tokens = [token.text.lower() for token in doc]

    # Iterate through tokens using a sliding window
    for i in range(len(tokens)):
        for length in range(2, 5):  # Handle 2+ word majors
            phrase = tuple(tokens[i:i+length])
            if phrase in major_tokens:
                found_majors.add(major_tokens[phrase])
    
    return list(found_majors)
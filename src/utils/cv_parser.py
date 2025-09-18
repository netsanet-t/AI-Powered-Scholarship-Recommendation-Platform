import re
import spacy
import pdfplumber

class CvParser:
    def __init__(self, cv):
        
        self.nlp = spacy.load("en_core_web_sm")
        self.skills = ["python", "java", "c++", "machine learning", "deep learning", "data science", "nlp", "sql", "aws", "azure", "tensorflow", "keras", "reactjs"]
        self.majors = ["Computer Science and Engineering", "Information Technology", "Software Engineering", "Data Science", "Artificial Intelligence", "Natural Language Processing"]
        self.cv_file = cv
        self.cv_text = self.extract_text_from_pdf()
        self.doc = self.nlp(self.cv_text)
        self.result = {
            'skills': [],
            'university': None,
            'degree': None,
            'major': None,
            'graduation_year': None,
            'gpa': None,
            'nationality': None,
            'gender': None,
            'date_of_birth': None
        }

        self.calculate_results()

    def calculate_results(self):
        self.extract_skills()
        self.extract_dob()
        self.extract_gpa()
        self.extract_university()
        self.extract_gender()
        self.extract_nationality()
        self.extract_graduation_year()
        self.extract_degree()
        self.extract_major()

    def get_result(self):
        return self.result
    
    def extract_text_from_pdf(self):
      text = ""
      with pdfplumber.open(self.cv_file) as pdf:
          for page in pdf.pages:
              page_text = page.extract_text()
              if page_text:
                  text += page_text
      return text
    
    def extract_skills(self):
      skill_tokens = {tuple(skill.lower().split()): skill for skill in self.skills}
      found_skills = set()
      
      # Lowercase all input tokens for case-insensitive comparison
      tokens = [token.text.lower() for token in self.doc]

      # Iterate through tokens using a sliding window
      for i in range(len(tokens)):
          for length in range(1, 2):  # Handle 2+ word majors
              phrase = tuple(tokens[i:i+length])
              if phrase in skill_tokens:
                  found_skills.add(skill_tokens[phrase])
      
      self.result.update({'skills': list(found_skills)})

    def extract_dob(self):
      dob_match = re.search(r"(?:date of birth|dob)[\s:]*([\d]{1,2}[-/.\s]?\d{1,2}[-/.\s]?\d{2,4})", self.cv_text, re.I)
      if dob_match:
          self.result.update({'date_of_birth': dob_match.group(1)})  # Return the matched DOB
      return None
    

    def extract_gpa(self):
        gpa_match = re.search(r'(\d\.\d{1,2})\s*/\s*4\.0', self.cv_text)
        if gpa_match:
            self.result.update({'gpa': gpa_match.group(1)})  # Return the matched GPA
        return None

    def extract_university(self):
        for ent in self.doc.ents:
            if ent.label_ == "ORG" and ("university" in ent.text.lower() or "college" in ent.text.lower()):
                self.result.update({'university': ent.text})
                return
        return None

    def extract_gender(self):
        gender_match = re.search(r'gender[:\s]*(male|female)', self.cv_text, re.I)
        if gender_match:
            self.result.update({'gender': gender_match.group(1).capitalize()})
        return None

    def extract_nationality(self):
        for ent in self.doc.ents:
            if ent.label_ == "GPE":
                self.result.update({'nationality': ent.text})
                return
        return None

    def extract_graduation_year(self):
        match = re.search(r'graduation\s*(year)?[:\s]*([\d]{4})', self.cv_text, re.I)
        if match:
            self.result.update({'graduation_year': match.group(2)})
        return None

    def extract_degree(self):
        match = re.search(r'(bachelor|master|ph\.?d|msc|bsc)', self.cv_text, re.I)
        if match:
            self.result.update({'degree': match.group(0)})
        return None

    def extract_major(self):
        major_tokens = {tuple(major.lower().split()): major for major in self.majors}
        found_majors = set()
        
        # Lowercase all input tokens for case-insensitive comparison
        tokens = [token.text.lower() for token in self.doc]

        # Iterate through tokens using a sliding window
        for i in range(len(tokens)):
            for length in range(2, 5):  # Handle 2+ word majors
                phrase = tuple(tokens[i:i+length])
                if phrase in major_tokens:
                    found_majors.add(major_tokens[phrase])
        if not found_majors:
            return
        self.result.update({'major': list(found_majors)[0]})

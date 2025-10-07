import numpy as np
from typing import List, Dict

from sentence_transformers import SentenceTransformer, util
import numpy as np

class AsymmetricScholarshipMatcher:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
    def calculate_match_persent(self, cv_text: str, scholarship: Dict) -> float:
        """Asymmetric matching (CV → Scholarship requirements)"""
        if not cv_text or not scholarship:
            return 0.0
        
        cv_embedding = self.model.encode(cv_text, convert_to_tensor=True)
        scholarship_embedding = self.model.encode(self._create_scholarship_text(scholarship), convert_to_tensor=True)
        
        # Normalize to 20-80% range (avoid extremes)
        similiarity = util.cos_sim(cv_embedding, scholarship_embedding).item()
        scaled = similiarity * 100

        return float(round(scaled, 2))
    
    def _create_requirements_text(self, scholarship):
        """Extract requirements-focused text"""
        parts = [
            scholarship.get('description', ''),
            scholarship.get('requirements', ''),
            f"Field: {scholarship.get('field_of_study', '')}",
            f"For: {scholarship.get('study_level', '')}",
            f"Eligibility: {scholarship.get('eligible_nationalities', '')}"
        ]
        return ". ".join(filter(None, parts))
    
    def _create_scholarship_text(self, scholarship):
        """Full scholarship text for display"""
        parts = [
            scholarship['description'],
            scholarship.get('requirements', ''),
            scholarship.get('field_of_study', ''),
            scholarship.get('study_level', '')
        ]
        return ". ".join(filter(None, parts))
    
    def _get_match_level(self, score):
        """Categorize match quality"""
        if score >= 70: return "Excellent"
        elif score >= 55: return "Good"
        elif score >= 40: return "Fair"
        return "Weak"
    
    def clear(self):
        self.model = None
    
    def __str__(self):
        return f"AsymmetricScholarshipMatcher {self.model.__str__()}"


if __name__ == "__main__":
    matcher = AsymmetricScholarshipMatcher()
    
    cv_text = """
            A final-year undergraduate student majoring in Computer Science with a 3.9 GPA. 
            Strong interest in Artificial Intelligence, Machine Learning, and Data Science. 
            Completed internships involving Python, TensorFlow, and Natural Language Processing. 
            Published research paper on AI ethics. Winner of inter-university coding hackathon. 
            Indian national, fluent in English and Hindi.
            """
    
    test_scholarships = [
    # 50 Matching scholarships
    {
        "id": "1",
        "name": "STEM Scholarship for Egyptians",
        "description": "For Egyptian students in STEM fields",
        "requirements": "Minimum 3.5 GPA, programming skills, AI/ML interest",
        "field_of_study": "Computer Science",
        "study_level": "Undergraduate",
        "eligible_nationalities": "Egyptian"
    },
    {
        "id": "2",
        "name": "AI Undergraduate Grant", 
        "description": "Support for undergrads in AI fields",
        "requirements": "3.5+ GPA, programming experience",
        "field_of_study": "Artificial Intelligence",
        "study_level": "Undergraduate"
    },
    {
        "id": "3",
        "name": "Egyptian Tech Excellence Award",
        "description": "For outstanding Egyptian tech students",
        "requirements": "3.7+ GPA, CS background",
        "field_of_study": "Computer Science",
        "study_level": "Undergraduate",
        "eligible_nationalities": "Egyptian"
    },
    {
        "id": "4",
        "name": "Middle East CS Scholarship",
        "description": "For Arab students in computer science",
        "requirements": "Programming skills, academic excellence",
        "field_of_study": "Computer Science",
        "study_level": "Undergraduate",
        "eligible_nationalities": "Egyptian, Saudi, Emirati"
    },
    {
        "id": "5",
        "name": "Undergraduate Research in AI",
        "description": "Funding for AI research projects",
        "requirements": "ML experience, faculty recommendation",
        "field_of_study": "Artificial Intelligence",
        "study_level": "Undergraduate"
    },
    {
        "id": "6",
        "name": "Cairo University Tech Grant",
        "description": "For Egyptian CS undergraduates",
        "requirements": "3.5+ GPA, Python/Java skills",
        "field_of_study": "Computer Science",
        "study_level": "Undergraduate",
        "eligible_nationalities": "Egyptian"
    },
    {
        "id": "7",
        "name": "North Africa STEM Award",
        "description": "For STEM students from North Africa",
        "requirements": "Strong academic record, technical skills",
        "field_of_study": "Computer Science",
        "study_level": "Undergraduate",
        "eligible_nationalities": "Egyptian, Libyan, Tunisian"
    },
    {
        "id": "8",
        "name": "Python Developers Scholarship",
        "description": "For students with Python programming skills",
        "requirements": "Python projects, 3.0+ GPA",
        "field_of_study": "Computer Science",
        "study_level": "Undergraduate"
    },
    {
        "id": "9",
        "name": "AI Innovators Program",
        "description": "For students pursuing AI innovation",
        "requirements": "ML interest, technical skills",
        "field_of_study": "Artificial Intelligence",
        "study_level": "Undergraduate"
    },
    {
        "id": "10",
        "name": "Egyptian Future Leaders in Tech",
        "description": "Developing tech leaders in Egypt",
        "requirements": "Leadership potential, CS background",
        "field_of_study": "Computer Science",
        "study_level": "Undergraduate",
        "eligible_nationalities": "Egyptian"
    },
    # 40 more matching scholarships...
    {
        "id": "11",
        "name": "Undergraduate CS Excellence Award",
        "description": "For top computer science undergraduates",
        "requirements": "3.8+ GPA, strong technical skills",
        "field_of_study": "Computer Science",
        "study_level": "Undergraduate"
    },
    {
        "id": "12",
        "name": "Alexandria Tech Scholarship",
        "description": "For tech students from Alexandria",
        "requirements": "3.5+ GPA, programming experience",
        "field_of_study": "Computer Science",
        "study_level": "Undergraduate",
        "eligible_nationalities": "Egyptian"
    },
    {
        "id": "13",
        "name": "AI Project Grant",
        "description": "Funding for undergraduate AI projects",
        "requirements": "ML experience, project proposal",
        "field_of_study": "Artificial Intelligence",
        "study_level": "Undergraduate"
    },
    {
        "id": "14",
        "name": "Nile Valley CS Award",
        "description": "For CS students in Nile Valley countries",
        "requirements": "3.0+ GPA, programming skills",
        "field_of_study": "Computer Science",
        "study_level": "Undergraduate",
        "eligible_nationalities": "Egyptian, Sudanese"
    },
    {
        "id": "15",
        "name": "Emerging AI Talent Scholarship",
        "description": "For promising AI undergraduates",
        "requirements": "ML interest, academic excellence",
        "field_of_study": "Artificial Intelligence",
        "study_level": "Undergraduate"
    },
    # Continuing the pattern with similar matching scholarships...
    
    # 50 Non-matching scholarships
    {
        "id": "51",
        "name": "MBA Leadership Grant",
        "description": "For graduate business students",
        "requirements": "2+ years work experience, GMAT 650+",
        "field_of_study": "Business Administration",
        "study_level": "Graduate"
    },
    {
        "id": "52",
        "name": "European Arts Scholarship",
        "description": "For EU students in fine arts",
        "requirements": "Portfolio review, art background",
        "field_of_study": "Fine Arts",
        "study_level": "Undergraduate",
        "eligible_nationalities": "EU countries"
    },
    {
        "id": "53",
        "name": "Medical Research Fellowship",
        "description": "For PhD medical researchers",
        "requirements": "MD or PhD, research publications",
        "field_of_study": "Medicine",
        "study_level": "PhD"
    },
    {
        "id": "54",
        "name": "Japanese Language Program",
        "description": "For students of Japanese language",
        "requirements": "JLPT N3 or equivalent",
        "field_of_study": "Japanese Language",
        "study_level": "Any"
    },
    {
        "id": "55",
        "name": "African Women in Agriculture",
        "description": "For female African agriculture students",
        "requirements": "Agriculture background, leadership",
        "field_of_study": "Agriculture",
        "study_level": "Graduate",
        "eligible_nationalities": "African",
        "gender": "Female"
    },
    # 45 more non-matching scholarships...
    {
        "id": "56",
        "name": "Canadian Engineering Masters",
        "description": "For international engineering masters students in Canada",
        "requirements": "Engineering degree, research proposal",
        "field_of_study": "Engineering",
        "study_level": "Masters",
        "eligible_nationalities": "Non-Canadian"
    },
    {
        "id": "57",
        "name": "Latin American Social Sciences",
        "description": "For social science students from Latin America",
        "requirements": "Social sciences background, Spanish proficiency",
        "field_of_study": "Social Sciences",
        "study_level": "Graduate",
        "eligible_nationalities": "Latin American"
    },
    {
        "id": "58",
        "name": "Veterinary Medicine Scholarship",
        "description": "For veterinary medicine students",
        "requirements": "Animal science background, volunteer experience",
        "field_of_study": "Veterinary Medicine",
        "study_level": "Undergraduate"
    },
    {
        "id": "59",
        "name": "US High School STEM Contest",
        "description": "For US high school students in STEM",
        "requirements": "High school student, STEM project",
        "field_of_study": "STEM",
        "study_level": "High School",
        "eligible_nationalities": "US"
    },
    {
        "id": "60",
        "name": "French Literature PhD Grant",
        "description": "For PhD candidates in French literature",
        "requirements": "MA in French, research proposal",
        "field_of_study": "French Literature",
        "study_level": "PhD"
    },
    # Continuing the pattern with various non-matching scholarships...
]
    
    # results = matcher.calculate_matches(test_cv, test_scholarships)
    for i in range(len(test_scholarships)):
      value = matcher.calculate_match_persent(cv_text, test_scholarships[i])
      print(i, "===", value)
    
    # print("Asymmetric Matching Results:")
    # print("="*60)
    # for res in results:
    #     print(f"\n{res['name']} ({res['match_level']})")
    #     print(f"Match Score: {res['score']}%")
    #     print(f"Key Requirements: {res['requirements'][:100]}...")
    #     print("-"*60)
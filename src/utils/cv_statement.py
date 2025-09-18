import json

class CvToStatement:
  def __init__(self, cv_object):
    self.cv_object = cv_object
    self.statement = self.cv_to_profile()

  def get_statement(self):
    return self.statement
  
  def cv_to_profile(self):
    """Convert parsed CV data into a human-readable summary"""
    try:
        statement_parts = []
        
        # 1. Basic Information
        basic_info = []
        if self.cv_object.get('gender'):
            basic_info.append(f"a {self.cv_object['gender'].lower()}")
        if self.cv_object.get('nationality'):
            basic_info.append(f"from {self.cv_object['nationality']}")
        if self.cv_object.get('degree') or self.cv_object.get('major'):
            if self.cv_object.get('degree') and self.cv_object.get('major'):
                basic_info.append(f"with a {self.cv_object['degree']}'s degree in {self.cv_object['major']}")
            elif self.cv_object.get('degree'):
                basic_info.append(f"with a {self.cv_object['degree']}'s degree")
            elif self.cv_object.get('major'):
                basic_info.append(f"with a {self.cv_object['major']} major")
        
        if basic_info:
            statement_parts.append("I am " + " ".join(basic_info) + ".")
        
        # 2. Academic Information
        academic_info = []
        if self.cv_object.get('gpa'):
            academic_info.append(f"gpa of {self.cv_object['gpa']}")
        if self.cv_object.get('university'):
            academic_info.append(f"studied at {self.cv_object['university']}")
        if self.cv_object.get('graduation_year'):
            academic_info.append(f"graduated in {self.cv_object['graduation_year']}")
        
        if academic_info:
            statement_parts.append("I have a " + " and ".join(academic_info) + ".")
        
        # 3. Skills
        if self.cv_object.get('skills'):
            skills = json.loads(self.cv_object['skills'])
            skill_text = "My skills include " + ", ".join(skills)
            statement_parts.append(skill_text + ".")
        
       
        
        # Combine all parts
        statement = " ".join(statement_parts)
        
        # Clean up formatting
        statement = (statement.replace(" ,", ",")
                  .replace(" .", ".")
                  .replace("  ", " ")
                  .strip())
        
        return statement
    
    except Exception as e:
        print(f"Error generating profile: {str(e)}")
        return "Could not generate profile due to incomplete data"
    


# user_cv_dict = user.cv.__dict__.copy()
#     user_cv_dict["skills"] = json.loads(user_cv_dict["skills"])
#     cv_to_statement = CvToStatement(cv_object=user_cv_dict)
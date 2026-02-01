#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillgap_project.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from analyzer.models import Skill, Company, JobRole, JobRoleSkill, LearningResource

print("Creating skills...")
skills_data = [
    ('Python', 'Programming', 'Beginner'),
    ('Java', 'Programming', 'Beginner'),
    ('JavaScript', 'Programming', 'Beginner'),
    ('C++', 'Programming', 'Intermediate'),
    ('Django', 'Web Framework', 'Intermediate'),
    ('Spring Boot', 'Web Framework', 'Intermediate'),
    ('React', 'Web Framework', 'Intermediate'),
    ('Angular', 'Web Framework', 'Intermediate'),
    ('MySQL', 'Database', 'Beginner'),
    ('PostgreSQL', 'Database', 'Beginner'),
    ('MongoDB', 'Database', 'Intermediate'),
    ('SQL', 'Database', 'Beginner'),
    ('Git', 'Version Control', 'Beginner'),
    ('Docker', 'DevOps', 'Intermediate'),
    ('Kubernetes', 'DevOps', 'Advanced'),
    ('AWS', 'Cloud', 'Intermediate'),
    ('Azure', 'Cloud', 'Intermediate'),
    ('REST API', 'API', 'Intermediate'),
    ('Microservices', 'Architecture', 'Advanced'),
]

skills = {}
for name, category, difficulty in skills_data:
    skill, created = Skill.objects.get_or_create(
        name=name, 
        defaults={'category': category, 'difficulty_level': difficulty}
    )
    skills[name] = skill
    if created:
        print(f"  ✓ {name}")

print(f"\nCreating companies...")
companies_data = [
    ('TCS', 'TCS', 'Mumbai, India', 1968, 'Tata Consultancy Services - IT leader'),
    ('Infosys', 'INFY', 'Bangalore, India', 1981, 'Infosys - Global IT consulting'),
    ('Wipro', 'WIPRO', 'Bangalore, India', 1980, 'Wipro - IT services provider'),
    ('HCL', 'HCL', 'Noida, India', 1976, 'HCL Technologies - IT company'),
    ('Google', 'GOOG', 'Mountain View, USA', 1998, 'Google - Search & cloud'),
    ('Microsoft', 'MSFT', 'Redmond, USA', 1975, 'Microsoft - Software & cloud'),
    ('Amazon', 'AMZN', 'Seattle, USA', 1994, 'Amazon - Cloud & e-commerce'),
]

companies = {}
for name, code, hq, year, desc in companies_data:
    company, created = Company.objects.get_or_create(
        name=name, 
        defaults={
            'code': code, 
            'headquarters': hq,
            'established_year': year,
            'description': desc,
            'website': f'https://www.{name.lower()}.com'
        }
    )
    companies[name] = company
    if created:
        print(f"  ✓ {name}")

print(f"\nCreating job roles...")
roles_data = [
    ('TCS', 'Java Developer', 0, '3-5 LPA', ['Java', 'SQL', 'Git', 'Spring Boot']),
    ('TCS', 'Python Developer', 0, '3-5 LPA', ['Python', 'Django', 'SQL', 'Git']),
    ('Infosys', 'Full Stack Developer', 1, '4-7 LPA', ['Java', 'React', 'SQL', 'REST API']),
    ('Infosys', 'DevOps Engineer', 2, '6-10 LPA', ['Docker', 'Kubernetes', 'AWS', 'Python']),
    ('Wipro', 'QA Automation', 1, '3-5 LPA', ['Python', 'SQL', 'Git', 'REST API']),
    ('Google', 'Software Engineer', 0, '15-25 LPA', ['Python', 'Java', 'JavaScript', 'SQL', 'Microservices']),
    ('Microsoft', 'Cloud Architect', 2, '20-30 LPA', ['Azure', 'SQL', 'Docker', 'REST API']),
    ('Amazon', 'Backend Engineer', 1, '15-20 LPA', ['Java', 'Python', 'AWS', 'SQL', 'Microservices']),
]

for company_name, role_title, exp, salary, role_skills in roles_data:
    company = companies[company_name]
    job_role, created = JobRole.objects.get_or_create(
        company=company, 
        title=role_title,
        defaults={
            'required_experience': exp, 
            'salary_range': salary,
            'description': f'{role_title} role at {company_name}'
        }
    )
    if created:
        print(f"  ✓ {role_title} @ {company_name}")
        
        for i, skill_name in enumerate(role_skills):
            skill = skills.get(skill_name)
            if skill:
                JobRoleSkill.objects.get_or_create(
                    job_role=job_role, 
                    skill=skill,
                    defaults={'proficiency_level': 'Intermediate', 'is_mandatory': i < 2}
                )

print(f"\n{'='*60}")
print(f"✓ Database populated successfully!")
print(f"{'='*60}")
print(f"\nSummary:")
print(f"  Skills: {Skill.objects.count()}")
print(f"  Companies: {Company.objects.count()}")
print(f"  Job Roles: {JobRole.objects.count()}")
print(f"\nNow refresh http://localhost:8000/dashboard/")
print("You should see skills to add!\n")

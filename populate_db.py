"""
Django Shell Script - Populate Database with Sample Data

Run this with: python manage.py shell < populate_db.py
Or copy-paste this into: python manage.py shell
"""

from analyzer.models import Skill, Company, JobRole, JobRoleSkill, LearningResource

# ============================================================================
# 1. CREATE SKILLS
# ============================================================================

print("Creating skills...")

skills_data = [
    # Programming Languages
    {'name': 'Python', 'category': 'Programming', 'difficulty_level': 'Beginner'},
    {'name': 'Java', 'category': 'Programming', 'difficulty_level': 'Beginner'},
    {'name': 'JavaScript', 'category': 'Programming', 'difficulty_level': 'Beginner'},
    {'name': 'C++', 'category': 'Programming', 'difficulty_level': 'Intermediate'},
    {'name': 'C#', 'category': 'Programming', 'difficulty_level': 'Intermediate'},
    
    # Web Frameworks
    {'name': 'Django', 'category': 'Web Framework', 'difficulty_level': 'Intermediate'},
    {'name': 'Spring Boot', 'category': 'Web Framework', 'difficulty_level': 'Intermediate'},
    {'name': 'React', 'category': 'Web Framework', 'difficulty_level': 'Intermediate'},
    {'name': 'Angular', 'category': 'Web Framework', 'difficulty_level': 'Intermediate'},
    {'name': 'Node.js', 'category': 'Web Framework', 'difficulty_level': 'Intermediate'},
    
    # Databases
    {'name': 'MySQL', 'category': 'Database', 'difficulty_level': 'Beginner'},
    {'name': 'PostgreSQL', 'category': 'Database', 'difficulty_level': 'Beginner'},
    {'name': 'MongoDB', 'category': 'Database', 'difficulty_level': 'Intermediate'},
    {'name': 'Redis', 'category': 'Database', 'difficulty_level': 'Advanced'},
    
    # DevOps & Tools
    {'name': 'Git', 'category': 'Version Control', 'difficulty_level': 'Beginner'},
    {'name': 'Docker', 'category': 'DevOps', 'difficulty_level': 'Intermediate'},
    {'name': 'Kubernetes', 'category': 'DevOps', 'difficulty_level': 'Advanced'},
    {'name': 'AWS', 'category': 'Cloud', 'difficulty_level': 'Intermediate'},
    {'name': 'Azure', 'category': 'Cloud', 'difficulty_level': 'Intermediate'},
    
    # Other
    {'name': 'SQL', 'category': 'Database', 'difficulty_level': 'Beginner'},
    {'name': 'REST API', 'category': 'API', 'difficulty_level': 'Intermediate'},
    {'name': 'Microservices', 'category': 'Architecture', 'difficulty_level': 'Advanced'},
    {'name': 'Machine Learning', 'category': 'AI/ML', 'difficulty_level': 'Advanced'},
]

skills = {}
for skill_data in skills_data:
    skill, created = Skill.objects.get_or_create(
        name=skill_data['name'],
        defaults={
            'category': skill_data['category'],
            'difficulty_level': skill_data['difficulty_level']
        }
    )
    skills[skill_data['name']] = skill
    if created:
        print(f"  ✓ Created skill: {skill_data['name']}")
    else:
        print(f"  - Skill exists: {skill_data['name']}")

# ============================================================================
# 2. CREATE COMPANIES
# ============================================================================

print("\nCreating companies...")

companies_data = [
    {'name': 'TCS', 'code': 'TCS', 'headquarters': 'Mumbai, India'},
    {'name': 'Infosys', 'code': 'INFY', 'headquarters': 'Bangalore, India'},
    {'name': 'Wipro', 'code': 'WIPRO', 'headquarters': 'Bangalore, India'},
    {'name': 'HCL Technologies', 'code': 'HCL', 'headquarters': 'Noida, India'},
    {'name': 'Google', 'code': 'GOOG', 'headquarters': 'Mountain View, USA'},
    {'name': 'Microsoft', 'code': 'MSFT', 'headquarters': 'Redmond, USA'},
    {'name': 'Amazon', 'code': 'AMZN', 'headquarters': 'Seattle, USA'},
    {'name': 'Accenture', 'code': 'ACN', 'headquarters': 'Dublin, Ireland'},
]

companies = {}
for company_data in companies_data:
    company, created = Company.objects.get_or_create(
        name=company_data['name'],
        defaults={
            'code': company_data['code'],
            'headquarters': company_data['headquarters']
        }
    )
    companies[company_data['name']] = company
    if created:
        print(f"  ✓ Created company: {company_data['name']}")
    else:
        print(f"  - Company exists: {company_data['name']}")

# ============================================================================
# 3. CREATE JOB ROLES
# ============================================================================

print("\nCreating job roles...")

roles_data = [
    # TCS Roles
    {
        'company': 'TCS',
        'title': 'Java Developer',
        'description': 'Develop enterprise Java applications',
        'required_experience': '0-2 years',
        'salary_range': '3-5 LPA',
        'skills': ['Java', 'SQL', 'REST API', 'Git']
    },
    {
        'company': 'TCS',
        'title': 'Python Developer',
        'description': 'Build scalable Python applications',
        'required_experience': '0-2 years',
        'salary_range': '3-5 LPA',
        'skills': ['Python', 'Django', 'SQL', 'Git']
    },
    
    # Infosys Roles
    {
        'company': 'Infosys',
        'title': 'Full Stack Developer',
        'description': 'Develop front-end and back-end applications',
        'required_experience': '1-3 years',
        'salary_range': '4-7 LPA',
        'skills': ['Java', 'React', 'SQL', 'REST API', 'Git']
    },
    {
        'company': 'Infosys',
        'title': 'DevOps Engineer',
        'description': 'Manage infrastructure and deployment',
        'required_experience': '2-4 years',
        'salary_range': '6-10 LPA',
        'skills': ['Docker', 'Kubernetes', 'AWS', 'Git', 'Python']
    },
    
    # Wipro Roles
    {
        'company': 'Wipro',
        'title': 'QA Automation Engineer',
        'description': 'Automate testing and quality assurance',
        'required_experience': '1-2 years',
        'salary_range': '3-5 LPA',
        'skills': ['Python', 'SQL', 'Git', 'REST API']
    },
    
    # Google Roles
    {
        'company': 'Google',
        'title': 'Software Engineer',
        'description': 'Develop scalable software solutions',
        'required_experience': '0-3 years',
        'salary_range': '15-25 LPA',
        'skills': ['Python', 'Java', 'JavaScript', 'SQL', 'Microservices']
    },
    
    # Microsoft Roles
    {
        'company': 'Microsoft',
        'title': 'Cloud Solution Architect',
        'description': 'Design cloud-based solutions',
        'required_experience': '3-5 years',
        'salary_range': '20-30 LPA',
        'skills': ['Azure', 'SQL', 'Docker', 'REST API']
    },
    
    # Amazon Roles
    {
        'company': 'Amazon',
        'title': 'Backend Engineer',
        'description': 'Build high-performance backend systems',
        'required_experience': '1-3 years',
        'salary_range': '15-20 LPA',
        'skills': ['Java', 'Python', 'AWS', 'SQL', 'Microservices']
    },
]

job_roles = {}
for role_data in roles_data:
    company = companies[role_data['company']]
    job_role, created = JobRole.objects.get_or_create(
        company=company,
        title=role_data['title'],
        defaults={
            'description': role_data['description'],
            'required_experience': role_data['required_experience'],
            'salary_range': role_data['salary_range']
        }
    )
    
    if created:
        print(f"  ✓ Created role: {role_data['title']} @ {role_data['company']}")
        
        # Add skills to job role
        for skill_name in role_data['skills']:
            skill = skills[skill_name]
            is_mandatory = skill_name in ['Java', 'Python', 'SQL']  # Make some mandatory
            
            JobRoleSkill.objects.get_or_create(
                job_role=job_role,
                skill=skill,
                defaults={
                    'proficiency_level': 'Intermediate',
                    'is_mandatory': is_mandatory
                }
            )
    else:
        print(f"  - Role exists: {role_data['title']} @ {role_data['company']}")

# ============================================================================
# 4. CREATE LEARNING RESOURCES
# ============================================================================

print("\nCreating learning resources...")

resources_data = [
    {'skill': 'Python', 'title': 'Python for Everybody', 'type': 'Course', 'url': 'https://www.coursera.org/learn/python', 'is_free': True},
    {'skill': 'Python', 'title': 'Python Crash Course', 'type': 'Book', 'url': 'https://nostarch.com/pythoncrashcourse2e', 'is_free': False},
    
    {'skill': 'Java', 'title': 'Java Programming Masterclass', 'type': 'Video Course', 'url': 'https://www.udemy.com/course/java-the-complete-java-developer-course', 'is_free': False},
    {'skill': 'Java', 'title': 'Java Official Docs', 'type': 'Documentation', 'url': 'https://docs.oracle.com/javase/tutorial', 'is_free': True},
    
    {'skill': 'Django', 'title': 'Django for Beginners', 'type': 'Book', 'url': 'https://djangoforbeginners.com', 'is_free': False},
    {'skill': 'Django', 'title': 'Django Official Docs', 'type': 'Documentation', 'url': 'https://docs.djangoproject.com', 'is_free': True},
    
    {'skill': 'React', 'title': 'React Official Tutorial', 'type': 'Tutorial', 'url': 'https://react.dev', 'is_free': True},
    {'skill': 'React', 'title': 'Complete React Course', 'type': 'Video Course', 'url': 'https://www.udemy.com/course/react-the-complete-guide', 'is_free': False},
    
    {'skill': 'SQL', 'title': 'W3Schools SQL', 'type': 'Interactive Tutorial', 'url': 'https://www.w3schools.com/sql', 'is_free': True},
    {'skill': 'SQL', 'title': 'SQL in 100 Pages', 'type': 'E-book', 'url': 'https://sql-in-100-pages.com', 'is_free': False},
    
    {'skill': 'Docker', 'title': 'Docker Getting Started', 'type': 'Tutorial', 'url': 'https://www.docker.com/101-tutorial', 'is_free': True},
    {'skill': 'Docker', 'title': 'Docker Mastery', 'type': 'Video Course', 'url': 'https://www.udemy.com/course/docker-mastery', 'is_free': False},
    
    {'skill': 'AWS', 'title': 'AWS Free Tier', 'type': 'Hands-on Labs', 'url': 'https://aws.amazon.com/free', 'is_free': True},
    {'skill': 'AWS', 'title': 'AWS Solutions Architect', 'type': 'Certification Course', 'url': 'https://aws.amazon.com/training', 'is_free': False},
]

for resource_data in resources_data:
    skill = skills[resource_data['skill']]
    resource, created = LearningResource.objects.get_or_create(
        skill=skill,
        title=resource_data['title'],
        defaults={
            'resource_type': resource_data['type'],
            'url': resource_data['url'],
            'is_free': resource_data['is_free']
        }
    )
    if created:
        print(f"  ✓ Created resource: {resource_data['title']} for {resource_data['skill']}")
    else:
        print(f"  - Resource exists: {resource_data['title']}")

print("\n" + "="*60)
print("✓ Database population completed successfully!")
print("="*60)
print(f"\nSummary:")
print(f"  Skills: {Skill.objects.count()}")
print(f"  Companies: {Company.objects.count()}")
print(f"  Job Roles: {JobRole.objects.count()}")
print(f"  Learning Resources: {LearningResource.objects.count()}")
print("\nNow refresh your browser and go to http://localhost:8000/dashboard/")
print("You should see skills available to add!\n")

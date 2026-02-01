"""
MODELS.PY - Database Models for Skill Gap Analyzer
=================================================
This file defines all database tables and their relationships.

Models:
1. StudentProfile - Extended user information
2. Skill - Master data for all skills
3. Company - Recruiting companies
4. JobRole - Job positions available
5. JobRoleSkill - M2M relationship for required skills per role
6. StudentSkill - M2M relationship for student's current skills
7. LearningResource - Resources to learn specific skills
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class StudentProfile(models.Model):
    """
    Extended student information linked to Django User model.
    
    Relationship: One Student has One Profile (1:1)
    This extends Django's User model with academic information.
    
    Example:
        Student Rahul → User(username='rahul') + StudentProfile(year='TY')
    """
    
    YEAR_CHOICES = [
        ('FY', 'First Year'),
        ('SY', 'Second Year'),
        ('TY', 'Third Year'),
        ('FIN', 'Final Year'),
    ]
    
    DEPARTMENT_CHOICES = [
        ('CSE', 'Computer Science & Engineering'),
        ('IT', 'Information Technology'),
        ('ECE', 'Electronics & Communication'),
        ('ME', 'Mechanical Engineering'),
        ('CE', 'Civil Engineering'),
    ]
    
    # Link to Django's built-in User model (One-to-One)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Academic information
    phone_number = models.CharField(max_length=15, help_text="Student's contact number")
    college_name = models.CharField(max_length=200, help_text="College/University name")
    department = models.CharField(max_length=10, choices=DEPARTMENT_CHOICES)
    year = models.CharField(max_length=5, choices=YEAR_CHOICES)
    cgpa = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
        help_text="Cumulative GPA (0-10 scale)"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, help_text="Account creation date")
    updated_at = models.DateTimeField(auto_now=True, help_text="Last updated date")
    
    class Meta:
        verbose_name_plural = "Student Profiles"
        ordering = ['-created_at']  # Newest first
    
    def __str__(self):
        """String representation of student profile"""
        return f"{self.user.username} - {self.year} {self.department}"


class Skill(models.Model):
    """
    Master data for all technical and soft skills.
    
    This is a global, reusable table. Each skill defined once.
    Used as reference by JobRoleSkill and StudentSkill.
    
    Examples:
        - Python (Backend)
        - Django (Backend)
        - MySQL (Database)
        - Git (DevOps)
        - Communication (Soft Skills)
    """
    
    CATEGORY_CHOICES = [
        ('Backend', 'Backend Development'),
        ('Frontend', 'Frontend Development'),
        ('Database', 'Database Management'),
        ('DevOps', 'DevOps & Infrastructure'),
        ('Mobile', 'Mobile Development'),
        ('Data', 'Data Science & Analytics'),
        ('SoftSkills', 'Soft Skills'),
        ('Other', 'Other'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('Beginner', 'Beginner Level'),
        ('Intermediate', 'Intermediate Level'),
        ('Advanced', 'Advanced Level'),
    ]
    
    name = models.CharField(
        max_length=100, 
        unique=True,
        help_text="Skill name (e.g., 'Python', 'Django', 'MySQL')"
    )
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(
        help_text="What is this skill used for?"
    )
    difficulty_level = models.CharField(
        max_length=15, 
        choices=DIFFICULTY_CHOICES,
        default='Intermediate'
    )
    
    class Meta:
        verbose_name_plural = "Skills"
        ordering = ['category', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.category})"


class Company(models.Model):
    """
    Recruiting companies that participate in placements.
    
    Examples:
        - TCS (Tata Consultancy Services)
        - Infosys
        - Wipro
        - Accenture
    """
    
    name = models.CharField(
        max_length=200, 
        unique=True,
        help_text="Full company name"
    )
    code = models.CharField(
        max_length=20, 
        unique=True,
        help_text="Short code (e.g., 'TCS', 'INFY')"
    )
    description = models.TextField(help_text="Brief company overview")
    website = models.URLField(blank=True, help_text="Company website")
    headquarters = models.CharField(max_length=200, help_text="HQ location")
    established_year = models.IntegerField(help_text="Year company was founded")
    
    class Meta:
        verbose_name_plural = "Companies"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.code})"


class JobRole(models.Model):
    """
    Specific job roles offered by companies.
    
    Relationship: One Company has Many JobRoles (1:M)
    
    Examples:
        - TCS → Junior Python Developer
        - TCS → Junior Frontend Developer
        - Infosys → Data Analyst
    """
    
    EXPERIENCE_CHOICES = [
        (0, 'Fresher (0 years)'),
        (1, '1 year'),
        (2, '2 years'),
        (3, '3+ years'),
    ]
    
    company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE,
        related_name='job_roles',
        help_text="Company offering this role"
    )
    
    title = models.CharField(
        max_length=200,
        help_text="Job position title"
    )
    description = models.TextField(help_text="Role responsibilities and requirements")
    required_experience = models.IntegerField(
        choices=EXPERIENCE_CHOICES,
        help_text="Minimum experience required"
    )
    salary_range = models.CharField(
        max_length=50,
        help_text="Expected salary (e.g., '3.5-4.5 LPA')"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Job Roles"
        ordering = ['company', 'title']
    
    def __str__(self):
        return f"{self.company.code} - {self.title}"


class JobRoleSkill(models.Model):
    """
    Many-to-Many relationship: JobRole ←→ Skill
    
    Tracks which skills are required for each job role.
    Includes proficiency level and mandatory status.
    
    Example:
        - TCS Junior Dev role requires:
          * Python (Intermediate, Mandatory)
          * Django (Intermediate, Mandatory)
          * Git (Basic, Mandatory)
          * AWS (Intermediate, Optional)
    """
    
    PROFICIENCY_CHOICES = [
        ('Basic', 'Basic Knowledge'),
        ('Intermediate', 'Intermediate Level'),
        ('Expert', 'Expert Level'),
    ]
    
    job_role = models.ForeignKey(
        JobRole,
        on_delete=models.CASCADE,
        related_name='required_skills',
        help_text="Job role this skill is required for"
    )
    
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        related_name='job_roles',
        help_text="Required skill"
    )
    
    proficiency_level = models.CharField(
        max_length=15,
        choices=PROFICIENCY_CHOICES,
        default='Intermediate',
        help_text="Required proficiency level for this role"
    )
    
    is_mandatory = models.BooleanField(
        default=True,
        help_text="True if must-have, False if nice-to-have"
    )
    
    class Meta:
        verbose_name_plural = "Job Role Skills"
        unique_together = ('job_role', 'skill')  # Can't add same skill twice to one role
        ordering = ['-is_mandatory', 'skill']
    
    def __str__(self):
        return f"{self.job_role.title} → {self.skill.name}"


class StudentSkill(models.Model):
    """
    Many-to-Many relationship: StudentProfile ←→ Skill
    
    Tracks student's CURRENT skills and proficiency levels.
    This is data entered by student during self-assessment.
    
    Example:
        Student Rahul has:
        * Python (Intermediate, Verified)
        * Django (Basic, Not Verified)
        * MySQL (Intermediate, Verified)
    """
    
    PROFICIENCY_CHOICES = [
        ('Basic', 'Basic Knowledge'),
        ('Intermediate', 'Intermediate Level'),
        ('Expert', 'Expert Level'),
    ]
    
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='skills',
        help_text="Student who has this skill"
    )
    
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        related_name='students',
        help_text="Skill student has"
    )
    
    proficiency_level = models.CharField(
        max_length=15,
        choices=PROFICIENCY_CHOICES,
        default='Intermediate',
        help_text="Student's current proficiency"
    )
    
    verified = models.BooleanField(
        default=False,
        help_text="Admin verified this skill"
    )
    
    added_on = models.DateTimeField(
        auto_now_add=True,
        help_text="When student added this skill"
    )
    
    class Meta:
        verbose_name_plural = "Student Skills"
        unique_together = ('student', 'skill')  # Can't add same skill twice
        ordering = ['-verified', '-added_on']
    
    def __str__(self):
        status = "✓" if self.verified else "○"
        return f"{status} {self.student.user.username} - {self.skill.name}"


class LearningResource(models.Model):
    """
    Learning materials for each skill.
    
    Relationship: One Skill has Many Resources (1:M)
    
    Examples:
        - Python:
          * "Python Official Documentation" (Free)
          * "Complete Python Course on Udemy" (Paid)
          * "Python Tutorial - GeeksforGeeks" (Free)
    """
    
    RESOURCE_TYPE_CHOICES = [
        ('Video', 'Video Course'),
        ('Article', 'Article/Blog'),
        ('Course', 'Online Course'),
        ('Documentation', 'Official Documentation'),
        ('Book', 'Book/eBook'),
        ('Tutorial', 'Interactive Tutorial'),
        ('Other', 'Other'),
    ]
    
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        related_name='resources',
        help_text="Skill this resource teaches"
    )
    
    title = models.CharField(
        max_length=300,
        help_text="Resource title"
    )
    
    resource_type = models.CharField(
        max_length=20,
        choices=RESOURCE_TYPE_CHOICES,
        help_text="Type of learning material"
    )
    
    url = models.URLField(
        help_text="Link to the resource"
    )
    
    description = models.TextField(
        blank=True,
        help_text="Brief description of what this resource covers"
    )
    
    difficulty_level = models.CharField(
        max_length=15,
        choices=[
            ('Beginner', 'Beginner'),
            ('Intermediate', 'Intermediate'),
            ('Advanced', 'Advanced'),
        ],
        default='Intermediate',
        help_text="Recommended difficulty level"
    )
    
    estimated_hours = models.IntegerField(
        help_text="Estimated time to complete (in hours)"
    )
    
    is_free = models.BooleanField(
        default=True,
        help_text="True if free, False if paid"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Learning Resources"
        ordering = ['-is_free', 'difficulty_level']
    
    def __str__(self):
        cost = "FREE" if self.is_free else "PAID"
        return f"{self.skill.name} - {self.title} [{cost}]"


# ============================================================================
# OPTIONAL: Model for tracking student's analysis history
# ============================================================================

class SkillGapAnalysis(models.Model):
    """
    Optional: Track each time a student analyzes a job role.
    Useful for:
    - Tracking student progress over time
    - Analytics (which roles are popular)
    - Recommendations (suggest easier roles first)
    """
    
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='analyses'
    )
    
    job_role = models.ForeignKey(
        JobRole,
        on_delete=models.CASCADE
    )
    
    # Results snapshot (calculated at analysis time)
    skills_matched = models.IntegerField()
    total_required_skills = models.IntegerField()
    placement_readiness_percentage = models.FloatField()
    
    # Metadata
    analyzed_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Skill Gap Analyses"
        ordering = ['-analyzed_on']
    
    def __str__(self):
        return f"{self.student.user.username} → {self.job_role.title} ({self.placement_readiness_percentage}%)"


# ============================================================================
# HELPFUL DOCSTRING SUMMARY
# ============================================================================

"""
DATABASE RELATIONSHIPS SUMMARY:

1. User (Django) ←→ StudentProfile (1:1)
   └─ Each student has one profile

2. StudentProfile ←→ Skill (M:M via StudentSkill)
   └─ Student can have many skills, skill can belong to many students

3. JobRole ←→ Skill (M:M via JobRoleSkill)
   └─ Role requires many skills, skill required by many roles

4. Skill ←→ LearningResource (1:M)
   └─ One skill has many resources

5. Company ←→ JobRole (1:M)
   └─ Company offers many roles

FLOW:
Student registers → StudentProfile created
Student lists skills → StudentSkill entries created
Student picks role → Fetch JobRoleSkill requirements
Compare → StudentSkill vs JobRoleSkill
Gap Analysis → Generate report with LearningResource recommendations
"""

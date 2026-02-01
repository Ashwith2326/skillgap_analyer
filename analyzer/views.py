"""
VIEWS.PY - Application Logic Layer
===================================

This file contains all view functions that:
1. Handle HTTP requests
2. Interact with database models
3. Implement business logic
4. Render HTML templates

Views handle:
- User Registration & Login
- Skill Dashboard
- Job Role Selection
- Skill Gap Analysis
- Result Generation
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from .models import (
    StudentProfile, Skill, Company, JobRole, 
    JobRoleSkill, StudentSkill, LearningResource, SkillGapAnalysis
)
from .skills_analyzer import SkillGapAnalyzer
import json


# ============================================================================
# AUTHENTICATION VIEWS
# ============================================================================

def register(request):
    """
    Handle student registration.
    
    GET: Show registration form
    POST: Create new user and student profile
    
    Flow:
    1. Get form data from POST request
    2. Validate (passwords match, email unique, etc.)
    3. Create Django User object
    4. Create StudentProfile linked to User
    5. Redirect to login
    """
    
    if request.method == 'POST':
        # Extract form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        phone_number = request.POST.get('phone_number')
        college_name = request.POST.get('college_name')
        department = request.POST.get('department')
        year = request.POST.get('year')
        cgpa = request.POST.get('cgpa')
        
        # Validation 1: Check passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('analyzer:register')
        
        # Validation 2: Check username doesn't exist
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect('analyzer:register')
        
        # Validation 3: Check email doesn't exist
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('analyzer:register')
        
        try:
            # Create Django User
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=username  # Can be improved later
            )
            
            # Create StudentProfile linked to User
            StudentProfile.objects.create(
                user=user,
                phone_number=phone_number,
                college_name=college_name,
                department=department,
                year=year,
                cgpa=float(cgpa)
            )
            
            messages.success(request, "Registration successful! Please login.")
            return redirect('analyzer:login')
        
        except Exception as e:
            messages.error(request, f"Error during registration: {str(e)}")
            return redirect('analyzer:register')
    
    # GET request: Show registration form
    return render(request, 'analyzer/register.html', {
        'departments': StudentProfile.DEPARTMENT_CHOICES,
        'years': StudentProfile.YEAR_CHOICES
    })


def user_login(request):
    """
    Handle student login.
    
    GET: Show login form
    POST: Authenticate user and create session
    
    Flow:
    1. Get username and password from form
    2. Authenticate using Django's authenticate()
    3. If valid, create session using login()
    4. Redirect to dashboard
    """
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Valid credentials: Create session
            login(request, user)
            messages.success(request, f"Welcome back, {username}!")
            return redirect('analyzer:dashboard')
        else:
            # Invalid credentials
            messages.error(request, "Invalid username or password!")
            return redirect('analyzer:login')
    
    # GET request: Show login form
    return render(request, 'analyzer/login.html')


def user_logout(request):
    """
    Handle logout.
    - Clear user session
    - Redirect to login page
    """
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('analyzer:login')


# ============================================================================
# MAIN APPLICATION VIEWS
# ============================================================================

@login_required(login_url='analyzer:login')
def dashboard(request):
    """
    Student dashboard - Skill selection interface.
    
    Purpose:
    - Show all available skills
    - Let student select/deselect skills
    - Submit selected skills to database
    
    Flow:
    1. Fetch all skills from database
    2. Fetch student's current skills
    3. Mark which skills student already has
    4. Show form for selection
    5. On submit, update StudentSkill table
    """
    
    try:
        # Get student profile for current user
        student_profile = StudentProfile.objects.get(user=request.user)
    except StudentProfile.DoesNotExist:
        # User exists but no profile - shouldn't happen normally
        messages.error(request, "Student profile not found. Please contact admin.")
        return redirect('analyzer:login')
    
    # Fetch all skills, grouped by category
    skills_by_category = {}
    for skill in Skill.objects.all().order_by('category', 'name'):
        if skill.category not in skills_by_category:
            skills_by_category[skill.category] = []
        skills_by_category[skill.category].append(skill)
    
    # Get student's current skills (for UI highlighting)
    student_skills = StudentSkill.objects.filter(student=student_profile).values_list('skill_id', flat=True)
    
    if request.method == 'POST':
        # Receive selected skills from form
        selected_skill_ids = request.POST.getlist('skills')
        
        # Clear old skills first
        StudentSkill.objects.filter(student=student_profile).delete()
        
        # Add new skills with proficiency level
        for skill_id in selected_skill_ids:
            try:
                skill = Skill.objects.get(id=skill_id)
                proficiency = request.POST.get(f'proficiency_{skill_id}', 'Intermediate')
                
                StudentSkill.objects.create(
                    student=student_profile,
                    skill=skill,
                    proficiency_level=proficiency,
                    verified=False
                )
            except Skill.DoesNotExist:
                continue
        
        messages.success(request, f"Updated skills! You have {len(selected_skill_ids)} skills selected.")
        return redirect('analyzer:select_role')
    
    # GET request: Show dashboard
    return render(request, 'analyzer/dashboard.html', {
        'skills_by_category': skills_by_category,
        'student_skills': student_skills,
        'proficiency_choices': StudentSkill.PROFICIENCY_CHOICES,
        'student': student_profile
    })


@login_required(login_url='analyzer:login')
def select_role(request):
    """
    Job role selection interface.
    
    Purpose:
    - Show all available job roles
    - Let student select a role for analysis
    - Trigger skill gap analysis
    
    Flow:
    1. Fetch all companies and their roles
    2. Group roles by company
    3. Student selects one role
    4. Redirect to analysis
    """
    
    # Fetch companies with their job roles
    companies = Company.objects.prefetch_related('job_roles').all()
    
    if request.method == 'POST':
        job_role_id = request.POST.get('job_role')
        
        try:
            job_role = JobRole.objects.get(id=job_role_id)
            # Store selected role in session for analysis
            request.session['selected_job_role_id'] = job_role_id
            return redirect('analyzer:analyze_gap')
        except JobRole.DoesNotExist:
            messages.error(request, "Invalid job role selected!")
            return redirect('analyzer:select_role')
    
    # GET request: Show role selection
    return render(request, 'analyzer/select_role.html', {
        'companies': companies
    })


@login_required(login_url='analyzer:login')
def analyze_gap(request):
    """
    Core skill gap analysis engine.
    
    THIS IS THE HEART OF THE PROJECT!
    
    Purpose:
    - Compare student skills with role requirements
    - Calculate gaps
    - Generate recommendations
    - Display results
    
    Business Logic:
    1. Fetch student's current skills
    2. Fetch job role's required skills
    3. Compare and categorize into:
       - Matched (student has it)
       - Gaps (student doesn't have)
       - Extras (student has but role doesn't need)
    4. Calculate placement readiness percentage
    5. Fetch learning resources for gaps
    6. Generate report
    
    Formula:
    Placement Readiness = (Matched Skills / Total Required Skills) × 100
    """
    
    try:
        student_profile = StudentProfile.objects.get(user=request.user)
    except StudentProfile.DoesNotExist:
        messages.error(request, "Student profile not found!")
        return redirect('analyzer:login')
    
    # Get selected job role from session
    job_role_id = request.session.get('selected_job_role_id')
    if not job_role_id:
        messages.error(request, "No job role selected!")
        return redirect('analyzer:select_role')
    
    try:
        job_role = JobRole.objects.get(id=job_role_id)
    except JobRole.DoesNotExist:
        messages.error(request, "Job role not found!")
        return redirect('analyzer:select_role')
    
    # ========== CORE ANALYSIS LOGIC ==========
    
    # Create analyzer instance
    analyzer = SkillGapAnalyzer(student_profile, job_role)
    
    # Perform analysis
    analysis_result = analyzer.analyze()
    
    # ========================================
    
    # Save analysis to history (optional)
    SkillGapAnalysis.objects.create(
        student=student_profile,
        job_role=job_role,
        skills_matched=analysis_result['matched_count'],
        total_required_skills=analysis_result['total_required'],
        placement_readiness_percentage=analysis_result['placement_readiness']
    )
    
    # GET learning resources for gaps
    gap_resources = {}
    for gap_skill in analysis_result['skill_gaps']:
        resources = LearningResource.objects.filter(
            skill=gap_skill['skill'],
            is_free=True  # Show free resources first
        ).order_by('-is_free', 'difficulty_level')
        gap_resources[gap_skill['skill'].id] = {
            'skill': gap_skill['skill'],
            'resources': resources[:5],  # Show top 5 resources
            'proficiency_needed': gap_skill['proficiency_needed']
        }
    
    # Prepare context for template
    context = {
        'job_role': job_role,
        'company': job_role.company,
        'student': student_profile,
        'analysis': analysis_result,
        'gap_resources': gap_resources
    }
    
    return render(request, 'analyzer/result.html', context)


# ============================================================================
# HELPER VIEWS (Optional)
# ============================================================================

def home(request):
    """
    Landing page / home view.
    Show project information and links.
    """
    if request.user.is_authenticated:
        return redirect('analyzer:dashboard')
    
    return render(request, 'analyzer/home.html', {
        'total_companies': Company.objects.count(),
        'total_jobs': JobRole.objects.count(),
        'total_skills': Skill.objects.count()
    })


@login_required(login_url='analyzer:login')
def profile_view(request):
    """
    View and edit student profile information.
    """
    try:
        student_profile = StudentProfile.objects.get(user=request.user)
    except StudentProfile.DoesNotExist:
        messages.error(request, "Profile not found!")
        return redirect('dashboard')
    
    if request.method == 'POST':
        # Update profile fields
        student_profile.phone_number = request.POST.get('phone_number')
        student_profile.college_name = request.POST.get('college_name')
        student_profile.cgpa = float(request.POST.get('cgpa'))
        student_profile.save()
        
        messages.success(request, "Profile updated successfully!")
        return redirect('analyzer:profile')
    
    return render(request, 'analyzer/profile.html', {
        'student': student_profile,
        'departments': StudentProfile.DEPARTMENT_CHOICES,
        'years': StudentProfile.YEAR_CHOICES
    })


@login_required(login_url='analyzer:login')
def skill_history(request):
    """
    Show student's analysis history.
    Track which roles they've analyzed.
    """
    try:
        student_profile = StudentProfile.objects.get(user=request.user)
    except StudentProfile.DoesNotExist:
        return redirect('analyzer:login')
    
    # Fetch all analyses for this student
    analyses = SkillGapAnalysis.objects.filter(
        student=student_profile
    ).select_related('job_role', 'job_role__company').order_by('-analyzed_on')
    
    return render(request, 'analyzer/skill_history.html', {
        'analyses': analyses,
        'total': analyses.count()
    })


# ============================================================================
# API ENDPOINTS (Optional - for AJAX/Future Enhancement)
# ============================================================================

@login_required(login_url='analyzer:login')
def get_role_skills_ajax(request, role_id):
    """
    AJAX endpoint to get required skills for a role.
    
    Used for: Dynamic UI updates without page reload
    Returns: JSON with skill requirements
    """
    try:
        job_role = JobRole.objects.get(id=role_id)
        role_skills = JobRoleSkill.objects.filter(
            job_role=job_role
        ).select_related('skill')
        
        skills_data = [
            {
                'id': rs.skill.id,
                'name': rs.skill.name,
                'proficiency': rs.proficiency_level,
                'mandatory': rs.is_mandatory
            }
            for rs in role_skills
        ]
        
        return JsonResponse({
            'success': True,
            'role_title': job_role.title,
            'company': job_role.company.name,
            'skills': skills_data,
            'total_skills': len(skills_data)
        })
    except JobRole.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Role not found'})


# ============================================================================
# ERROR HANDLERS (Optional)
# ============================================================================

def error_404(request, exception):
    """Handle 404 errors"""
    return render(request, 'analyzer/404.html', status=404)


def error_500(request):
    """Handle 500 errors"""
    return render(request, 'analyzer/500.html', status=500)

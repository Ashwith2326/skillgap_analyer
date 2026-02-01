"""
ADMIN.PY - Django Admin Configuration
======================================

This file configures which models appear in Django Admin panel.

The Django Admin is a built-in feature that provides:
✅ Create/Read/Update/Delete (CRUD) operations
✅ Data management interface
✅ Perfect for adding demo data
✅ No need to write database management code
"""

from django.contrib import admin
from .models import (
    StudentProfile, Skill, Company, JobRole, 
    JobRoleSkill, StudentSkill, LearningResource, SkillGapAnalysis
)


# ============================================
# STUDENT PROFILE ADMIN
# ============================================

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    """Customize how StudentProfile appears in admin"""
    
    list_display = ('user', 'college_name', 'department', 'year', 'cgpa', 'created_at')
    list_filter = ('department', 'year', 'created_at')
    search_fields = ('user__username', 'user__email', 'college_name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Contact', {
            'fields': ('phone_number',)
        }),
        ('Academic', {
            'fields': ('college_name', 'department', 'year', 'cgpa')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# ============================================
# SKILL ADMIN
# ============================================

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    """Customize how Skill appears in admin"""
    
    list_display = ('name', 'category', 'difficulty_level')
    list_filter = ('category', 'difficulty_level')
    search_fields = ('name', 'description')
    ordering = ('category', 'name')


# ============================================
# COMPANY ADMIN
# ============================================

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """Customize how Company appears in admin"""
    
    list_display = ('name', 'code', 'headquarters', 'established_year')
    search_fields = ('name', 'code', 'headquarters')
    readonly_fields = ('established_year',)


# ============================================
# JOB ROLE ADMIN
# ============================================

@admin.register(JobRole)
class JobRoleAdmin(admin.ModelAdmin):
    """Customize how JobRole appears in admin"""
    
    list_display = ('title', 'company', 'required_experience', 'salary_range', 'created_at')
    list_filter = ('company', 'required_experience', 'created_at')
    search_fields = ('title', 'description', 'company__name')
    readonly_fields = ('created_at', 'updated_at')


# ============================================
# JOB ROLE SKILL INLINE
# ============================================

class JobRoleSkillInline(admin.TabularInline):
    """Inline editing of skills for a job role"""
    model = JobRoleSkill
    extra = 1  # Show 1 empty row for adding new
    fields = ('skill', 'proficiency_level', 'is_mandatory')


# Add inline to JobRole
JobRoleAdmin.inlines = [JobRoleSkillInline]


# ============================================
# JOB ROLE SKILL ADMIN
# ============================================

@admin.register(JobRoleSkill)
class JobRoleSkillAdmin(admin.ModelAdmin):
    """Customize how JobRoleSkill appears in admin"""
    
    list_display = ('job_role', 'skill', 'proficiency_level', 'is_mandatory')
    list_filter = ('job_role', 'proficiency_level', 'is_mandatory')
    search_fields = ('job_role__title', 'skill__name')


# ============================================
# STUDENT SKILL ADMIN
# ============================================

@admin.register(StudentSkill)
class StudentSkillAdmin(admin.ModelAdmin):
    """Customize how StudentSkill appears in admin"""
    
    list_display = ('student', 'skill', 'proficiency_level', 'verified', 'added_on')
    list_filter = ('proficiency_level', 'verified', 'added_on')
    search_fields = ('student__user__username', 'skill__name')
    readonly_fields = ('added_on',)


# ============================================
# LEARNING RESOURCE ADMIN
# ============================================

@admin.register(LearningResource)
class LearningResourceAdmin(admin.ModelAdmin):
    """Customize how LearningResource appears in admin"""
    
    list_display = ('title', 'skill', 'resource_type', 'is_free', 'estimated_hours')
    list_filter = ('skill', 'resource_type', 'is_free', 'difficulty_level')
    search_fields = ('title', 'skill__name', 'url')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('General', {
            'fields': ('skill', 'title', 'resource_type')
        }),
        ('Details', {
            'fields': ('url', 'description', 'difficulty_level')
        }),
        ('Metadata', {
            'fields': ('estimated_hours', 'is_free', 'created_at')
        }),
    )


# ============================================
# SKILL GAP ANALYSIS ADMIN
# ============================================

@admin.register(SkillGapAnalysis)
class SkillGapAnalysisAdmin(admin.ModelAdmin):
    """Track student analyses history"""
    
    list_display = ('student', 'job_role', 'placement_readiness_percentage', 'analyzed_on')
    list_filter = ('job_role', 'analyzed_on')
    search_fields = ('student__user__username', 'job_role__title')
    readonly_fields = ('analyzed_on', 'skills_matched', 'total_required_skills', 'placement_readiness_percentage')


# ============================================
# ADMIN SITE CUSTOMIZATION
# ============================================

admin.site.site_header = "Skill Gap Analyzer - Admin Panel"
admin.site.site_title = "SGA Admin"
admin.site.index_title = "Welcome to Admin Dashboard"

"""
HOW TO USE DJANGO ADMIN:

1. Access admin at: http://localhost:8000/admin/
2. Login with superuser credentials

3. Create sample data:
   - Companies (TCS, Infosys, Wipro, etc.)
   - Skills (Python, Django, MySQL, etc.)
   - Job Roles (Junior Dev, Senior Dev, etc.)
   - Job Role Requirements (which skills needed)
   - Learning Resources (links to courses)

4. Add demo data for testing:
   - Create test companies
   - Create job roles
   - Assign skills to roles
   - Create learning resources

5. Features:
   - Search by any field
   - Filter by category/difficulty/etc.
   - Bulk actions
   - Export data

VIVA QUESTION:
Q: Why use Django Admin?
A: It provides CRUD operations out-of-the-box, saves development time,
   is secure, and allows non-technical users to manage data.
"""

"""
SKILLS_ANALYZER.PY - Core Skill Gap Analysis Engine
===================================================

This module contains the SkillGapAnalyzer class which is the
HEART of the project. It implements the business logic that:

1. Compares student skills with job requirements
2. Identifies skill gaps
3. Calculates placement readiness
4. Generates recommendations

This is placement-ready, interview-ready code!
"""

from .models import StudentSkill, JobRoleSkill


class SkillGapAnalyzer:
    """
    Core class for skill gap analysis.
    
    Responsibilities:
    - Compare student skills with role requirements
    - Calculate matching and gap metrics
    - Generate actionable recommendations
    - Determine placement readiness
    
    Usage:
        analyzer = SkillGapAnalyzer(student_profile, job_role)
        result = analyzer.analyze()
        print(f"Placement Readiness: {result['placement_readiness']}%")
    """
    
    def __init__(self, student_profile, job_role):
        """
        Initialize analyzer with student and job role.
        
        Args:
            student_profile: StudentProfile instance
            job_role: JobRole instance
        """
        self.student = student_profile
        self.job_role = job_role
        
        # Prefetch data for performance
        self.student_skills = self._get_student_skills()
        self.required_skills = self._get_required_skills()
    
    
    def _get_student_skills(self):
        """
        Fetch student's current skills.
        
        Returns:
            dict: {skill_id: {'name': str, 'proficiency': str, 'skill_obj': Skill}}
        """
        student_skills = {}
        
        # Query database for student's skills
        skill_records = StudentSkill.objects.filter(
            student=self.student
        ).select_related('skill')
        
        for record in skill_records:
            student_skills[record.skill.id] = {
                'name': record.skill.name,
                'proficiency': record.proficiency_level,
                'skill_obj': record.skill,
                'verified': record.verified
            }
        
        return student_skills
    
    
    def _get_required_skills(self):
        """
        Fetch required skills for the job role.
        
        Returns:
            dict: {skill_id: {'name': str, 'proficiency': str, 'mandatory': bool, 'skill_obj': Skill}}
        """
        required_skills = {}
        
        # Query database for role's required skills
        role_skills = JobRoleSkill.objects.filter(
            job_role=self.job_role
        ).select_related('skill')
        
        for record in role_skills:
            required_skills[record.skill.id] = {
                'name': record.skill.name,
                'proficiency': record.proficiency_level,
                'mandatory': record.is_mandatory,
                'skill_obj': record.skill
            }
        
        return required_skills
    
    
    def _compare_proficiency(self, student_level, required_level):
        """
        Compare if student's proficiency meets requirement.
        
        Proficiency hierarchy: Basic < Intermediate < Expert
        
        Args:
            student_level: str ('Basic', 'Intermediate', 'Expert')
            required_level: str ('Basic', 'Intermediate', 'Expert')
        
        Returns:
            bool: True if student proficiency >= required proficiency
        
        Logic:
            If role needs Intermediate and student has Expert → OK (overskilled)
            If role needs Intermediate and student has Intermediate → OK
            If role needs Intermediate and student has Basic → NOT OK
        """
        # Define proficiency levels with numeric values
        proficiency_levels = {
            'Basic': 1,
            'Intermediate': 2,
            'Expert': 3
        }
        
        student_value = proficiency_levels.get(student_level, 0)
        required_value = proficiency_levels.get(required_level, 0)
        
        return student_value >= required_value
    
    
    def analyze(self):
        """
        Main analysis method - combines all logic.
        
        Returns:
            dict: Comprehensive analysis result with:
                - matched_skills: List of skills student has
                - skill_gaps: List of missing skills with recommendations
                - extra_skills: Skills student has but role doesn't need
                - placement_readiness: Score from 0-100
                - risk_level: 'HIGH', 'MEDIUM', or 'LOW'
                - summary: Human-readable summary
        """
        
        matched_skills = []
        skill_gaps = []
        extra_skills = []
        partial_matches = []  # Student has skill but wrong proficiency
        
        # ========== STEP 1: Identify Matched Skills ==========
        for skill_id, required_info in self.required_skills.items():
            if skill_id in self.student_skills:
                student_info = self.student_skills[skill_id]
                
                # Check proficiency level
                if self._compare_proficiency(
                    student_info['proficiency'],
                    required_info['proficiency']
                ):
                    # Full match
                    matched_skills.append({
                        'skill': required_info['skill_obj'],
                        'student_proficiency': student_info['proficiency'],
                        'required_proficiency': required_info['proficiency'],
                        'is_verified': student_info['verified'],
                        'status': 'MATCHED'
                    })
                else:
                    # Partial match (skill exists but proficiency is low)
                    partial_matches.append({
                        'skill': required_info['skill_obj'],
                        'student_proficiency': student_info['proficiency'],
                        'required_proficiency': required_info['proficiency'],
                        'gap_type': 'PROFICIENCY_GAP',
                        'recommendation': f"Upgrade {required_info['skill_obj'].name} from {student_info['proficiency']} to {required_info['proficiency']}"
                    })
            else:
                # Complete gap - skill not found
                skill_gaps.append({
                    'skill': required_info['skill_obj'],
                    'proficiency_needed': required_info['proficiency'],
                    'is_mandatory': required_info['mandatory'],
                    'gap_type': 'NEW_SKILL',
                    'recommendation': f"Learn {required_info['skill_obj'].name} from scratch"
                })
        
        # ========== STEP 2: Identify Extra Skills ==========
        for skill_id, student_info in self.student_skills.items():
            if skill_id not in self.required_skills:
                extra_skills.append({
                    'skill': student_info['skill_obj'],
                    'student_proficiency': student_info['proficiency'],
                    'status': 'EXTRA'
                })
        
        # ========== STEP 3: Calculate Placement Readiness ==========
        
        total_required = len(self.required_skills)
        matched_count = len(matched_skills)
        
        if total_required > 0:
            # Formula: (Matched Skills / Total Required Skills) × 100
            placement_readiness = (matched_count / total_required) * 100
        else:
            placement_readiness = 100.0
        
        # ========== STEP 4: Determine Risk Level ==========
        
        if placement_readiness >= 80:
            risk_level = 'LOW'
            risk_description = "✅ EXCELLENT - Very good placement chances!"
        elif placement_readiness >= 60:
            risk_level = 'MEDIUM'
            risk_description = "⚠️ FAIR - Needs some upskilling for better chances"
        elif placement_readiness >= 40:
            risk_level = 'HIGH'
            risk_description = "❌ POOR - Significant upskilling required"
        else:
            risk_level = 'CRITICAL'
            risk_description = "🔴 CRITICAL - Major skill gaps, start learning immediately"
        
        # ========== STEP 5: Generate Summary & Recommendations ==========
        
        recommendations = []
        
        # Priority 1: Mandatory gaps
        mandatory_gaps = [g for g in skill_gaps if g['is_mandatory']]
        if mandatory_gaps:
            recommendations.append({
                'priority': 1,
                'title': f"CRITICAL: Learn {len(mandatory_gaps)} Mandatory Skills",
                'description': "These are must-have skills for this role",
                'skills': mandatory_gaps
            })
        
        # Priority 2: Optional gaps
        optional_gaps = [g for g in skill_gaps if not g['is_mandatory']]
        if optional_gaps:
            recommendations.append({
                'priority': 2,
                'title': f"IMPORTANT: Learn {len(optional_gaps)} Nice-to-Have Skills",
                'description': "These will boost your chances",
                'skills': optional_gaps
            })
        
        # Priority 3: Proficiency improvements
        if partial_matches:
            recommendations.append({
                'priority': 3,
                'title': f"IMPROVE: Strengthen {len(partial_matches)} Skills",
                'description': "You have these skills but need to improve proficiency",
                'skills': partial_matches
            })
        
        # ========== STEP 6: Compile Result Object ==========
        
        result = {
            'job_role': self.job_role,
            'company': self.job_role.company,
            'student': self.student,
            
            # Metrics
            'matched_count': matched_count,
            'total_required': total_required,
            'gap_count': len(skill_gaps),
            'partial_match_count': len(partial_matches),
            'extra_skills_count': len(extra_skills),
            
            # Score
            'placement_readiness': round(placement_readiness, 2),
            'risk_level': risk_level,
            'risk_description': risk_description,
            
            # Details
            'matched_skills': matched_skills,
            'skill_gaps': skill_gaps,
            'partial_matches': partial_matches,
            'extra_skills': extra_skills,
            
            # Recommendations
            'recommendations': recommendations,
            
            # Additional info
            'analysis_summary': self._generate_summary(
                matched_count, total_required, len(skill_gaps)
            )
        }
        
        return result
    
    
    def _generate_summary(self, matched, total, gaps):
        """
        Generate human-readable summary of analysis.
        
        Args:
            matched (int): Number of matched skills
            total (int): Total required skills
            gaps (int): Number of gaps
        
        Returns:
            str: Summary text for display in report
        """
        if total == 0:
            return "No skills required for this role."
        
        summary = f"""
        You have {matched} out of {total} required skills ({(matched/total)*100:.0f}% match).
        You need to learn {gaps} new skills to be fully prepared for this role.
        """
        
        return summary.strip()
    
    
    def get_learning_roadmap(self):
        """
        Generate a week-by-week learning plan.
        
        Useful for: Showing students a realistic timeline for upskilling
        
        Returns:
            list: Weekly learning schedule
        """
        analysis = self.analyze()
        skill_gaps = analysis['skill_gaps']
        
        # Sort by mandatory first, then by difficulty
        sorted_gaps = sorted(
            skill_gaps,
            key=lambda x: (not x['is_mandatory'], x['skill'].difficulty_level)
        )
        
        roadmap = []
        weeks_needed = (len(sorted_gaps) + 1) // 2  # 2 skills per week
        
        for week, i in enumerate(range(0, len(sorted_gaps), 2), 1):
            week_skills = sorted_gaps[i:i+2]
            roadmap.append({
                'week': week,
                'skills': week_skills,
                'estimated_hours': sum(
                    r.objects.filter(skill=s['skill']).aggregate(
                        total=models.Sum('estimated_hours')
                    )['total'] or 0
                    for s in week_skills
                )
            })
        
        return {
            'total_weeks': weeks_needed,
            'roadmap': roadmap,
            'message': f"Complete upskilling possible in approximately {weeks_needed} weeks!"
        }


# ============================================================================
# EXAMPLE USAGE (For Testing)
# ============================================================================

"""
Example of how to use SkillGapAnalyzer:

from analyzer.models import StudentProfile, JobRole
from analyzer.skills_analyzer import SkillGapAnalyzer

# Get student and role
student = StudentProfile.objects.get(user__username='rahul')
role = JobRole.objects.get(title='Junior Python Developer')

# Create analyzer
analyzer = SkillGapAnalyzer(student, role)

# Run analysis
result = analyzer.analyze()

# Access results
print(f"Placement Readiness: {result['placement_readiness']}%")
print(f"Risk Level: {result['risk_level']}")
print(f"Matched Skills: {result['matched_count']}/{result['total_required']}")
print(f"Skill Gaps: {result['gap_count']}")

# Get learning roadmap
roadmap = analyzer.get_learning_roadmap()
print(f"Learn in {roadmap['total_weeks']} weeks")
"""

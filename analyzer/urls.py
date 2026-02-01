"""
URLS.PY - URL Routing Configuration
====================================

This file maps URLs to view functions.

URL Routing explains:
- How Django handles incoming URLs
- How URLs map to views
- URL naming for templates ({% url 'view_name' %})

Example:
URL: http://localhost:8000/register/
Maps to: register view function

URL Pattern: path('register/', views.register, name='register')
"""

from django.urls import path
from . import views

# App namespace (helps organize URLs when multiple apps exist)
app_name = 'analyzer'

urlpatterns = [
    # Home page
    path('', views.home, name='home'),
    
    # ============ AUTHENTICATION URLS ============
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # ============ MAIN APPLICATION URLS ============
    path('dashboard/', views.dashboard, name='dashboard'),
    path('select-role/', views.select_role, name='select_role'),
    path('analyze-gap/', views.analyze_gap, name='analyze_gap'),
    
    # ============ PROFILE & HISTORY URLS ============
    path('profile/', views.profile_view, name='profile'),
    path('skill-history/', views.skill_history, name='skill_history'),
    
    # ============ API ENDPOINTS (Optional) ============
    path('api/role-skills/<int:role_id>/', views.get_role_skills_ajax, name='get_role_skills'),
]

"""
URL EXPLANATION FOR VIVA:

1. URL PATTERN STRUCTURE:
   path('route/', view_function, name='url_name')
   
   Example:
   path('register/', views.register, name='register')
   
   - 'register/' = URL path (what user types)
   - views.register = Function to execute
   - name='register' = Used in templates as {% url 'register' %}

2. URL FLOW:
   User visits → http://localhost:8000/register/
   Django checks urlpatterns (top to bottom)
   Finds matching pattern
   Calls corresponding view function
   View renders response (HTML/data)
   Browser displays page

3. NAMED URLS (Why we use 'name' parameter):
   Instead of hardcoding paths in templates:
   ❌ <a href="/register/"> - brittle, breaks if path changes
   ✅ <a href="{% url 'register' %}"> - flexible, auto-updates
   
   If we change path from 'register/' to 'user-registration/',
   All templates automatically update!

4. APP_NAME NAMESPACE:
   When multiple apps exist, namespace prevents conflicts:
   - analyzer/urls.py: app_name = 'analyzer'
   - Use in templates: {% url 'analyzer:register' %}
   
5. URL PARAMETERS (Dynamic URLs):
   path('analyze-gap/<int:role_id>/', views.analyze_gap)
   
   Captures role_id from URL and passes to view:
   http://localhost:8000/analyze-gap/5/
   → view receives role_id=5

6. HTTP METHODS:
   Same URL can handle GET and POST:
   - GET: Display form
   - POST: Process form submission
   
   Example (register view):
   if request.method == 'POST':
       # Process form
   else:
       # Show form

7. URL VS VIEW:
   URL = Route mapping
   View = Business logic
   
   They work together:
   URL routes incoming request → View handles logic → View returns response
"""

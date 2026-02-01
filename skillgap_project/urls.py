"""
SKILLGAP_PROJECT/URLS.PY - Main Project URL Configuration
=========================================================

This is the MAIN URL router for the entire Django project.
It includes URLs from individual apps (like analyzer app).

Think of it as: Main Router → includes App Routers
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django Admin Panel
    path('admin/', admin.site.urls),
    
    # Include analyzer app URLs
    # This means all URLs in analyzer/urls.py are included here
    # Example: analyzer/urls.py has path('register/', ...)
    # Final URL becomes: http://localhost:8000/register/
    path('', include('analyzer.urls')),
]

"""
URL STRUCTURE EXPLANATION:

Project Level (this file):
├── admin/ → Django Admin
└── '' → Includes analyzer app URLs

App Level (analyzer/urls.py):
├── register/ → register view
├── login/ → login view
├── dashboard/ → dashboard view
└── ... (more URLs)

FLOW:
User visits: http://localhost:8000/register/
↓
Django checks urlpatterns in skillgap_project/urls.py
↓
Finds: path('', include('analyzer.urls'))
↓
Includes all URLs from analyzer/urls.py
↓
Finds matching: path('register/', views.register)
↓
Calls: views.register(request)
↓
Renders: analyzer/register.html
"""

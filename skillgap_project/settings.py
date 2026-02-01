"""
SETTINGS.PY - Django Configuration
===================================

This file configures:
- Database settings
- Installed apps
- Authentication
- Static files
- Security settings
"""

from pathlib import Path
import os

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================
# SECURITY SETTINGS
# ============================================

# Change this to your actual secret key for production
SECRET_KEY = 'django-insecure-your-secret-key-change-this-for-production-12345'

# DEBUG: Set to False in production
DEBUG = True

# ALLOWED_HOSTS: Add domains that can access this site
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '*']  # For development only

# ============================================
# INSTALLED APPS
# ============================================

INSTALLED_APPS = [
    # Django built-in apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Our app
    'analyzer.apps.AnalyzerConfig',
]

# ============================================
# MIDDLEWARE
# ============================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ============================================
# URL CONFIGURATION
# ============================================

ROOT_URLCONF = 'skillgap_project.urls'

# ============================================
# TEMPLATES
# ============================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'analyzer', 'templates')],  # Look for templates here
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ============================================
# WSGI APPLICATION
# ============================================

WSGI_APPLICATION = 'skillgap_project.wsgi.application'

# ============================================
# DATABASE CONFIGURATION
# ============================================

# Using SQLite (default for development)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

"""
Why SQLite for this project?
✅ Zero setup - file-based database
✅ Perfect for learning and small projects
✅ Easy to backup (just copy db.sqlite3)
✅ No server needed

For production, use PostgreSQL or MySQL:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'skillgap_db',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
"""

# ============================================
# PASSWORD VALIDATION
# ============================================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,  # Minimum 8 characters
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ============================================
# INTERNATIONALIZATION
# ============================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ============================================
# STATIC FILES (CSS, JS, Images)
# ============================================

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Look for static files in analyzer app
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'analyzer', 'static'),
]

# ============================================
# MEDIA FILES (User Uploads)
# ============================================

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ============================================
# DEFAULT PRIMARY KEY TYPE
# ============================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============================================
# AUTHENTICATION
# ============================================

# Login URL (where unauthenticated users are redirected)
LOGIN_URL = 'analyzer:login'
LOGIN_REDIRECT_URL = 'analyzer:dashboard'

# ============================================
# LOGGING CONFIGURATION (Optional)
# ============================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

# ============================================
# SESSION CONFIGURATION
# ============================================

SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Store sessions in database
SESSION_COOKIE_AGE = 1209600  # 2 weeks
SESSION_COOKIE_SECURE = False  # Set True in production with HTTPS
SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access

# ============================================
# CSRF CONFIGURATION
# ============================================

CSRF_COOKIE_SECURE = False  # Set True in production with HTTPS
CSRF_COOKIE_HTTPONLY = True

# ============================================
# PRODUCTION CHECKLIST
# ============================================

"""
Before deploying to production:

1. Set DEBUG = False
2. Set ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
3. Use a strong SECRET_KEY
4. Use PostgreSQL or MySQL instead of SQLite
5. Set CSRF_COOKIE_SECURE = True
6. Set SESSION_COOKIE_SECURE = True
7. Use environment variables for sensitive data
8. Set up HTTPS/SSL
9. Run: python manage.py collectstatic
10. Use a production WSGI server (Gunicorn, uWSGI)

For deployment, use settings like:
export DEBUG=False
export SECRET_KEY='your-production-secret-key'
export ALLOWED_HOSTS='yourdomain.com'
"""

"""


For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# from local import *
import os
from scipy2017.local import *
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'w81ia+6)sak!)t@kv=@x267y78ceh4iu2c@o@2#8+h$kua3e9a'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
#DEBUG = False

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['localhost', 'scipy.in', 'www.scipy.in']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'website',
    'social.apps.django_app.default',
    'widget_tweaks',
    'crispy_forms',
    'floppyforms',
    'captcha',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
   'django.contrib.auth.context_processors.auth',
   'django.core.context_processors.debug',
   'django.core.context_processors.i18n',
   'django.core.context_processors.media',
   'django.core.context_processors.static',
   'django.core.context_processors.tz',
   'django.contrib.messages.context_processors.messages',
   'social.apps.django_app.context_processors.backends',
   'social.apps.django_app.context_processors.login_redirect',
   # 'website.context_processors.contact_us_context_processor'

)

AUTHENTICATION_BACKENDS = (
   'social.backends.facebook.FacebookOAuth2',
   'social.backends.google.GoogleOAuth2',
   'social.backends.twitter.TwitterOAuth',
   'social.backends.github.GithubOAuth2',
   'django.contrib.auth.backends.ModelBackend',
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,  '../website/templates'),
)

STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, '../website/static'),
)

ROOT_URLCONF = 'scipy2017.urls'

URL_ROOT = '/'

WSGI_APPLICATION = 'scipy2017.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': DBNAME,                      # Or path to database file if using sqlite3.
        'USER': DBUSER,
        'PASSWORD': DBPWD,
        'HOST': '127.0.0.1',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '3306',
    }
}

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = GOOGLE_KEY
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = GOOGLE_SECRET
# API key AIzaSyDxRqGfJNJJIFw6traKTG5nC1mY8TNODu4 

SOCIAL_AUTH_GOOGLE_OAUTH2_USE_DEPRECATED_API = True
SOCIAL_AUTH_GOOGLE_PLUS_USE_DEPRECATED_API = True


SOCIAL_AUTH_FACEBOOK_KEY = FACEBOOK_KEY
SOCIAL_AUTH_FACEBOOK_SECRET = FACEBOOK_SECRET
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'id,name,email', 
}


LOCAL_SOCIAL_AUTH_GITHUB_KEY = GITHUB_KEY
LOCAL_SOCIAL_AUTH_GITHUB_SECRET = GITHUB_SECRET

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

RECAPTCHA_PUBLIC_KEY = RECAPTCHA_PUBLIC
RECAPTCHA_PRIVATE_KEY = RECAPTCHA_PRIVATE


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Calcutta'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')
MEDIA_URL = "/downloads/"
LOGIN_URL = '/2017/accounts/login/'
LOGIN_REDIRECT_URL = '/2017/cfp'


ADMINS = SYSADMINS
SERVER_EMAIL = SYS_SERVER_EMAIL


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# Host for sending e-mail.
EMAIL_HOST = EMAIL_HOST_SERVER

# Port for sending e-mail.
EMAIL_PORT = EMAIL_PORT_SERVER

# Optional SMTP authentication information for EMAIL_HOST.
EMAIL_HOST_USER = EMAIL_HOST_USER_SERVER
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD_SERVER
EMAIL_USE_TLS = EMAIL_USE_TLS_SERVER


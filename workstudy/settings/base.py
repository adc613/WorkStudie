
"""
Django settings for workstudy project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import sys
if 'test' in sys.argv or 'test_coverage' in sys.argv:
    from .test_settings import DATABASES
else:
    from .normal_settings import DATABASES


from django.core.urlresolvers import reverse
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
FIXTURE_DIRS = (
   os.path.join(BASE_DIR, 'Test_Case_Fixtures'),
)



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'cqum+f%ac)9dq@*$50y+j4#33zao*14b5h-+ar0!n7ge9480p1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

ADMINS = (
    ('Adam Collins', 'adc82@case.edu'),
)

AUTH_USER_MODEL = 'users.User'
# Application definition

DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

THIRD_PARTY_APPS = (
    #'south',
    #'debug_toolbar',
    'braintree',
)

LOCAL_APPS = (
    'tasks',
    'users',
    'checkout'
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'workstudy.urls'

WSGI_APPLICATION = 'workstudy.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Chicago'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

MEDIA_ROOT = os.path.join(BASE_DIR, 'static', 'media')

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static', 'static-only')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static','static'),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

LOGIN_URL = '/account/login'

EMAIL_HOST = 'smtp.gmail.com'

EMAIL_HOST_USER = 'workstudie@gmail.com'

EMAIL_HOST_PASSWORD = 'Case10is'
 
EMAIL_PORT = 587

EMAIL_USE_TLS = True

BRAINTREE_MERCHANT_ID = "bhfgybf7d8vtqn55"

BRAINTREE_PUBLIC_KEY = "ym2c9nswtdtkzbfs"

BRAINTREE_PRIVATE_KET = "7391420db569e604b2fed4d5b742d891"

import braintree
braintree.Configuration.configure(braintree.Environment.Sandbox,
                                  merchant_id=BRAINTREE_MERCHANT_ID,
                                  public_key=BRAINTREE_PUBLIC_KEY,
                                  private_key=BRAINTREE_PRIVATE_KET)



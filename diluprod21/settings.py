"""
Django settings for diluprod21 project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret! ---------------------cambios para produccion-------------------------
# SECRET_KEY = ')6nu)feg%5==x_5-64u3s_x(#m)&!*m-)cbsqzylif4y(sc^22'
import os
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', ')6nu)feg%5==x_5-64u3s_x(#m)&!*m-)cbsqzylif4y(sc^22')

# SECURITY WARNING: don't run with debug turned on in production! ---------------------cambios para produccion-------------------------
# DEBUG = True
DEBUG = bool( os.environ.get('DJANGO_DEBUG', True) )

ALLOWED_HOSTS = ['diluprod21.herokuapp.com','127.0.0.1','localhost']


# Application definition

INSTALLED_APPS = [
    'Basic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'import_export',
]
# adicion de 'whitenoise.middleware.WhiteNoiseMiddleware'---------------------cambios para produccion-------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'diluprod21.urls'

# MEDIA_ROOT = BASE_DIR / 'media'

# MEDIA_URL = '/media/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'diluprod21.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DATABASE_NAME','diluprod21db'),
        'USER': os.environ.get('DATABASE_USER','root'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD','Controwell.2020'),
        'HOST': os.environ.get('DATABASE_HOST','localhost'),
        'PORT': os.environ.get('DATABASE_PORT','3310'),
    }
}

AUTH_USER_MODEL = 'Basic.User'

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

# para la libreria import-export
IMPORT_EXPORT_USE_TRANSACTIONS = True

# Heroku: Update database configuration from $DATABASE_URL.---------------------cambios para produccion-------------------------
import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

# The absolute path to the directory where collectstatic will collect static files for deployment.---------------------cambios para produccion-------------------------
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Simplified static file serving.---------------------cambios para produccion-------------------------
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# resolver el problema de serializar objetos que no son json
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_ACCEPT_CONTENT = ['pickle']

# usar broker de rediss heroku, para el cual se utiliza la REDIS_TLS_URL en las config vars, si no quiero usar redis quitar linea e instalar rabbit MQ en el equipo donde corre celery
CELERY_BROKER_URL=os.environ.get('REDIS_TLS_URL','rediss://:p9287001193ee93f6b150df968e319f40c88de7d19f5e4654651f9d8dd510411c@ec2-52-22-1-220.compute-1.amazonaws.com:30040')
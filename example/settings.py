"""
Django settings for example project.

Generated by 'django-admin startproject' using Django 1.9.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import logging
import redis

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'c&lj)dr!*lvu5fwefwgrr_$p4#qq5ssix_16q*(e&os'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'example.urls'

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

WSGI_APPLICATION = 'example.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

FB_HUB_CHALLENGE = '164646513asd4849849'
FB_PAGE_TOKEN = 'EAAaHHoZAbazQBAHg83H3eulRnZBn64iYX0ffQqQGdL4toiafN4ChJZAResNMV4iaF3YXUFZCpYH3m89UXIlZBdi3odB04jtrhbqcxlDm3bYytqnO1pCZC3UE6hfQ2bmS2Eg1ADt0nwR5vHdpP2wfnnwZB4f5BFL4LAtIPsRey3KUAZDZD'
FACEBOOK_APP_ID = '1837415033170740'

#     'default': {
REDIS_CONF = {
    'PASSWORD' : None,
    'HOST' : 'localhost',
    'PORT' : '6379'
}

def get_logger(uid):
    global CHAT_LOG_DIR
    logger = logging.getLogger('conversation_'+uid)
    if not len(logger.handlers):
        logger.setLevel(logging.INFO)
        consoleHandler = logging.StreamHandler()
        logFormatter = logging.Formatter("["+uid+"][%(levelname)s] %(message)s")
        consoleHandler.setFormatter(logFormatter)
        logger.addHandler(consoleHandler)
    return logger

REDIS_DB = None
def get_key_value_store():
    global REDIS_DB
    if not REDIS_DB:
        try:
            REDIS_DB = redis.StrictRedis(host=REDIS_CONF['HOST'], port=REDIS_CONF['PORT'], password=REDIS_CONF['PASSWORD'], db=0)
            REDIS_DB.set('check','testing connection...')
        except Exception:
            print('----------------------------------------------------------')
            print('!!! Exception: Unable to connect to Redis')
            print('!!! Make sure it is running on %s:%s' % (REDIS_CONF['HOST'],REDIS_CONF['PORT']))
            print('----------------------------------------------------------')
            return None
    return REDIS_DB

DIALOG_CONFIG = {
    'WIT_TOKEN': '5WOK5P6QCDO2GVKQJ6L4DQFVPLOYUGUU',
    'CHATBOT_MODULE' : 'example.chatbot',
    'GET_LOGGER' : get_logger,
    'GET_STORAGE' : get_key_value_store,
    'FB_PAGE_TOKEN' : FB_PAGE_TOKEN
}
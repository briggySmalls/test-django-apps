"""
Django settings for mysite project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%zhnjj*0lr7@4%p1y8iq=r^&l@$uebtd8))#z^6n4*g&tycb3#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'grappelli',
    #'filebrowser',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ckeditor',  # WYSIWYG editor (enables RichTextField)
    'colorfield',  # enables ColorField (TO DO: doesn't work with grappelli)
    'homepage',  # SJB: app for fullPage pages
    'container',  # SJB: generic (tabbed) content container
    'zineapp',  # SJB: app for uploading and displaying zines
    'articles',  # SJB: app for recording rich text articles
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'mysite.urls'

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'GB'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

# for serving static files to grappelli/filebrowser
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# for grappelli
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
)

# MEDIA SETTINGS (also used by filebrowser)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # store media on server at /media
MEDIA_URL = '/media/'  # media at MEDIA_ROOT hosted at MEDIA_URL

# FILEBROWSER SETTINGS
FILEBROWSER_DIRECTORY = ''  # browse from MEDIA_URL
FILEBROWSER_OVERWRITE_EXISTING = True  # TO DO: doublecheck this
FILEBROWSWER_EXTENSIONS = {
    'Folder': [''],
    'Image': ['.jpg','.jpeg','.gif','.png','.tif','.tiff'],
    'Document': ['.pdf'],
    'Video': [''],
    'Audio': ['']
}  # allow these uploads TO DO: anything other than pdf necessary?

# CKEDITOR SETTINGS
CKEDITOR_UPLOAD_PATH = "ckeitor-uploads/"  # within MEDIA_ROOT/MEDIA_URL
CKEDITOR_IMAGE_BACKEND = "Pillow"
CKEDITOR_JQUERY_URL = "/static/homepage/js/jquery-1.10.2.min.js"

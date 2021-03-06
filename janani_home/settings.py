import os

import dj_database_url
from decouple import config, Csv

# General app config
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEBUG = config('DEBUG', default=False, cast=bool)
GOOGLE_ANALYTICS_ID = config('GOOGLE_ANALYTICS_ID', default='')
GOOGLE_SITE_VERIFICATION = config('GOOGLE_SITE_VERIFICATION', default='')
PASSWORD_RESET_TIMEOUT_DAYS = 4
PHONE_NUMBER = config('PHONE_NUMBER', default='')
SECRET_KEY = config('SECRET_KEY')
SERVER_EMAIL = config('SERVER_EMAIL', default='root@localhost')
SESSION_COOKIE_AGE = 60 * 30
SITE_ID = 1
INTERNAL_IPS = '127.0.0.1'

# Database
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL'),
        conn_max_age=500,
    )
}

# Email backend
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_USE_TLS = True
    EMAIL_HOST = config('EMAIL_HOST')
    EMAIL_HOST_USER = config('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
    EMAIL_PORT = 587

# Application definition
INSTALLED_APPS = [
    'events.apps.EventsConfig',
    'accounts.apps.AccountConfig',
    'announcements.apps.AnnouncementsConfig',
    'cms.apps.CmsConfig',
    'comment.apps.CommentConfig',
    'educational_need.apps.EducationalneedConfig',
    'superadmin.apps.SuperadminConfig',
    'volunteers.apps.VolunteersConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'smart_selects',
    'widget_tweaks',
    'easy_thumbnails',
    'ckeditor',
    'ckeditor_uploader',
    'storages',
    'django_user_agents',
    #'debug_toolbar',
]

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

USER_AGENTS_CACHE = 'default'

MIDDLEWARE = [
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
]

ROOT_URLCONF = 'janani_home.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cms.context_processors.menu_processor',
                'janani_home.context_processors.config_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'janani_home.wsgi.application'

# Password validation
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

# Authentication backend
AUTHENTICATION_BACKENDS = ('accounts.backends.CustomModelBackend', )

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAdminUser'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100
}

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Serving static files in development
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'staticfiles'),
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# S3 Media Storage

if not DEBUG:
    AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
    AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
    DEFAULT_FILE_STORAGE = 'janani_home.storage_backends.MediaStorage'
    THUMBNAIL_DEFAULT_STORAGE = DEFAULT_FILE_STORAGE  # easy_thumbnails
    MEDIAFILES_LOCATION = 'media'
    MEDIA_URL = 'https://%s.s3.amazonaws.com/%s/' % (AWS_STORAGE_BUCKET_NAME,
                                                     MEDIAFILES_LOCATION)
    AWS_QUERYSTRING_AUTH = False

# Avatars
THUMBNAIL_ALIASES = {
    '': {
        'avatar50': {'size': (50, 50), 'crop': True},
        'avatar70': {'size': (70, 70), 'crop': True},
        'avatar150': {'size': (150, 150), 'crop': True},
        'avatar250': {'size': (250, 250), 'crop': True},
        'slide': {'size': (250, 300), 'crop': True},
        'gallery': {'size': (800, 800), 'crop': False},
    },
}

# Ckeditor
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js'
CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono',
        # 'skin': 'office2013',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_YourCustomToolbarConfig': [
            {'name': 'document', 'items': ['Maximize', '-',]},
            {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
            {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl']},
            {'name': 'insert',
             'items': ['Table', 'HorizontalRule', 'Smiley', 'SpecialChar',]},
            '/',
            {'name': 'styles', 'items': ['Styles', 'Format', 'Font']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'about', 'items': ['About']},
        ],
        'toolbar': 'YourCustomToolbarConfig',
        'height': 200,
        'width': '100%',
        'language': 'en',
        'tabSpaces': 4,
        'extraPlugins': ','.join([
            'uploadimage', # the upload image feature
            # your extra plugins here
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            # 'devtools',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath'
        ]),
    },
    'admin': {
        'toolbar': 'full',
        'height': 200,
        'width': '100%',
        'extraPlugins': ','.join([
            'uploadimage', # the upload image feature
            # your extra plugins here
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            # 'devtools',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath'
        ]),
    },
    'admin2': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Maximize', 'Format', 'Bold', 'Italic', 'Underline', '-', 'TextColor', 'BGColor'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink', 'Anchor', 'Image', 'Embed', '-'],
            ['Undo', 'Redo', 'Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo', 'Find', 'Replace', '-', 'SelectAll', '-', 'Source']
        ],
        'height': 400,
        'width': '100%',
        'extraPlugins': ','.join(
            [
                'image2',
                'embed',
            ]),
        'language': 'en',
    },
}

# App lockdown for staging
USE_LOCKDOWN = config('USE_LOCKDOWN', default=False)
if USE_LOCKDOWN:
    INSTALLED_APPS += ('lockdown',)
    MIDDLEWARE += ('lockdown.middleware.LockdownMiddleware',)
    LOCKDOWN_PASSWORDS = config('LOCKDOWN_PASSWORDS', default=False, cast=Csv())

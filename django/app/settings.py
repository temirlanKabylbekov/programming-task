import environ

root = environ.Path(__file__) - 1        # one folder back (/django/app/settings.py - 1 = /django)
env = environ.Env(DEBUG=(bool, False),)  # set default values and casting
environ.Env.read_env()                   # reading .env file

DEBUG = env('DEBUG')

SECRET_KEY = env('SECRET_KEY')

SITE_ROOT = root()

MEDIA_URL = env('MEDIA_URL')
MEDIA_ROOT = env('MEDIA_ROOT')
STATIC_URL = env('STATIC_URL')
STATIC_ROOT = env('STATIC_ROOT')

USE_L10N = True
USE_i18N = True
USE_TZ = True
FORMAT_MODULE_PATH = [
    'app.formats',
]
TIME_ZONE = env('TIME_ZONE')
LANGUAGE_CODE = env('LANGUAGE_CODE')
LOCALE_PATHS = ['locale']

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    'localhost:8080',
]
INTERNAL_IPS = [
    '127.0.0.1',
    '::1',
]

DATABASES = {
    'default': env.db_url(),
}
CONN_MAX_AGE = 300

CACHES = {
    'default': env.cache_url(),
}

TEST_RUNNER = 'app.test.disable_test_command_runner.DisableTestCommandRunner'

ROOT_URLCONF = 'app.urls'

WSGI_APPLICATION = 'app.wsgi.application'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

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

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'app.renderers.AppJSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissions',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 24,
    'TIME_FORMAT': '%H:%M',
}

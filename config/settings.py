import os

import environ


root = environ.Path(__file__) - 2
env = environ.Env()
environ.Env.read_env(env.str(root(), '.env'))

BASE_DIR = root()

SECRET_KEY = env.str('SECRET_KEY')
DEBUG = env.bool('DEBUG', False)
ALLOWED_HOSTS = env.str('ALLOWED_HOSTS', '').split(' ')

# Base packages
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# Additional packages
INSTALLED_APPS += [
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'django_filters',
    'corsheaders',
    'debug_toolbar',
]

# Apps
INSTALLED_APPS += [
    'api',
    'users',
    'storage',
    'common',
]

# After apps
INSTALLED_APPS += [
    'drf_spectacular',
]

AUTH_USER_MODEL = 'users.User'
AUTHENTICATION_BACKENDS = ('users.backends.AuthBackend', )

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# My middleware
MIDDLEWARE += [
    'common.middleware.LoggingMiddleware',
]

INTERNAL_IPS = [
    '127.0.0.1',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

################################
# DATABASE SETTINGS
################################
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env.str('PG_DATABASE', 'postgres'),
        'USER': env.str('PG_USER', 'postgres'),
        'PASSWORD': env.str('PG_PASSWORD', 'postgres'),
        'HOST': env.str('PG_HOST', 'localhost'),
        'PORT': env.int('PG_PORT', 5432),
    },
    'extra': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

################################
# DJANGO REST FRAMEWORK
################################
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PARSES_CLASSES': [
        'rest_framework.parses.JSONParses',
        'rest_framework.parses.FormParser',
        'rest_framework.parses.MultiPartParser',
        'rest_framework.parses.FileUploadParser',
    ],

    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    # 'DEFAULT_PAGINATION_CLASS': 'common.pagination.BasePagination',
    # 'EXCEPTION_HANDLER': 'common.exceptions.app_exception_handler'
}

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

################################
# LOGGER CONFIG
################################
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "filters": {
        "special": {
            "()": "project.logging.SpecialFilter",
            "foo": "bar",
        },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            "filters": ["special"],
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "propagate": True,
        },
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": False,
        },
        "myproject.custom": {
            "handlers": ["console", "mail_admins"],
            "level": "INFO",
            "filters": ["special"],
        },
    },
}


################################
# LOCALIZATION
################################
LANGUAGE_CODE = 'ru-Ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

################################
# CORS-HEADERS
################################
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = ['*']
CSRF_COOKIE_SECURE = False

################################
# STATIC & MEDIA
################################
STATIC_URL = env.str('STATIC_URL', 'static/')
STATIC_ROOT = os.path.join(BASE_DIR, STATIC_URL)
MEDIA_URL = env.str('MEDIA_URL', 'media/')
MEDIA_ROOT = os.path.join(BASE_DIR, MEDIA_URL)
FILE_STORAGE_URL = env.str('FILE_STORAGE_URL', 'fs/')
FILE_STORAGE_ROOT = os.path.join(BASE_DIR, FILE_STORAGE_URL)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

################################
# DRF SPECTACULAR SETTINGS
################################
SPECTACULAR_SETTINGS = {
    'TITLE': 'API-сервис файлового хранилища данных',
    'DESCRIPTION': 'Полное описание REST API доступа к сервису',
    'VERSION': '1.0.0',

    'SERVE_PERMISSIONS': [
        'rest_framework.permissions.IsAuthenticated',
    ],

    'SERVE_AUTHENTICATION': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],

    'SWAGGER_UI_SETTINGS': {
        'DeepLinking': True,
        'DisplayOperationId': True,
        'filter': False,
    },

    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SORT_OPERATIONS': False,

    'COMPONENTS': {
        'SCHEMAS': False,
    },

    'TITLES_TAGS': {
        'AUTH': 'Аутентификация и авторизация',
        'USER': 'Интерфейс пользователя',
        'ADMIN': 'Интерфейс администратора',
        'STORAGE': 'Файловое хранилище',
    },

    # 'TAGS': [
    #     {
    #         'name': 'STORAGE',
    #         'exclude': ['put'],
    #     }
    # ],
}

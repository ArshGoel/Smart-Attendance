import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-i+=&t()t7s+-0_p8sfm8mnky8g^oco983#_fp3*3ja!dh1(c9q"

DEBUG = True

ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = [
    'https://smart-attendance-1-q7ja.onrender.com'
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    #Added Manually
    "Accounts.apps.AccountsConfig",
    "Services.apps.ServicesConfig",
    'whitenoise.runserver_nostatic',

]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    #Added Manually
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = "Django_Final.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        'DIRS': [os.path.join(BASE_DIR,"templates")],   #Added Manually
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "Django_Final.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'smart_attendance',     # Replace with your Aiven database name
#         'USER': 'avnadmin',          # Replace with your Aiven database username
#         'PASSWORD': 'AVNS_ZBxpNZDSgH38UEicwgp',      # Replace with your Aiven database password
#         'HOST': 'url-shortner-arshgoel16-ba75.e.aivencloud.com',        # Replace with your Aiven database hostname
#         'PORT': '12743',        # Replace with your Aiven database port
#         'OPTIONS': {
#             'sslmode': 'require',         # Enforce SSL for Aiven connections
#         },
#     }
# }

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


#Added Manually

STATICFILES_DIRS = [os.path.join(BASE_DIR,"static")]
STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles_build',"static")

# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR,"static")
# ] 

MEDIA_URL = '/media/'
MEDIAFILES_DIRS = [
    os.path.join(BASE_DIR,"media")
] 
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
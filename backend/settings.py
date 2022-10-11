import os
from urllib.parse import quote

import environ


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_ROOT = os.path.dirname(os.path.dirname(__file__))

# Load env to get settings
env = environ.Env()

SECRET_KEY = env.str("SECRET_KEY", default="dummy-key")

DEBUG = env.bool("DJANGO_DEBUG", default=False)

ALLOWED_HOSTS = ["*"]
if not DEBUG:
    ALLOWED_HOSTS = ["localhost", env.str("HOST", default="127.0.0.1")]
    CSRF_TRUSTED_ORIGINS = ["https://" + env.str("HOST", default="127.0.0.1")]
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True

USE_TZ = True
TIME_ZONE = "Europe/Tallinn"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.contrib.modeladmin",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "modelcluster",
    "taggit",
    # Local apps
    "dashboard",
    "accounts",
    # Important to keep them as a last apps,
    # because we are overwriting some of the templates
    "wagtail.users",
    "wagtail.core",
    "wagtail.admin",
]

if DEBUG:
    INSTALLED_APPS += ["wagtail.contrib.styleguide"]

MIDDLEWARE = [
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
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

WSGI_APPLICATION = "wsgi.application"

DATABASES = {
    # When using DATABASE_URL, unsafe characters in the url should be encoded.
    # See: https://django-environ.readthedocs.io/en/latest/#using-unsafe-characters-in-urls
    "default": env.db_url(
        "DATABASE_URL",
        # pylint: disable-next=consider-using-f-string
        default="psql://{user}:{password}@{host}:{port}/{name}?sslmode={sslmode}".format(
            host=env.str("DATABASE_HOST", default="postgres"),
            port=env.int("DATABASE_PORT", default=5432),
            name=quote(env.str("DATABASE_NAME", default="projectdb")),
            user=quote(env.str("DATABASE_USER", default="dbuser")),
            password=quote(env.str("DATABASE_PASSWORD", default="dbpass")),
            sslmode=env.str("DATABASE_SSLMODE", default="disable"),
        ),
    )
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": ("django.contrib.auth.password_validation." "MinimumLengthValidator"),
    },
    {
        "NAME": ("django.contrib.auth.password_validation." "CommonPasswordValidator"),
    },
    {
        "NAME": ("django.contrib.auth.password_validation." "NumericPasswordValidator"),
    },
]
AUTH_USER_MODEL = "accounts.CustomUser"

LANGUAGE_CODE = "en-us"

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
STATICFILES_DIRS = (os.path.join(BASE_DIR, "app", "static"),)
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

DEFAULT_FROM_EMAIL = "Admins <admins@example.com>"
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_PORT = 1025
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""

EMAIL_HOST = env.str("EMAIL_HOST", default="localhost")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

WAGTAIL_SITE_NAME = "#TODO-OVERWRITE-ME"
WAGTAILSEARCH_BACKENDS = {"default": {"BACKEND": "wagtail.search.backends.database"}}
WAGTAIL_MODERATION_ENABLED = False
WAGTAIL_SLIM_SIDEBAR = True
WAGTAILADMIN_COMMENTS_ENABLED = False
WAGTAIL_ENABLE_UPDATE_CHECK = False
WAGTAIL_WORKFLOW_ENABLED = False

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
}

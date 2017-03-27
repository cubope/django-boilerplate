import django.conf.global_settings as DEFAULT_SETTINGS


SECRET_KEY = 'boilerplateattherescue'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}


INSTALLED_APPS = (
    # Default Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # We test this one
    'boilerplate',
)

MIDDLEWARE_CLASSES = DEFAULT_SETTINGS.MIDDLEWARE_CLASSES


MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'


TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            "django.contrib.auth.context_processors.auth",
            "django.template.context_processors.debug",
            "django.template.context_processors.i18n",
            "django.template.context_processors.media",
            "django.template.context_processors.static",
            "django.template.context_processors.tz",
            "django.contrib.messages.context_processors.messages"
        ]
    }
}]


ROOT_URLCONF = None

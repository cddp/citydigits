# import the stuff I actually change
from config import (backend, gis_backend,
        dbname, dbusername, pw,
        INSTALLED_APPS, SECRET_KEY,
        MEDIA_ROOT,
        MEDIA_URL,
        STATIC_ROOT,
        STATIC_URL,
        MIDDLEWARE_CLASSES,
        ROOT_URLCONF,
        TEMPLATE_DIRS,
        TEMPLATE_CONTEXT_PROCESSORS,
        site_name,
        )

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
        ('Benjamin Golder', 'benjamin.j.golder@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': gis_backend,
        'NAME': dbname,
        'USER': dbusername,
        'PASSWORD': pw,
        'HOST': '',
        'PORT': '',
    }
}

TIME_ZONE = None
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATICFILES_DIRS = (
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

WSGI_APPLICATION = site_name + '.wsgi.application'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


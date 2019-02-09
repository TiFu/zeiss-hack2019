from .settings import *  # noqa

INSTALLED_APPS += ['debug_toolbar']

MIDDLEWARE +=['debug_toolbar.middleware.DebugToolbarMiddleware']

ALLOWED_HOSTS = [
    "localhost",
    "0.0.0.0",
    "127.0.0.1",
]

DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': [
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ],
    'SHOW_TEMPLATE_CONTEXT': True,
}

# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#internal-ips
INTERNAL_IPS = ['127.0.0.1', 'localhost']

CORS_ORIGIN_ALLOW_ALL = True


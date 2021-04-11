# Overrides
from .settings import *  # noqa: F401
# secrets has to come after settings
try:
    from .secrets import *
except Exception: # file not found
    pass
import os

SECRET_KEY = 'lksdf98wrhkjs88dsf8-324ksdm'

DEBUG = True

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'gtd',
#         'USER': 'you',
#         'PASSWORD': '',
#         'HOST': '127.0.0.1',
#         'PORT': '',
#     },
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

TODO_STAFF_ONLY = False
TODO_DEFAULT_ASSIGNEE = None
TODO_PUBLIC_SUBMIT_REDIRECT = '/'
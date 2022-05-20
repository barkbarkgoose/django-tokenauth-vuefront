"""
this file is meant to be used when running tests for the api app.  It will
overwrite a few things

to run from BASE_DIR

    python manage.py test api --settings=api.testconfig
"""

from main.settings import *
from main.settings import BASE_DIR # 2nd import not needed but will stop pylance from complaining

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
				# --- for tests.py to work this needs to be set ---
        'TEST': {
            'MIRROR': 'default',  # Added this setting
        }
    }
}

# # --- code to put in start of tests if want to enforce this file usage ---
# def check_settings(self, settings):
#     db = settings.DATABASES['default']
#     if (
#         'TEST' not in db or 
#         'MIRROR' not in db['TEST'] or
#         db['TEST']['MIRROR'] != 'default'
#         ):
#         self.fail("run again with `--settings=api.testconfig` option")
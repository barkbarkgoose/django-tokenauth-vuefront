# about

> "If creating a separate backend and frontend then session based authentication won't work, you'll need to do token based authentication" ~ me + the internet

The user_api app is intended to be added into your existing project to provide api endpoints for user management.  It's built to use token based authentication so intended that the front end / client doesn't need to be within the same project.

# references

**docs**: https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication

**an article that goes into more detail**: https://spapas.github.io/2021/08/25/django-token-rest-auth/

- code they use for that: https://github.com/spapas/rest_authenticate

# project setup

## dependencies

_see requirements.txt_
	
## settings

**NOTE**: _I didn't find anything in the docs saying that `DEFAULT_PERMISSION_CLASSES` needed to be specified in the rest_framework settings.  After testing I found that this needs to be there in order for authentication to be required_

```python
# ...

# --- uri needed to perform localized testing ---
TEST_BASE_URL = 'http://localhost:8000/'

INSTALLED_APPS = [
	# ...
	'rest_framework',
	'rest_framework.authtoken',
	'user_api',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
				# --- if you need tests to have access to same data that's already in
				#     db - add this next portion ---
        # 'TEST': {
        #     'MIRROR': 'default',  # Added this setting
        # }
    }
}

# ...

```

# testing

see notes at top of user_api.tests file.

## manually create a test csrf_token for a user

The endpoint to create a token for a user is `'users/login/'`. 

alternatively you can create from the admin page or with a call like this.

	python manage.py drf_create_token <username>
	
	a1c8c64fa2907c5ad43c37dfea7506ce08d8cf82





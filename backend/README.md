> "If creating a separate backend and frontend then session based authentication won't work, you'll need to do token based authentication" ~ me + the internet

**docs**: https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication

**an article that goes into more detail**: https://spapas.github.io/2021/08/25/django-token-rest-auth/

- code they use for that: https://github.com/spapas/rest_authenticate

-----

# simple tutorial

**original post**: https://simpleisbetterthancomplex.com/tutorial/2018/11/22/how-to-implement-token-authentication-using-django-rest-framework.html

-----

# notes

my notes are pretty much the condensed version of the article.

DRF tokens may not be enough security on its own for some use cases.  I'd suggest looking into the following:

- https://james1345.github.io/django-rest-knox/
- https://django-rest-framework-simplejwt.readthedocs.io/en/latest/

## create django project

	mkdir main
	cd main
	django-admin startproject main .
	cd main
	django-admin startapp core

## dependencies

	django==3.2
	djangorestframework

## apps.py

I got an error with the project being set up the way it is in reference to the import for the core app.  In `core.apps.py` i have the following

```python
# ...
name = 'main.core'
# ...
```

## urls.py

```python
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token 
from main.core import views

urlpatterns = [
    path('hello/', views.HelloView.as_view(), name='hello'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
```

## views.py

```python
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

class HelloView(APIView):
  def get(self, request):
    content = {'message': 'Hello, World!'}
    return Response(content)
```
	
## settings.py

**NOTE**: _I didn't find anything in the docs saying that `DEFAULT_PERMISSION_CLASSES` needed to be specified in the rest_framework settings.  After testing I found that this needs to be there in order for authentication to be required_

```python
# ...

INSTALLED_APPS = [
	# ...
	'rest_framework',
	'rest_framework.authtoken',
	'<appname>',  # for tutorial it's 'main.core',
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
				# --- for tests.py to work this needs to be set ---
        'TEST': {
            'MIRROR': 'default',  # Added this setting
        }
    }
}

# ...

```

_note that I've added `'TEST'` under `DATABASES`, this is needed to fully test routing endpoints from tests.py_ 

## create a user

	python manage.py createsuperuser --username <name> --email <name>@<example.com>

### create a test csrf_token for the user

	python manage.py drf_create_token <name>
	
	a1c8c64fa2907c5ad43c37dfea7506ce08d8cf82

### test calls to api now

calls without Token as a header should fail.

test with curl:

	curl http://127.0.0.1:8000/hello/ -H 'Authorization: Token a1c8c64fa2907c5ad43c37dfea7506ce08d8cf82'
	
test with http: 

	http http://127.0.0.1:8000/hello/ 'Authorization: Token a1c8c64fa2907c5ad43c37dfea7506ce08d8cf82'

finally as a python request:

	import requests
	
	url = 'http://localhost:8000/hello/'
	headers = {'Authorization': 'Token 5475212b125e8d056e4c12ec050854d737f8718f'}
	r = requests.get(url, headers=headers)

### users can request a token via an api call if they give the correct password and username

```bash
http post http://127.0.0.1:8000/api-token-auth/ username=<name> password=<pass>
```

if a token has already been created for the user this will return that one.

# testing

to test the api endpoints django tests will need to access the same database that is normally used.

<!-- when testing from the BASE_DIR type the following:

	python manage.py test api --settings=api.testconfig -->

I've gone back and forth between forcing usage of a settings file just for tests.  Right now I think I prefer just putting a BASE_URL variable in the main settings file and referencing that.


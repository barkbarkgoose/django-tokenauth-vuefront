# django token authentication with vue client

The starter code for the backend came from another [project](https://github.com/barkbarkgoose/django-tokenauth) which came from this [tutorial](https://simpleisbetterthancomplex.com/tutorial/2018/11/22/how-to-implement-token-authentication-using-django-rest-framework.html)

My intention is to make different pages in the frontend to test out and document ways that token authentication can be used with DRF.

## things I want to try

- [ ]  set up tests

- [ ]  front end requests a form from django

- [ ]  form submission and checking in django

- [ ]  timeout for token, force front-end to request update
  - [ ]  [token creation/retrieval](https://www.django-rest-framework.org/api-guide/authentication/#generating-tokens)

- [ ]  require csrf for any unsafe requests: GET, POST, PUT, PATCH, DELETE
  - [ ]  see `django-cors-headers`

- [ ]  user creation from front-end

- [ ]  vue create hash for password and send that when authenticating
  - [ ]  backend then unhashes password

- [ ]  user login done via `api-token-auth/` POST request.  If username and password match then a token is returned.  That can be stored in local or session storage with an optional timeout to stay logged into the site.

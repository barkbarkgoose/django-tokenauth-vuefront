# django token authentication with vue client

The starter code for the backend came from another [project](https://github.com/barkbarkgoose/django-tokenauth) which came from this [tutorial](https://simpleisbetterthancomplex.com/tutorial/2018/11/22/how-to-implement-token-authentication-using-django-rest-framework.html)

My intention is to make different pages in the frontend to test out and document ways that token authentication can be used with DRF.

# TODO

## backend

- [ ]  data sanitization.  Make all the views use a serializer to confirm format is correct.

## frontend

- [ ]  front end requests a form from django
- [ ]  form submission and checking in django
- [ ]  timeout for token, force front-end to request update
  - [ ]  [token creation/retrieval](https://www.django-rest-framework.org/api-guide/authentication/#generating-tokens)
- [ ]  require csrf for any unsafe requests: GET, POST, PUT, PATCH, DELETE
  - [ ]  see `django-cors-headers`
- [ ]  user creation from front-end
- [ ]  vue create hash for password and send that when authenticating
  - [ ]  backend then unhashes password

-----

# testing

## backend

- [x]  user login done via `login/` POST request.  If username and password match then a token is returned.  That can be stored in local or session storage with an optional timeout to stay logged into the site.
- [x]  regular user deletion to set their account as inactive
  - [ ]  user to have option to completely delete their account
- [x]  admin to delete other user completely
- [x]  test_user to perform soft delete on itself
- [x]  user updates
  - [x]  password
  - [x]  email
  - [x]  username
- [ ]  admin user updates
  - [ ]  will need to check if attribute is valid before trying to set it
  - [ ]  use serializer
- [x]  test using token to authenticate without any user
  -  ...token has to have associated user to work with DRF.
- [x]  check if "is_staff" gives admin priveleges
  -  ...it does, checked manually
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

import pdb
import requests
import sys
# import requests

test_client = Client()

"""
DRF response codes: https://www.django-rest-framework.org/api-guide/status-codes/#status-codes

"""

class ApiEndpointTest(TestCase):
    def setUp(self):
        # --- create user ---
        self.test_user, created = User.objects.get_or_create(
            username = 'testuser',
            password = 'grumpymcgrumpface88'
        )
        # --- user will start with staff privelages ---
        if created: 
            self.test_user.is_staff = True
            self.test_user.save()
        # --- set token for user ---
        self.token, created = Token.objects.get_or_create(user=self.test_user)
        if created: 
            self.token.save()
            self.test_user.auth_token = self.token
            self.test_user.save()

    def test_add_testuser(self):
        """
        try to make call to create, or fetch, test user. Exit if fails
        """
        pass


    def test_pass(self):
        response = requests.get(
            settings.TEST_BASE_URL + 'hello/',
            headers={'Authorization': f"Token {str(self.test_user.auth_token)}"}
        )
        pdb.set_trace()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_jake(self):
        jake = User.objects.get(username='jake')
        response = requests.get(
            settings.TEST_BASE_URL + 'hello/',
            headers={"Authorization": f"Token {str(jake.auth_token)}"}
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
    
    def test_auth_fail(self):
        response = test_client.get('/hello/')
        # --- check for 401 response ---
        self.assertEqual(
            response.status_code, 
            status.HTTP_401_UNAUTHORIZED
        )

    # def test_method_fail(self):
    #     response = test_client.post('/hello/')
    #     self.assertEqual(
    #         response.status_code, 
    #         status.HTTP_301_MOVED_PERMANENTLY
    #     )
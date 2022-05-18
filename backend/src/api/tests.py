from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from api.request_methods import _delete_request
from api.request_methods import _get_request
from api.request_methods import _post_request
from api.request_methods import _put_request

import pdb
import requests
import sys
# import requests

test_client = Client()

"""
DRF response codes: https://www.django-rest-framework.org/api-guide/status-codes/#status-codes

"""
_testData = {
    'test_user': {
        'username': 'testuser',
        'password': 'grumpymcgrumpface88',
        'token': '',
    },
    'admin_user': {
        'username': '',
        'password': '',
        'token': '',
    }
}

class Test00(TestCase):
    def test_00_add_testuser(self):
        """
        try to make call to create, or fetch, test user. Exit if fails
        """
        uri = 'signup'
        headers = {
            'username': _testData['test_user']['username'], 
            'password': _testData['test_user']['password']
        }
        response = _put_request(uri, headers)

        # --- make sure account was either created or duplicate found ---
        if response.status_code == status.HTTP_201_CREATED:
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED
            )
        else:
            self.assertEqual(
                response.status_code,
                status.HTTP_409_CONFLICT
            )

class Test01(TestCase):
    def test_00_login(self):
        """
        test user login to get token for authentication
        """
        uri = 'login'
        headers = {
            'username': _testData['test_user']['username'], 
            'password': _testData['test_user']['password']
        }
        response = _post_request(uri, headers)
        if response.status_code == status.HTTP_200_OK:
            user, _ = User.objects.get_or_create(username=headers['username'])
            token, created = Token.objects.get_or_create(
                user=user,
                key=response.json()['token']
            )
            if created: token.save()
            _testData['test_user']['token'] = str(token)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

class Test02(TestCase):
    def test_00_hello_fail(self):
        uri = 'hello'
        response = _get_request(uri)
        self.assertEqual(
            response.status_code, 
            status.HTTP_401_UNAUTHORIZED
        )

    def test_01_hello_success(self):
        token = _testData['test_user']['token']
        headers={
            'Authorization': f"Token {token}"
        }
        uri = 'hello'
        response = _get_request(uri, headers)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )


class Test03(TestCase):
    def test_00_delete_user_admin_fail(self):
        
        token = _testData['test_user']['token']
        headers={
            'username': _testData['test_user']['username'],
            'password': _testData['test_user']['password'],
            'Authorization': f"Token {token}",
        }
        uri = 'admin-delete-user'
        response = _delete_request(uri, headers)
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_01_get_admin_user(self):
        """
        add admin user to _testData
        """
        username = input("\nEnter admin username: ")
        password = input("Enter admin password: ")
        _testData['admin_user']['username'] = username
        _testData['admin_user']['password'] = password

        # --- try to get token with user credentials ---
        response = _post_request(
            'login',
            {'username': username, 'password': password}
        )
        if response.status_code == status.HTTP_200_OK:
            _testData['admin_user']['token'] = response.json()['token']
            self.assertEqual(True, True)
        else:
            self.fail("\ntoken or admin user not found\n")

    def test_02_delete_user_admin_pass(self):
        """
        
        """
        token = _testData['admin_user']['token']
        headers={
            'username': _testData['admin_user']['username'],
            'password': _testData['admin_user']['password'],
            'Authorization': f"Token {token}",
        }
        uri = 'admin-delete-user'
        response = _delete_request(uri, headers)
        self.assertEqual(
            response.status_code,
            status.HTTP_202_ACCEPTED
        )


    # def test_jake(self):
    #     jake = User.objects.get(username='jake')
    #     headers={"Authorization": f"Token {str(jake.auth_token)}"}
    #     uri = '/hello/'
    #     response = self._get_request(uri, headers)
    #     self.assertEqual(
    #         response.status_code,
    #         status.HTTP_200_OK
    #     )


    # def test_method_fail(self):
    #     response = test_client.post('/hello/')
    #     self.assertEqual(
    #         response.status_code, 
    #         status.HTTP_301_MOVED_PERMANENTLY
    #     )
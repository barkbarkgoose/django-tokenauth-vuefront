from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from api.request_methods import MakeRequest

import pdb
import sys

# ==============================================================================
"""
DRF response codes: https://www.django-rest-framework.org/api-guide/status-codes/#status-codes
"""
test_client = Client()
_testData = {
    'test_user': {
        'id': '',
        'username': 'testuser',
        'password': 'grumpymcgrumpface88',
        'token': '',
    },
    'admin_user': {
        'id': '',
        'username': 'admin',
        'password': 'adminpass',
        'token': '',
    }
}

# =========================== SETUP (add testuserr) ============================
class Test00_TestUser_Create(TestCase):
    def test_00_testuser_add_testuser_pass(self):
        """
        try to make call to create, or fetch, test user. Exit if fails
        """
        uri = 'signup'
        data = {
            'username': _testData['test_user']['username'], 
            'password': _testData['test_user']['password']
        }
        response = MakeRequest.put(uri, json=data)
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

# =============================== TESTUSER TESTS ===============================
class Test01_TestUser_Login_Info(TestCase):
    def test_00_testuser_login_pass(self):
        """
        test user login to get token for authentication
        """
        uri = 'login'
        data = {
            'username': _testData['test_user']['username'], 
            'password': _testData['test_user']['password']
        }
        response = MakeRequest.post(uri, json=data)
        if response.status_code == status.HTTP_200_OK:
            user, _ = User.objects.get_or_create(username=data['username'])
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

    def test_01_testuser_get_userinfo_pass(self):
        """
        get testuser info
        """
        uri = 'info'
        headers = {'Authorization': f"Token {_testData['test_user']['token']}"}
        response = MakeRequest.get(uri, headers=headers)
        if response.status_code == status.HTTP_200_OK:
            rdata = response.json()
            _testData['test_user']['id'] = rdata['id']

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

# =============================== HELLO TEST ===================================
class Test02_TestUser_Hello(TestCase):
    def test_00_testuser_hello_fail(self):
        uri = 'hello'
        response = MakeRequest.get(uri)
        self.assertEqual(
            response.status_code, 
            status.HTTP_401_UNAUTHORIZED
        )

    def test_01_testuser_hello_success(self):
        token = _testData['test_user']['token']
        headers={'Authorization': f"Token {token}"}
        uri = 'hello'
        response = MakeRequest.get(uri, headers=headers)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

class Test03_TestUser_Update_Delete_Signup(TestCase):
    def test_00_testuser_update_pass(self):
        """
        send request to update user
        """
        uri = 'update'
        headers = {'Authorization': f"Token {_testData['test_user']['token']}"}
        data = {
            'first_name': 'newfirstname',
            'last_name': 'newlastname',
            'email': 'newemail@test.tst',
            'is_active': False,
        }
        response = MakeRequest.post(uri, headers=headers, json=data)
        self.assertEqual(
            response.status_code,
            status.HTTP_202_ACCEPTED
        )

    def test_00_testuser_update_fail(self):
        """
        send request to update, don't send authtoken
        """
        uri = 'update'
        headers = {}
        data = {
            'first_name': 'anothernewfirstname',
            'last_name': 'anothernewlastname',
            'email': 'anothernewemail@test.tst',
            'yo_mama': 'unsavory joke',
        }
        response = MakeRequest.post(uri, headers=headers, json=data)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_02_testuser_delete_fail(self):
        """
        testuser try to delete self, don't send authtoken
        """
        uri = 'delete'
        headers = {}
        response = MakeRequest.delete(uri, headers=headers)
        self.assertEqual(
            response.status_code, 
            status.HTTP_401_UNAUTHORIZED
        )

    def test_03_testuser_delete_pass(self):
        """
        testuser try to delete self, don't send authtoken
        """
        uri = 'delete'
        headers = {"Authorization": f"Token {_testData['test_user']['token']}"}
        response = MakeRequest.delete(uri, headers=headers)
        self.assertEqual(
            response.status_code, 
            status.HTTP_202_ACCEPTED
        )

    def test_04_testuser_hello_fail(self):
        """
        user is inactive, so this request should now fail
        """
        uri = 'hello'
        headers = {"Authorization": f"Token {_testData['test_user']['token']}"}
        response = MakeRequest.get(uri, headers=headers)
        self.assertEqual(
            response.status_code, 
            status.HTTP_401_UNAUTHORIZED
        )

    def test_05_testuser_reactivate_pass(self):
        """
        use signup endpoint to reactivate test_user
        """
        uri = 'signup'
        data = {
            "username": _testData['test_user']['username'],
            "password": _testData['test_user']['password'],
        }
        response = MakeRequest.put(uri, json=data)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_06_testuser_newsignup_fail(self):
        """
        try to sign up enduser again, should fail with 409 status
        """
        uri = 'signup'
        data = {
            "username": _testData['test_user']['username'],
            "password": _testData['test_user']['password'],
        }
        response = MakeRequest.put(uri, json=data)
        self.assertEqual(
            response.status_code,
            status.HTTP_409_CONFLICT
        )

# ==============================================================================
# ==================== ADMIN TESTS (these should come last) ====================
# ==============================================================================
class Test04_Admin_Login_DeleteTestUser(TestCase):
    """
    test endpoints requiring admin privelages
    """
    def test_01_admin_login_pass(self):
        """
        add admin user to _testData
        """
        if _testData['admin_user']['username'] == '':
            username = input("\nEnter admin username: ")
            _testData['admin_user']['username'] = username

        if _testData['admin_user']['password'] == '':
            password = input("Enter admin password: ")
            _testData['admin_user']['password'] = password
        # --- try to get token with user credentials ---
        response = MakeRequest.post(
            'login',
            json={
                'username': _testData['admin_user']['username'], 
                'password': _testData['admin_user']['password']
            }
        )
        if response.status_code == status.HTTP_200_OK:
            _testData['admin_user']['token'] = response.json()['token']
            self.assertEqual(True, True)
        else:
            self.fail("\ntoken or admin user not found\n")

    def test_02_admin_get_userlist_pass(self):
        """
        get testuser info
        """
        uri = 'admin-userlist'
        headers = {'Authorization': f"Token {_testData['admin_user']['token']}"}
        response = MakeRequest.get(uri, headers=headers)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_03_admin_search_testuser_pass(self):
        """
        successfully search for test_user by username
        """
        uri = 'admin-searchuser'
        headers = {'Authorization': f"Token {_testData['admin_user']['token']}"}
        response = MakeRequest.get(
            uri, 
            headers=headers,
            json={"username": _testData['test_user']['username']}
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_04_admin_search_testuser_fail(self):
        """
        search for user, but give username that won't work
        """
        uri = 'admin-searchuser'
        headers = {'Authorization': f"Token {_testData['admin_user']['token']}"}
        response = MakeRequest.get(
            uri, 
            headers=headers,
            json={"username": "badusername"}
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
    
    def test_05_admin_search_testuser_fail(self):
        """
        search for user, but don't give any arguments in json
        """
        uri = 'admin-searchuser'
        headers = {'Authorization': f"Token {_testData['admin_user']['token']}"}
        response = MakeRequest.get(
            uri, 
            headers=headers,
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_06_admin_search_testuser_fail(self):
        """
        FAIL: search for user, but as test_user
        """
        uri = 'admin-searchuser'
        headers = {'Authorization': f"Token {_testData['test_user']['token']}"}
        response = MakeRequest.get(
            uri, 
            headers=headers,
            json={"username": _testData['test_user']['username']}
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_07_admin_delete_testuser_fail(self):
        """
        FAIL: try to delete user as admin, but with test_user token
        """
        token = _testData['test_user']['token']
        data = {
            'id': _testData['test_user']['id']
        }
        headers={'Authorization': f"Token {token}"}
        uri = 'admin-deleteuser'
        response = MakeRequest.delete(uri, headers=headers, json=data)
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_08_admin_delete_testuser_fail(self):
        """
        FAIL: try to delete user as admin, but no data privided
        """
        token = _testData['admin_user']['token']
        data = {}
        headers={'Authorization': f"Token {token}"}
        uri = 'admin-deleteuser'
        response = MakeRequest.delete(uri, headers=headers, json=data)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_09_admin_delete_testuser_fail(self):
        """
        FAIL: try to delete user as admin, bad id provided
        """
        token = _testData['admin_user']['token']
        data = {
            'id': 'badid'
        }
        headers={'Authorization': f"Token {token}"}
        uri = 'admin-deleteuser'
        response = MakeRequest.delete(uri, headers=headers, json=data)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_10_admin_delete_testuser_pass(self):
        """
        SUCCESS: successfully delete user as admin
        """
        token = _testData['admin_user']['token']
        data = {
            'id': _testData['test_user']['id']
        }
        headers = {'Authorization': f"Token {token}"}
        uri = 'admin-deleteuser'
        response = MakeRequest.delete(uri, headers=headers, json=data)
        self.assertEqual(
            response.status_code,
            status.HTTP_202_ACCEPTED
        )
# --- django imports ---
from re import S
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from api.serializer import CreateUserSerializer

# --- 3rd party imports ---
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# --- project imports ---
from api.serializer import CreateUserSerializer
from api.serializer import AdminGetUserSerializer
from api.serializer import GetUserSerializer

# --- generic python library imports ---
import pdb

"""
fields for request.user

'_get_pk_val', '_get_unique_checks', '_legacy_get_session_auth_hash', '_meta', '_password', '_perform_date_checks', '_perform_unique_checks', '_prepare_related_fields_for_save', '_save_parents', '_save_table', '_set_pk_val', '_state', 

'auth_token', 'check', 'check_password', 'clean', 'clean_fields', 'date_error_message', 'date_joined', 'delete', 'email', 'email_user', 'first_name', 'from_db', 'full_clean', 'get_all_permissions', 'get_deferred_fields', 'get_email_field_name', 'get_full_name', 'get_group_permissions', 'get_next_by_date_joined', 'get_previous_by_date_joined', 'get_session_auth_hash', 'get_short_name', 'get_user_permissions', 'get_username', 'groups', 'has_module_perms', 'has_perm', 'has_perms', 'has_usable_password', 'id', 'is_active', 'is_anonymous', 'is_authenticated', 'is_staff', 'is_superuser', 'last_login', 'last_name', 'logentry_set', 'natural_key', 'normalize_username', 'objects', 'password', 'pk', 'prepare_database_save', 'refresh_from_db', 'save', 'save_base', 'serializable_value', 'set_password', 'set_unusable_password', 'unique_error_message', 'user_permissions', 'username', 'username_validator', 'userprofile', 'validate_unique'

"""
# NOTE: user login handled by 


# --- basic hello api response ---
class HelloView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': f'Hello, {request.user}!'}
        return Response(content)


class SignupView(APIView):
    """
    @return:
        201 - SUCCESS
        400 - ERROR
    """
    http_method_names = ["put"]
    permission_classes = [AllowAny]
    serializer_class = CreateUserSerializer

    def put(self, request):
        serialized = CreateUserSerializer(data=request.data)
        if serialized.is_valid():
            pw = serialized.validated_data.pop('password')
            user = serialized.create(serialized.validated_data, pw)
            return Response(serialized.validated_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)
        
        

class UserInfo(APIView):
    http_method_names = ['get']
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = GetUserSerializer(request.user)
        return Response(serializer.data)


# --- return list of all users if request comes from admin ---
class UserList(ListCreateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = AdminGetUserSerializer
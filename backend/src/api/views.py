# --- django imports ---
from re import S
from django.contrib.auth.models import User
from django.http import QueryDict
from django.shortcuts import render, redirect
from django.urls import reverse

# --- 3rd party imports ---
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# --- project imports ---
# from api.serializer import CreateUserSerializer
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
class AdminDeleteUser(APIView):
    """
    USER DELETION - ADMIN
        - admin privileges required to fully delete user
        - username and password are required along with token
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def delete(self, request):
        print(f"request.POST: {request.POST}")
        print(f"request.data: {request.data}")
        return Response({"status": "OK"}, status=status.HTTP_202_ACCEPTED)

# ==============================================================================
class UserDeleteAccount(APIView):
    """
    USER DELETION - NORMAL USER
        - regular users can shallow-delete their own account. which sets
          user.is_active to False
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        pdb.set_trace()
        print(request.POST)


# ==============================================================================
class Hello(APIView):
    """
    simple Hello view to test user authentication
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': f'Hello, {request.user}!'}
        return Response(content, status=status.HTTP_200_OK)

# ==============================================================================
# LoginView --> rest_framework.authtoken.views.obtain_auth_token.
#       - returns token if username and pass check out (creates if not already made)

# ==============================================================================
class Signup(APIView):
    """
    create new User
    Error cases:
        - username taken and user is active
        - username taken but user not active
            - in this case no data is overwritten and the account is reactivated
    
    @RETURN_STATUS:
        201 - SUCCESS
        400 - ERROR
        409 - CONFLICT (username taken)
    """
    http_method_names = ["put"]
    permission_classes = [AllowAny]
    # serializer_class = CreateUserSerializer

    def put(self, request):
        # --- make sure data has at least username and password ---
        if False in ('username', 'password' in request.data):
            request_data = request.POST.dict()
        else:
            request_data = request.data
    
        try:
            user, created = User.objects.get_or_create(username=request_data['username'])
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # --- check possible conflict if user not created (username taken) ---
        conflict = not created
        if not created:
            if not user.is_active:
                user.is_active = True
                conflict = False
        else:
            # --- password only set if new user, not reinstating old one ---
            user.set_password = request_data['password']
        
        if conflict: 
            return Response(
                {"username": "username already taken"}, 
                status=status.HTTP_409_CONFLICT
            )
        else:
            user.save()
            return Response(
                {'id': user.id, 'username': user.username},
                status=status.HTTP_201_CREATED
            )
                
                
# ==============================================================================
class UserInfo(APIView):
    """
    get info for single user
    """
    http_method_names = ['get']
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = GetUserSerializer(request.user)
        return Response(serializer.data)

# ==============================================================================
class UserList(ListCreateAPIView):
    """
    return list of all users if request comes from admin
    """
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = AdminGetUserSerializer

# ==============================================================================
class UserUpdate(APIView):
    pass
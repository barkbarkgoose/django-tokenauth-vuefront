# --- django imports ---
from re import S
from django.contrib.auth.hashers import check_password
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
from user_api.serializer import AdminGetUserSerializer
from user_api.serializer import GetUserSerializer

# --- generic python library imports ---
import pdb

"""
__RESPONSE_CODES__
    SUCCESS - (methods that I return explicitly)
        DELETE: 202
        GET: 200
        POST: 201, 202
        PUT: 201, 202

    ERROR
        ... a bit of everything ...
        400: bad request
        401: unauthorized - typically if a user is inactive and trying to log in
        403: forbidden - user doesn't have permissions to access endpoint
        404: not found
        409: conflict - example would be trying to create user that is already created
        500: internal server error
"""
# ==============================================================================
class AdminDeleteUser(APIView):
    """
    USER DELETION - ADMIN
        - admin privileges and valid user id required to fully delete
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def delete(self, request):
        """
        - check for id in request.data
        - check for user match
        """
        error = False
        # --- default repsonse status ---
        if 'id' in request.data:
            userid = request.data['id']
            try:
                user = User.objects.get(id=userid)
            except:
                error = True
        else:
            userid = "None"
            error = True

        # --- now actually try to delete user ---
        if not error:
            try:
                user.delete()
            except:
                error = True
        
        if error:
            return Response(
                {'message': f'user with id "{userid}" not found'},
                status.HTTP_400_BAD_REQUEST
            )

        return Response({"message": "OK"}, status=status.HTTP_202_ACCEPTED)

# ==============================================================================
class AdminSearchUser(APIView):
    """
    search for User as Admin
        - if authenticated will return 200 response whether user is found or not
        - if user found 
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        # --- make sure id or username are in request.data ---
        user = None
        if 'id' in request.data:
            user = User.objects.filter(id=request.data['id']).first()
        elif 'username' in request.data:
            user = User.objects.filter(username=request.data['username']).first()
        
        if not user:
            if 'id' in request.data or 'username' in request.data:
                message = "user not found"
            else:
                message = "user id or username required for lookup"

            return Response(
                {'message': message}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = GetUserSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)

class AdminUserUpdate(APIView):
    """
    same as regular UserUpdate view, but all user fields are accessible
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    allowed_fields = ['first_name', 'last_name', 'email']

    def post(self, request):
        user = request.user
        data = request.data
        keys = data.keys()
        print("\nkey-val pairs in request:")
        for key in keys:
            print(f"\t{key}: {data[key]} --> ")

# ==============================================================================
class DeleteUser(APIView):
    """
    USER DELETION - NORMAL USER
        - requires token authentication, user will be part of request
        - allows users shallow-delete their own account. Which sets
          user.is_active to False
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        try:
            request.user.is_active = False
            request.user.save()
            return Response(
                {"message": f"user: {request.user} set as inactive"}, 
                status=status.HTTP_202_ACCEPTED
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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
        200 - SUCCESS (reactivated)
        201 - SUCCESS (created)
        400 - ERROR
        409 - CONFLICT (username taken)
    """
    permission_classes = [AllowAny]
    # serializer_class = CreateUserSerializer

    def put(self, request):
        # --- make sure data has username and password ---
        if False in ('username', 'password' in request.data):
            try:
                _ = request.data['username']
                _ = request.data['password']
            except Exception as e:
                return Response(
                    {'error': f'{str(e)} missing'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

        user, created = User.objects.get_or_create(username=request.data['username'])

        # --- check possible conflict if user not created (username taken) ---
        conflict = not created
        rstatus = None
        message = None
        if not created:
            if not user.is_active:
                passmatch = check_password(request.data['password'], user.password)
                if passmatch:
                    user.is_active = True
                    user.save()
                    conflict = False
                    rstatus = status.HTTP_200_OK
                    message = {"message": "previous user found and reactivated"}
        else:
            # --- password only set if new user, not reinstating old one ---
            user.set_password(request.data['password'])
            user.save()
            rstatus = status.HTTP_201_CREATED
            message = {"id": user.id, "message": f"user \"{user.username}\" created"}
        
        if conflict: 
            return Response(
                {"message": "username already taken"}, 
                status=status.HTTP_409_CONFLICT
            )
        else:
            return Response(message, status=rstatus)
                  
# ==============================================================================
class UserInfo(APIView):
    """
    get info for single user
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = GetUserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

# ==============================================================================
class UserList(ListCreateAPIView):
    """
    return list of all users if request comes from admin
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = AdminGetUserSerializer

# ==============================================================================
class UserUpdate(APIView):
    """
    Update user based on key/val pairs in request.data.  ignores unallowed_fields
    will always return 202 response if user is authenticated, even if nothing is changed
    response data will include user info.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    allowed_fields = ['first_name', 'last_name', 'email']

    def post(self, request):
        user = request.user
        data = request.data
        keys = data.keys()
        updated = False
        for key in keys:
            if key in self.allowed_fields: 
                setattr(user, key, data[key])
                updated = True
        
        if updated:
            user.save()

        serializer = GetUserSerializer(user)
        
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

# ==============================================================================
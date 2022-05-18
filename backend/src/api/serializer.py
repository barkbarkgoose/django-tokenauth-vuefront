from wsgiref import validate
from django.contrib.auth.models import User
from rest_framework import serializers
# from .models import UserProfile

import pdb

class AdminDeleteUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
    
    def delete(self, validated_data):
        pdb.set_trace()
        pass


class AdminGetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'is_staff', 'is_active', 
            'first_name', 'last_name', 'email', 'auth_token',
            'last_login',
        )


# class CreateUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = [
#             'id', 'username', 'password', 'email', 
#             'first_name', 'last_name', 'is_active', 'is_staff',
#         ]
#         write_only_fields = ['password']
#         read_only_fields = ['id']

#     def create(self, validated_data, pw):
#         """
#         create() by default won't allow duplicates to be made with the same 
#         unique fields.  In this case the username.
#         """
#         pdb.set_trace()
#         user = User.objects.create(**validated_data)
#         user.set_password(pw)
#         user.save()
#         return user


class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


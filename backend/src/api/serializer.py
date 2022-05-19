from wsgiref import validate
from django.contrib.auth.models import User
from rest_framework import serializers
# from .models import UserProfile

import pdb

class AdminGetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'is_staff', 'is_active', 
            'first_name', 'last_name', 'email', 'auth_token',
            'last_login',
        )


class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


# class UpdateUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('email', 'first_name', 'last_name')
    
#     def get(self, instance, validated_data):
#         pass
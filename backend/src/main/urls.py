"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.urls import include, path
	2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token

from api import views

urlpatterns = [
	path('admin/', admin.site.urls),
	path('admin-deleteuser/', views.AdminDeleteUser.as_view(), name='admin_delete_user'),
	path('admin-searchuser/', views.AdminSearchUser.as_view(), name='admin_search_user'),
	path('admin-userlist/', views.UserList.as_view(), name='admin_userlist'),
	path('delete/', views.DeleteUser.as_view(), name='delete'),
	path('hello/', views.Hello.as_view(), name='hello'),
	path('login/', obtain_auth_token, name='login'), # returns token if successful
	path('signup/', views.Signup.as_view(), name='signup'),
	path('info/', views.UserInfo.as_view(), name='user_info'),
	path('update/', views.UserUpdate.as_view(), name="user_update"),
]
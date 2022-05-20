from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token

from user_api import views

urlpatterns = [
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
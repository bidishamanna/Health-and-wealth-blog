from django.urls import path
from .views import (RegisterAPIView,DeleteUserView, LoginAPIView, UserAPIView, RefreshAPIView, LogoutAPIView,UserListView,UserUpdateView,UserPutView)

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),#1
    path('login/', LoginAPIView.as_view()),#4
    path('user/', UserAPIView.as_view()),#3
    path('refresh/', RefreshAPIView.as_view()),
    path('view/', UserListView.as_view()),#2
    path('patch/', UserUpdateView.as_view()),
    path('put/', UserPutView.as_view()),
    path('Delete/', DeleteUserView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
]



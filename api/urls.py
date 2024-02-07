from django.urls import path, re_path
from .views import CreateLocationView, LogoutUser_view, LocationView
from .views import LoginUser_view, CreateUser_view

urlpatterns = [
    path('login', LoginUser_view.as_view()),
    path('create-user', CreateUser_view.as_view()),
    # path('logout',LogoutUser_view.as_view()),
    # path(logoutall', logoutall_view.as_view()),
    path('create-location', CreateLocationView.as_view()),
    path('location', LocationView.as_view())
]
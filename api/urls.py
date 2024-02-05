from django.urls import path, re_path
from .views import LocationView, CreateLocationView, LocationUser_view, CreateUser_view, LogoutUser_view


urlpatterns = [
    path('location', LocationView.as_view()),
    path('create-location', CreateLocationView.as_view()),
    path('login', LocationUser_view.as_view()),
    path('create-user', CreateUser_view.as_view()),
    # path('logout',LogoutUser_view.as_view()),
    # path(logoutall', logoutall_view.as_view()),
]
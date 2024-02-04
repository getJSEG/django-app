from django.urls import path, re_path
from .views import LocationView, CreateLocationView, LocationUser_view, CreateUser_view, LogoutUser_view


urlpatterns = [
    path('location', LocationView.as_view()),
    path('create-location', CreateLocationView.as_view()),
    path('sign-in', LocationUser_view.as_view()),
    path('create_user', CreateUser_view.as_view()),
    # path('logout',LogoutUser_view.as_view(), include('knox.urls'))
]
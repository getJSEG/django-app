from django.urls import re_path, path
from . import views

urlpatterns = [
    path('', views.index),
    path('main', views.index),
    path('sign-in', views.index)
]
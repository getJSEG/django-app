from django.urls import re_path, path
from . import views


urlpatterns = [
    path('', views.index),
    path('login', views.index),
    path('dashboard', views.index),
    path('inventory', views.index),
    path('search', views.index),
    path('sales', views.index),
    path('menu', views.index),
    path('create-product', views.index),
    path('product/<str:id>/varient', views.index),
    re_path('.*/', views.index),
]


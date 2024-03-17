from django.urls import path, re_path
# from knox.views import LogoutView, LogoutAllView


from .views import CreateLocationView, LocationView # Locations
from .views import LocationUserLoginView, CreateLocationUserView, UpdateUserinformationView, GetCSRFToken, LocationserLogoutView, GetUserProfileView, CheckAuthenticatedView# Location User
from .views import CreateProductView, GetProductsView, UpdateProductView # Product
from .views import CreateVarientView, GetVarientView, UpdateVarientView, DeleteMultipleVarientView, GetImages # Varient

urlpatterns = [
    #user 
    path('signup', CreateLocationUserView.as_view()),
    path('session', GetCSRFToken.as_view()),
    path('login', LocationUserLoginView.as_view()),
    path('logout', LocationserLogoutView.as_view()),
    path('profile', GetUserProfileView.as_view()),
    path('authenticated', CheckAuthenticatedView.as_view()),
    # path('logout-all', LogoutAllView.as_view()),
    path('update/<str:pk>', UpdateUserinformationView.as_view()),
    #locations
    path('create-location', CreateLocationView.as_view()),
    path('location', LocationView.as_view()),
    #products
    path('createproduct', CreateProductView.as_view()),
    path('products', GetProductsView.as_view()),
    path('products/update/<str:pk>', UpdateProductView.as_view()),
    #varients
    path('product/<str:pk>/createvarient', CreateVarientView.as_view()), # creating varient on the product by getting pk
    path('product/<str:product_id>/varients', GetVarientView.as_view()), # we get all of the varient base on the product
    path('product/<str:product>/varient/<str:pk>', UpdateVarientView.as_view()), # update varient by the barient pk(primary key)
    path('product/<str:pk>/varients/delete', DeleteMultipleVarientView.as_view()), # Delete Mutiple Varient
    # path('product/<str:product>/varient/delete/<str:varient>', DeleteMultipleVarientView.as_view()), # Delete Single Varient
    path('getImages', GetImages.as_view())

]
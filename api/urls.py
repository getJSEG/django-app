from django.urls import path, re_path
# from knox.views import LogoutView, LogoutAllView


from .views import product, varients, location, user, session_auth, point_of_purchase, discount

urlpatterns = [
    #Auth
    path('session', session_auth.GetCSRFToken.as_view()),
    path('authenticated', session_auth.CheckAuthenticatedView.as_view()),
    #knox
    # path('logout/', LogoutView.as_view()),
    # path('logout-all/', LogoutAllView.as_view()),
    #user
    path('signup', user.CreateUserView.as_view()),
    path('employee/create', user.CreateEmployeeView.as_view()),
    path('login', user.UserLoginView.as_view()),
    path('logout', user.LocationserLogoutView.as_view()),
    path('profile', user.GetUserProfileView.as_view()),
    path('user/update', user.UpdateUserinformationView.as_view()),
    #locations
    path('location/create', location.CreateLocationView.as_view()),
    path('location', location.LocationView.as_view()),
    path('location/delete/<str:pk>', location.DeleteLocationView.as_view()),
    path('location/update', location.UpdateLocationView.as_view()),
    #products
    path('products', product.ProductInventoryView.as_view()),
    path('product/create', product.CreateProductView.as_view()),
    path('product/update/<str:pk>', product.UpdateProductView.as_view()),
    path('product/delete/<str:product_id>', product.DeleteProductView.as_view()),
    #varients
    path('product/<str:pk>/createvarient', varients.CreateVarientView.as_view()),                       # creating varient on the product by getting pk
    path('product/<str:product_id>/varients', varients.GetVarientView.as_view()),                       # we get all of the varient base on the product
    path('product/<str:product>/varient/<str:pk>', varients.UpdateVarientView.as_view()),               # update varient by the barient pk(primary key)
    path('product/<str:pk>/varients/delete', varients.DeleteMultipleVarientView.as_view()),             # Delete Mutiple Varient
    path('varient/<str:pk>/update', varients.UpdateVarientView.as_view()),
    #Point of purchase system
    path('pos', point_of_purchase.SKUSearch.as_view()),
    path('pos/transaction', point_of_purchase.POSTransaction.as_view()),
    #DISCOUNT
    path('put/discount', discount.GetDiscountView.as_view()),
    path('create/discount', discount.CreateDiscountView.as_view()),
    path('delete/discount/<str:pk>', discount.DeleteDiscount.as_view()),

]
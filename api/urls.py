import dj_rest_auth.jwt_auth
from django.urls import path, re_path
from django.urls import path, include
from django.conf import settings
import dj_rest_auth.views as drfa
import dj_rest_auth
import rest_framework_simplejwt.views as JWTTokenView
from rest_framework_simplejwt.views import TokenVerifyView
# import oauth2_provider.views as oauth2_views 
# from knox.views import LogoutView, LogoutAllView
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )
# from rest_framework_simplejwt.views import TokenVerifyView

from .views import pos_system, product, varients, location, user, discount, accounting

# oauth2_endpoint_views = [
#     path('authorize/', oauth2_views.AuthorizationView.as_view(), name="authorize"),
#     path('token/', oauth2_views.TokenView.as_view(), name="token"),
#     path('revoke-token/', oauth2_views.RevokeTokenView.as_view(), name="revoke-token"),
# ]


# if settings.DEBUG:
#     # OAuth2 Application Management endpoints
#     oauth2_endpoint_views += [
#         path('applications/', oauth2_views.ApplicationList.as_view(), name="list"),
#         path('applications/register/', oauth2_views.ApplicationRegistration.as_view(), name="register"),
#         path('applications/<pk>/', oauth2_views.ApplicationDetail.as_view(), name="detail"),
#         path('applications/<pk>/delete/', oauth2_views.ApplicationDelete.as_view(), name="delete"),
#         path('applications/<pk>/update/', oauth2_views.ApplicationUpdate.as_view(), name="update"),
#     ]

#     # OAuth2 Token Management endpoints
#     oauth2_endpoint_views += [
#         path('authorized-tokens/', oauth2_views.AuthorizedTokensListView.as_view(), name="authorized-token-list"),
#         path('authorized-tokens/<pk>/delete/', oauth2_views.AuthorizedTokenDeleteView.as_view(),
#             name="authorized-token-delete"),
# ]

urlpatterns = [
    # path("admin", admin.site.urls),
    #Auth
    # path('o/', include((oauth2_endpoint_views, 'fourever'), namespace="oauth2_provider")),
    # path('accounts/', include('allauth.urls')),
    path('auth/login/', drfa.LoginView.as_view()),
    path('auth/token/refresh/', JWTTokenView.TokenRefreshView.as_view()),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('auth/password/reset/', drfa.PasswordResetView.as_view()),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #user
    # path('signup', user.CreateUserView.as_view(), name="login"),
    path('employee/create', user.CreateEmployeeView.as_view()),
    path('logout', user.userLogoutView.as_view()),                                                              #this only black list the JWT
    path('profile', user.GetUserProfileView.as_view(), name="profile"),
    path('user/update', user.UpdateUserinformationView.as_view()),
    #locations
    path('location/create', location.CreateLocationView.as_view()),
    path('location', location.LocationView.as_view()),
    path('location/delete/<str:pk>', location.DeleteLocationView.as_view()),
    path('location/update', location.UpdateLocationView.as_view()),
    #products
    path('product', product.CreateProductView.as_view()),                                                      # Creating product with varient
    path('products/', product.RetriveProducts.as_view()),                                                      # Retriving a list of products
    path('product/<str:pk>', product.RetriveProduct.as_view()),                                                # Retrving a single product
    path('product/<str:pk>/update/', product.UpdateProductView.as_view()),                                     # updating the Product Info Only
    path('product/<str:product_id>/delete/', product.DeleteProductView.as_view()),                             # Deleting the produt and its varients
    # images
    path('product/<str:pk>/image/', product.CreateProductImagesView.as_view()),                                # Adding Images to the Product
    path('product/<str:product>/image/<str:pk>/delete/', product.DeleteImageProduct.as_view()),                # Deleting Images to the product
    #varients
    path('product/<str:pk>/varient/', varients.CreateVarientView.as_view()),                                   # Creating a varient with product ID
    path('product/<str:product>/varient/<str:pk>/update/', varients.UpdateVarientView.as_view()),              # Updating varient
    path('product/varients/stock_level', varients.LowStockLevel.as_view()),                                       # Checking stock level of all of the varients
    path('product/<str:product>/varient/<str:pk>/delete/', varients.DeleteVarientView.as_view()),              # Deleting varient
    #POS System
    path('pos/search', pos_system.SKUSearch.as_view()),
    path('pos/checkout', pos_system.checkout.as_view()),
    path('pos/sales', pos_system.SalesorderView.as_view()),
    path('pos/products', pos_system.RetriveVarientsProducts.as_view()),
    # Accounting
    path('accounting/revenue', accounting.Revenue.as_view()),
    path('accounting/transaction_history', accounting.TransactionHistory.as_view()),
    #DISCOUNT
    path('put/discount', discount.GetDiscountView.as_view()),
    path('create/discount', discount.CreateDiscountView.as_view()),
    path('delete/discount/<str:pk>', discount.DeleteDiscount.as_view()),

]
from django.urls import path
from django.urls import path
import dj_rest_auth.views as drfa
# import rest_framework_simplejwt.views as JWTTokenViewz
# from rest_framework_simplejwt.views import TokenVerifyView
# from rest_framework_simplejwt.views import TokenRefreshView

from .views import pos_system, product, varients, location, user, discount, shipping, accounting, customer
# from .views.shipping import shipping
from .views.Products import tags, categories


urlpatterns = [
    #Auth
    path('login', user.LoginView.as_view(), name='login'),
    # path('login', drfa.LoginView.as_view(), name='login'),
    path('refresh/', user.CookieTokenRefreshView.as_view()),
    # path('auth/token/refresh/', TokenRefreshView.as_view()),
    # path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('auth/password/reset/', drfa.PasswordResetView.as_view()),
    #user
    # TODO: chager from employee -> USER
    path('user/create', user.CreateEmployeeView.as_view()),
    path('logout', user.userLogoutView.as_view()),                                                                   #this only black list the JWT
    path('profile', user.GetUserProfileView.as_view(), name="profile"),
    path('user/update', user.UpdateUserinformationView.as_view()),
    path('user/roles', user.getUserRoles.as_view()),
    #locations
    path('location/create', location.CreateLocationView.as_view()),
    path('location', location.LocationView.as_view()),
    path('location/search',location.SearchLocation.as_view()),
    path('location/delete/<str:pk>', location.DeleteLocationView.as_view()),
    path('location/update', location.UpdateLocationView.as_view()),
    #products
    path('product', product.ProductView.as_view(), name="product"),                                                      # Creating product with varient
    path('products', product.RetriveProducts.as_view(), name="retrive_product"),
    path('product/stock-level', product.LowStockLevel.as_view()),  
    path('product/search', product.SearchProducts.as_view(), name="search_product"),                                                  # Search products by name
    path('product/update/', product.UpdateProductView.as_view(), name="update_product"),                                     # updating the Product Info Only
    path('product/delete/<str:pk>', product.DeleteProductView.as_view(), name="delete_product"),                             # Deleting the produt and its varients
    #varients
    path('product/varient', varients.VarientView.as_view()),                                   # Creating a varient with product ID
    path('product/varient/update', varients.UpdateVarientView.as_view()),                     # Updating varient                                
    path('product/varient/delete/<str:pk>', varients.DeleteVarientView.as_view()),                        # Deleting varient
    path('product/tags', tags.tagsView.as_view(), name="product_tags"),
    path('product/category', categories.CategoryView.as_view(), name="product_category"),
    #POS System
    # path('pos/search', pos_system.SKUSearch.as_view()),
    path('pos/checkout', pos_system.CheckoutView.as_view()),
    path('pos/products', pos_system.PointOfSalesProductsView.as_view()),
    # Accounting
    path('accounting/revenue', accounting.IncomeView.as_view()),
    path('accounting/sales-by-category', accounting.salesbyCategory.as_view()),
    # path('accounting/transaction-history', accounting.TransactionHistory.as_view()),
    path('accounting/purchaseOrder', accounting.PurchaseOrderView.as_view()),
    path('accounting/expenses', accounting.ExpensesView.as_view()),

    # Handling Shipping Here
    path('shipping/regular', shipping.RegularShippingView.as_view()),
    path('shipping/parcel', shipping.ParselShippingView.as_view()),
    path('shipping/tracker', shipping.TrackShippingView.as_view()), #change to retrive all-packages
    path('packages/recently-created', shipping.RetriveRecentlyCreatedPackages.as_view()),
    #DISCOUNT
    path('discount', discount.GetDiscountView.as_view()),
    path('create/discount', discount.CreateDiscountView.as_view()),
    path('delete/discount/<str:pk>', discount.DeleteDiscount.as_view()),

    # customer
    path('customer/search', customer.customerView.as_view())

]
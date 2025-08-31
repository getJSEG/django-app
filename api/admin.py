from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (CustomUser, Order, ReceiptLine, Varient, Images, Product, ExpenseTypes, Expense, PurchaseOrder, PurchaseOrderLines, Tags, Categories, CustomShipping, ParselShipping, Customer, 
                     CashPayment, CreditCardPayment, BankTransferPayment)
from django.forms import Textarea, TextInput
# from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

# Register your models here.
# class UserAdminConfig(UserAdmin):

#     ordering = ('email',)
#     list_display = ('email', 'user_name', 'first_name', 'is_active', 'is_staff')

#     # fieldsets = (
#     #     (None, {'fields': ('email', 'user_name', 'first_name',)}),
#     #     ('Permissions', {'fields': ('is_staff', 'is_active')}),
#     #     ('Personal', {'fields': ('date_joined',)}),
#     # )


admin.site.register(CustomUser)
admin.site.register(Order)
admin.site.register(ReceiptLine)
admin.site.register(CustomShipping)
admin.site.register(ParselShipping)
# admin.site.register(Payment)
admin.site.register(CashPayment)
admin.site.register(CreditCardPayment)
admin.site.register(BankTransferPayment)
admin.site.register(Customer)
# admin.site.register(TransactionReceipt)
admin.site.register(Varient)
admin.site.register(PurchaseOrder)
admin.site.register(PurchaseOrderLines)
admin.site.register(Images)
admin.site.register(Product)
admin.site.register(Expense)
admin.site.register(ExpenseTypes)


admin.site.register(Tags)
admin.site.register(Categories)
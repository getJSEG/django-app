from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, SalesOrder, SalesOrderLine, TransactionReceipt
from django.forms import Textarea, TextInput

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
admin.site.register(SalesOrder)
admin.site.register(SalesOrderLine)
admin.site.register(TransactionReceipt)

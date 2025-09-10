import logging

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, ContentType
from django.contrib.auth.models import Permission
# from application.api.models. import CusomUserField
from ...models import CustomUser
import os
# all name have to be lowercase
# permission need to be lowercase

GROUPS = {
    "Owner": {
        #general permissions
        "location" : ["change", "view"],
        "discount": ["add", "change", "view", "delete"],
        "avatar": ["add", "change", "view", "delete"],
        "custom user": ["add", "change", "view", "delete"],

        #Products
        "product" : ["add", "change", "view", "delete"],
        "varient" : ["add", "change", "view", "delete"],
        "images" : ["add", "change", "view", "delete"], 
        "tags": ["add", "change", "view", "delete"],
        "categories": ["add", "change", "view", "delete"],
        "stock transfer" : ["add", "change","view", "delete"],

        # orders and payments
        "order" : ["add", "change","view", "delete"],
        "receipt line" : ["add", "change","view", "delete"],
        "cash payment" : ["add", "change","view"],
        "bank transfer payment" : ["add", "change","view"],
        "credit card payment" : ["add", "change","view"],

        # shipping and customers
        "custom shipping" : ["add", "delete", "change", "view"],
        "parsel shipping" : ["add", "delete", "change", "view"],
        "customer" : ["add", "delete", "change","view"],

        # accounting, purchases and expenses
        "expense" : ["add", "delete", "change","view"],
        "expense types" : ["add", "delete", "change","view"],
        "purchase order" : ["add", "delete", "change","view"],
        "purchase order lines" : ["add", "delete", "change","view"],      
    },

    "Manager": {
        #general permissions
        "location" : ["view"],
        "discount": ["view"],
        "avatar": ["add", "change", "view", "delete"],
        "custom user": ["add", "change", "view"],

        #Products
        "product" : ["add", "change","view", "delete"],
        "varient" : ["add", "change","view", "delete"],
        "images" : ["add", "change","view", "delete"], 
        "tags": ["add", "change", "view", "delete"],
        "categories": ["add", "change", "view", "delete"],
        "stock transfer" : ["add", "change","view", "delete"],

        # orders and payments
        "order" : ["add", "change","view", "delete"],
        "receipt line" : ["add", "change","view", "delete"],
        "cash payment" : ["add", "change","view"],
        "bank transfer payment" : ["add", "change","view"],
        "credit card payment" : ["add", "change","view"],

        # shipping and customers
        "custom shipping" : ["add", "delete", "change","view"],
        "parsel shipping" : ["add", "delete", "change","view"],
        "customer" : ["add", "delete", "change","view"],

        # accounting, purchases and expenses
        "expense" : ["add", "change","view"],
        "expense types" : ["add", "change","view"],
        "purchase order" : ["add", "change","view"],
        "purchase order lines" : ["add", "change","view"],  
    },

    "Employee": {
        #general permissions
        "location" : ["view"],
        "discount": ["view"],
        "avatar": ["add", "change", "view", "delete"],
        "custom user": ["view"],

        #Products
        "product" : ["add", "change","view", "delete"],
        "varient" : ["add", "change","view", "delete"],
        "images" : ["add", "change","view", "delete"], 
        "tags": ["add", "change", "view", "delete"],
        "categories": ["add", "change", "view", "delete"],
        "stock transfer" : ["add", "change","view", "delete"],

        # orders and payments
        "order" : ["add", "change", "view"],
        "receipt line" : ["add", "change", "view", "delete"],
        "cash payment" : ["add","view"],
        "bank transfer payment" : ["add", "view"],
        "credit card payment" : ["add", "view"],

        # shipping and customers
        "custom shipping" : ["add", "change", "view"],
        "parsel shipping" : ["add", "change", "view"],
        "customer" : ["add", "delete", "change", "view"], 
    },

    "Accounting": {
        #general permissions
        "location" : ["view"],
        "avatar": ["view"],

        #Products
        "stock transfer" : ["view"],

        # orders and payments
        "order" : ["view"],
        "receipt line" : ["view"],
        "cash payment" : ["view"],
        "bank transfer payment" : ["view"],
        "credit card payment" : ["view"],

        # accounting, purchases and expenses
        "expense" : ["view"],
        "expense types" : ["view"],
        "purchase order" : ["view"],
        "purchase order lines" : ["view"],  
    },
    "Contractor": {
        #django app model specific permissions
        "product" : ["view"],
        "varient" : ["view"],
        "images" : ["view"], 
        "tags": ["view"],
        "categories": ["view"],
        "discount": ["view"],
    },
    "Customer": {
        #Products
        "product" : ["view"],
        "varient" : ["view"],
        "images" : ["view"], 
        "tags": ["view"],
        "categories": ["view"],
        "discount": ["view"],
    },
}


USERS = {
    os.environ.get("GROUP_NAME_ONE", "") :  [os.environ.get("GROUP_POSITION_ONE", ""),os.environ.get("GROUP_EMAIL_ONE", ""),os.environ.get("GROUP_PASSWRD_ONE", "")],
    os.environ.get("GROUP_NAME_TWO", "") :  [os.environ.get("GROUP_POSITION_TWO", ""),os.environ.get("GROUP_EMAIL_TWO", ""),os.environ.get("GROUP_PASSWRD_TWO", "")],
}


class Command(BaseCommand):
    help = "Create read only default permission group for users"

    def handle(self, *args, **options):

        for group_name in GROUPS:

            new_group, created = Group.objects.get_or_create(name=group_name)

            #Loops models in group
            for app_model in GROUPS[group_name]:

                #LOOPS PERMISSION IN GROUP/MODEL
                for permission_name in GROUPS[group_name][app_model]:
                    #GENERATE PERMISSION NAMEAS DJANGO WOULD GENERATE IT
                    name = "Can {} {}".format(permission_name, app_model)
                    # codename = "".format()
                    ct = ContentType.objects.get_for_model(CustomUser)
                    print("Creating {}".format(name))

                    try:
                        model_add_perm = Permission.objects.get(name=name)
                    except:
                        logging.warning("Permission non found name {}".format(name))
                        continue
                    
                    new_group.permissions.add(model_add_perm)

            for user_name in USERS:
                new_user = None
                if user_name == "admin":
                    new_user, created = CustomUser.objects.get_or_create(username=USERS[user_name][1], is_staff = True, is_superuser=True)
                else:
                    new_user, created = CustomUser.objects.get_or_create(username=USERS[user_name][1], is_staff = False)

                new_user.set_password(USERS[user_name][2])
                new_user.save()

                if USERS[user_name][0] == str(new_group):
                    new_group.user_set.add(new_user)
                    print("Adding {} to {}".format(user_name, new_group))
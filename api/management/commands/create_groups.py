import logging

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, ContentType
from django.contrib.auth.models import Permission
# from application.api.models. import CusomUserField
from ...models import CustomUser

#TODO: CREATE  GROUPD WITH PERMISSIONS
#TODO: CONNECT A NEW DATA BASE
# TODO: FIX THE MODEL NAMING
GROUPS = {
    "Regional Manager": {
        #general permissions
        "locations" : ["add","change","view"],
        "expense" : ["add","delete","change","view"],
        "expense types" : ["add","delete","change","view"],
        "supplier" : ["add","delete","change","view"],
        "stock tranfer" : ["add","delete","change","view"], #TODO: FIX THE MISSSPELLING (tranfer to Transfer)
        "purchase order" : ["add","delete","change","view"],
        "purchase order lines" : ["add","delete","change","view"],
        "receite voucher" : ["add","delete","change","view"],
        "sales order" : ["add","delete","change","view"],
        "sales order lines" : ["add","delete","change","view"],
        "custom user" : ["add","delete","change","view"],
        "discount": ["add","delete","change","view"],
        
        "products" : ["add","delete","change","view"],
        "varients" : ["add","delete","change","view"],
        "varients images" : ["add","delete","change","view"], 
        "album" : ["add","delete","change","view"], 
    },

    "Manager": {
        #django app model specific permissions
        "locations" : ["view"],
        "custom user" : ["add","delete","change","view"],

        "expense" : ["add", "view", "change"],
        "expense types" : ["add", "view", "change"],
        "purchase order" : ["add", "view", "change"],
        "purchase order lines" : ["add", "view", "change"],
        "receite voucher" : ["add", "view", "change"],
        "return lines" : ["add", "view", "change"],
        "return orders" : ["add", "view", "change"],
        "sales order" : ["add", "view", "change"],
        "sales order lines" : ["add", "view", "change"],
        "invoice" : ["add", "view", "change"],
        "payment voucher" : ["add", "view", "change"],

        "products" : ["add","delete","change","view"],
        "varients" : ["add", "view", "change", "delete"],
        "varient images" : ["add", "view", "change", "delete"],
        "image album" : ["add", "view", "change", "delete"],
        "varient colors" : ["add", "view", "change", "delete"],

    },

    "Employee": {
        #django app model specific permissions
        "return lines" : ["add", "view"],
        "return orders" : ["add", "view"],
        "sales order" : ["add", "view"],
        "sales order lines" : ["add", "view"],
        "invoice": ["add", "view"],

        "products" : ["view"],
        "varients" : ["view"],
        "varient images" : ["view"],
        "image album" : ["view"],
        "varient colors" : ["view"],
    },

    "Accounting": {
        #django app model specific permissions
        "expense" : ["view"],
        "expense types" : [ "view"],
        "purchase order" : ["view"],
        "purchase order lines" : ["view"],
        "receite voucher" : ["view"],
        "return lines" : ["view"],
        "return orders" : ["view"],
        "sales order" : ["view"],
        "sales order lines" : ["view"],
        "invoice" : ["view"],
        "payment voucher" : ["view"],
    },
    "Contractor": {
        #django app model specific permissions
        "products" : ["view"],
        "varients" : ["view"],
        "varient images" : ["view"],
        "image album" : ["view"],
        "varient colors" : ["view"],
    },
    "Customers": {
        #django app model specific permissions
        "products" : ["view"],
        "varients" : ["view"],
        "varient images" : ["view"],
        "image album" : ["view"],
        "varient colors" : ["view"],
    },
}


USERS = {
    "jenn" : ["Manager","member@domain.cu","1234"],
    "john" :  ["Administration","admin@domain.ca","1234"],
    "admin" : ["Administration","elmer@domain.cu","1234"],
}


class Command(BaseCommand):
    help = "Create read only default permission groupd for users"

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
                    # ct = ContentType.objects.get_for_model(CustomLocationUser)
                    print("Creating {}".format(name))
                    # print(ct)

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

                if USERS[user_name][0] == str(new_group) :
                    new_group.user_set.add(new_user)
                    print("Adding {} to {}".format(user_name, new_group))
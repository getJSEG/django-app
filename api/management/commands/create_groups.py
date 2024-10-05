import logging

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, ContentType
from django.contrib.auth.models import Permission
# from application.api.models. import CusomUserField
from ...models import CustomUser

# all name have to be lowercase
# permission need to be lowercase
GROUPS = {
    "Regional Manager": {
        #general permissions
        "location" : ["add","change","view"],
        "expense" : ["add","delete","change","view"],
        "expense types" : ["add","delete","change","view"],
        "supplier" : ["add","delete","change","view"],
        "stock tranfer" : ["add","delete","change","view"], #TODO: FIX THE MISSSPELLING (tranfer to Transfer)
        "purchase order" : ["add","delete","change","view"],
        "purchase order lines" : ["add","delete","change","view"],
        "sales order" : ["add","delete","change","view"],
        "sales order line" : ["add","delete","change","view"],
        "custom user" : ["add","delete","change","view"],
        "discount": ["add","delete","change","view"],
        
        "product" : ["add","delete","change","view"],
        "varient" : ["add","delete","change","view"],
        "product images" : ["add","delete","change","view"], 
        "image album" : ["add","delete","change","view"], 
    },

    "Manager": {
        "location" : ["view"],
        "custom user" : ["add","delete","change","view"],
        "discount": ["view"],

        "expense" : ["add", "view", "change"],
        "expense types" : ["add", "view", "change"],
        "purchase order" : ["add", "view", "change"],
        "purchase order lines" : ["add", "view", "change"],
        "return lines" : ["add", "view", "change"],
        "return orders" : ["add", "view", "change"],
        "sales order" : ["add", "view", "change"],
        "sales order line" : ["add", "view", "change"],
        "payment voucher" : ["add", "view", "change"],

        "product" : ["add","delete","change","view"],
        "varient" : ["add", "view", "change", "delete"],
        "product images" : ["add", "view", "change", "delete"],
        "image album" : ["add", "view", "change", "delete"],
        "varient color" : ["add", "view", "change", "delete"],

    },

    "Employee": {
        #django app model specific permissions
        "return lines" : ["add", "view"],
        "return orders" : ["add", "view"],
        "sales order" : ["add", "view"],
        "sales order line" : ["add", "view"],
        "discount": ["view"],

        "product" : ["view"],
        "varient" : ["view"],
        "product images" : ["view"],
        "image album" : ["view"],
        "varient color" : ["view"],
    },

    "Accounting": {
        #django app model specific permissions
        "expense" : ["view"],
        "expense types" : [ "view"],
        "purchase order" : ["view"],
        "purchase order lines" : ["view"],
        "return lines" : ["view"],
        "return orders" : ["view"],
        "sales order" : ["view"],
        "sales order line" : ["view"],
        "payment voucher" : ["view"],
        "discount": ["view"],
    },
    "Contractor": {
        #django app model specific permissions
        "product" : ["view"],
        "varient" : ["view"],
        "product images" : ["view"],
        "image album" : ["view"],
        "varient color" : ["view"],
        "discount": ["view"],
    },
    "Customer": {
        #django app model specific permissions
        "product" : ["view"],
        "varient" : ["view"],
        "product images" : ["view"],
        "image album" : ["view"],
        "varient color" : ["view"],
        "discount": ["view"],
    },
}


USERS = {
    "jenn" : ["Manager","manager@gmail.com","1234"],
    "john" :  ["Administration","admin@domain.ca","1234"],
    "admin" : ["Administration","elmer@gmail.com","1234"],
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
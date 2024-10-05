from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, PermissionsMixin, AbstractBaseUser, BaseUserManager
from django.db.models import Sum
from django.core.validators import MaxValueValidator, MinValueValidator
from django import forms 
from django_resized import ResizedImageField

from sorl.thumbnail import ImageField, get_thumbnail


import os
import uuid
import datetime
from decimal import Decimal
import calendar

def get_upload_path(instance, filename):
    old_filename = filename
    filename = "%s%s" % ('product', old_filename)
    return os.path.join('varients/', filename)

#FAT MODELS THIN VIEWS
#TODO: Add country code
#TODO: Add Currency type
class Location(models.Model):
    WAREHOUSE = "Warehouse"
    RETAIL = "Retail"
    DISTRIBUTION_CENTER = "Distribution Center"

    LOCATION_TYPE_CHOICES = [
        ("WAREHOUSE", "Warehouse"),
        ("RETAIL", "Retail"),
        ("DISTRIBUTION_CENTER", "Distribution Center")
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    location_type = models.CharField(max_length=50, choices=LOCATION_TYPE_CHOICES, default=RETAIL)
    store_number = models.CharField(max_length=60, unique=True)
    incharge = models.CharField(max_length=30)
    email = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=255)
    country_code = models.CharField(max_length=255, null=True, blank=True)
    currency = models.CharField(max_length=255)
    department = models.CharField(max_length=60, null=True, blank=True)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=60)
    profit_center = models.CharField(max_length=60)
    cost_center = models.CharField(max_length=60)
    status = models.CharField(max_length=25)
    local_tax = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)       #Change name to vat (value_added_tax)
    pre_tax_items = models.BooleanField(default=False)                                  #This make it that the items already have a tax added to them
    status_date = models.DateTimeField(auto_now_add=True)
    
class CustomAccountManager(BaseUserManager):

    def create_user(self, username, first_name, password, **other_fields):
        if not username:
            raise ValueError(_("You must provide an email address"))
        
        username = self.normalize_email(username)
        user = self.model(username=username, first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, username, first_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must be assign to is_staff=true'))
        
        if other_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must be assign to is_superuser=true'))
        
        return self.create_user(username, first_name, password, **other_fields)

#USERS FOR LOCATIONS
class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.EmailField(max_length=255, null=False, blank=False, unique=True)
    # email = None
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150,  null=True, blank=True)
    password = models.CharField(max_length=255, null=False, blank=False)
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    create_on = models.DateTimeField(auto_now_add=True)
    date_joined  = models.DateTimeField(auto_now_add=True)
    status_date = models.DateTimeField(auto_now_add=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    avatar = ResizedImageField(size=[350, 350], upload_to='user', blank=True, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name']

    objects = CustomAccountManager()

    def __str__(self):
        return self.username

# user activity Here
class UserActivity(models.Model):
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=60)
    ref_doc_number = models.CharField(max_length=12)
    description = models.CharField(max_length=255)
    action_type = models.CharField(max_length=30)
    action_on = models.DateTimeField(max_length=60)
    actioned_by = models.CharField(max_length=60)

class Customer(models.Model):
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    create_on = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=20)
    email = models.CharField(max_length=75)
    country = models.CharField(max_length=25)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    state = models.CharField(max_length=30)
    zip_code = models.CharField(max_length=10, blank=True)
    department = models.CharField(max_length=30, null=True, blank=True)
    municipality = models.CharField(max_length=30, null=True, blank=True)
    status = models.ImageField(max_length=25)
    day_created = models.DateTimeField(auto_now_add=True)

##########################
##########################
####### INVENTORY ########
######## MANAGEMENT ######
##########################
class Supplier(models.Model):
    CASH = "Cash"
    CREDIT = "Credit"
    DEBIT = "Debit"
    TRANSFER = "Bank Transfer"
    CHECK = "cheque"
    PAYPAL = "Paypal"
    PAYMENT_TYPE_CHOICES = [
        ("CASH", "Cash"),
        ("CREDIT", "Credit"),
        ("DEBIT", "Debit"),
        ("TRANSFER", "Bank Transfer"),
        ("CHECK", "cheque"),
        ("PAYPAL", "Paypal")
    ]
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    create_on = models.DateTimeField(auto_now_add=True)
    supplier_name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100)
    contact_title = models.CharField(max_length=100, null=True, blank=True)
    contact_email = models.CharField(max_length=100)
    phone = models.CharField(max_length=30)
    city = models.CharField(max_length=35)
    state = models.CharField(max_length=35)
    country = models.CharField(max_length=35)
    address = models.CharField(max_length=100)
    LicenseNumber = models.CharField(max_length=30)
    payment_method = models.CharField(max_length=15, choices=PAYMENT_TYPE_CHOICES, default=CASH)
    payment_terms = models.IntegerField()
    status = models.CharField(max_length=25)
    status_date = models.DateTimeField(auto_now_add=True)

class PurchaseOrder(models.Model):
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    cost_center = models.CharField(max_length=25, blank=True)
    created_by = models.CharField(max_length=100)
    approved_by = models.CharField(max_length=100)
    status = models.CharField(max_length=25)
    status_date = models.DateTimeField(auto_now_add=True)

####################################################PRODUCT####################################################
###############################################################################################################
###############################################################################################################
 
class productCommoInfo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.ImageField(max_length=25, null=True, blank=True)
    status_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class Tags(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tag = models.CharField(max_length=100, unique=True, null=True, blank=True) 


class ImageAlbum(models.Model):
    def default(self):
        return self.images.filter(default=True).first()
    def thumnail(self):
        return self.images.filter(width__lt=100, length_lt=100)

# Product varient images for males and female models
class ProductImages(models.Model):
    images = ResizedImageField(size=[1000, 1500], upload_to="products/", blank=True, null=True)
    album = models.ForeignKey(ImageAlbum, related_name='images', on_delete=models.CASCADE)

class Product(productCommoInfo):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=60)
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    vendor_sku = models.CharField(max_length=100, null=True, blank=True)
    item_cost = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    product_acronym = models.CharField(max_length=10, null=True, blank=True)
    album = models.OneToOneField(ImageAlbum, related_name='product_album', on_delete=models.CASCADE, null=True)
    created_by = models.CharField(max_length=250, null=True, blank=True)
 
# Product varient colors
class VarientColor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = ResizedImageField(size=[100, 100], upload_to="color/", blank=True, null=True)
    color = models.CharField(max_length=100)

# product Varient
# iNSTAED OF HAVING A MANY 2 MANY RELATION SHIP  it could one a product ID
class Varient(productCommoInfo):
    size = models.CharField(max_length=10)
    units = models.PositiveIntegerField()
    sku = models.CharField(max_length=100, unique=True)
    varient_color = models.ForeignKey(VarientColor, related_name="product", on_delete=models.CASCADE)
    storage_location = models.CharField(max_length=100, null=True, blank=True)
    min_units = models.PositiveIntegerField(default=1)

    @property
    def cal_purchase_price(self):
        price = self.units * self.listed_price
        return '${}'.format(price)
    
# Product Attribute
class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, related_name="product", on_delete=models.CASCADE)
    varients = models.ManyToManyField(Varient, related_name="varients")
    tags = models.ManyToManyField(Tags, related_name="varients", blank=True)
    
    def totalVarientValue(self):
        totalPrice = self.varients.all().aggregate(total_value=Sum('price'))
        return totalPrice
    
    def varient_count(self):
        count = self.varients.all().count()
        return count


# class ProductManager(models.Manager):
#     def create (self, name, brand,location_id, vendor_sku, item_cost, product_acronym, album, created_by):
#         # attr
#         # Product
#         product = Product(name=name, brand=brand,location_id=location_id, vendor_sku=vendor_sku, item_cost=item_cost, product_acronym=product_acronym, album, created_by)
        # Tags

class Discount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    discount_code = models.CharField(max_length=56, unique=True)
    discount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, null=True, blank=True)
    expiration = models.DateTimeField()
    description = models.CharField(max_length=100)
    status_date = models.DateTimeField(auto_now_add=True)

class Catalog(models.Model):
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    catalog_name = models.CharField(max_length=100)
    varient_id = models.ForeignKey(Varient, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

# TODO: Change Spelling from __ to StockTransfer
class StockTranfer(models.Model):
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    varient_id = models.ForeignKey(Varient, on_delete=models.CASCADE)
    unit_purchase_price = models.DecimalField(max_digits=9, decimal_places=2)
    tranfer_by_location = models.IntegerField()
    tranfer_by_costcenter = models.CharField(max_length=25)
    transfer_qty = models.IntegerField()
    # total_transfer_value = models.DecimalField(max_digits=9, decimal_places=2)
    transferred_by = models.CharField(max_length=56)
    tranfer_to_location = models.IntegerField()
    tranfer_to_costcenter = models.CharField(max_length=25)
    received_qty = models.IntegerField()
    # total_received_value = models.DecimalField(max_digits=9, decimal_places=2)
    received_by = models.CharField(max_length=56)
    status = models.CharField(max_length=25)
    status_date = models.DateTimeField()

    @property
    def Total_transfer_value(self):
        return self.transfer_qty * self.unit_purchase_price

    @property
    def Total_receive_value(self):
        return self.unit_purchase_price * self.rec_quanity


###############################################################################################################
###############################################################################################################
###############################################################################################################
###############################################################################################################
###############################################################################################################
###############################################################################################################

#############
############## SALES MANAGEMENT ######
#################
#CORRECT SPELLING Receipted
# discount -> in dollars
# TAXES -> IN DOLLARS( Taxes Collected) this may vary country by coutry if taxed are included in the products
# sub total
class SalesOrder(models.Model):
    PROCESSING = "Processing"
    PAID = "Paid"
    
    SALESORDER_TYPE_CHOICES = [
        ("PROCESSING", "Processing"),
        ("PAID", "Paid"),
    ]
    # user = models.ForeignKey(Locations, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=250, null=True, blank=True)
    email = models.EmailField(max_length=250, null=True, blank=True)
    shipping_address = models.TextField(max_length=15000, null=True, blank=True)
    shipping_and_handling = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)

    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)                                         
    taxes = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    discount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, null=True, blank=True)
    order_total_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    order_total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=25, choices=SALESORDER_TYPE_CHOICES, default=PROCESSING, null=True, blank=True)
    created_by = models.CharField(max_length=250)

    @property
    def is_paid(self):
        if self.order_total_paid < self.order_total_price:
            return False
        else:
            return True

    @property
    def Gross_total(self):
        return self.subtotal + self.total_tax
    @property
    def Discount(self):
        return self.gross_total * self.discount_percentage
    
    @property
    def amount_payable(self):
        return self.gross_total - self.Discount
    
    @property
    def balance(self):
        return self.amount_payable - self.amount_paid
    
    def __str___(self):
        return f'Order Item - {str(self.id)}'

class SalesOrderLine(models.Model):
    # In store
    CLOSED = "Closed"
    # Online Orderd
    PROCESSING = "Processing"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"
    COMPLETED = "Completed"
    RETURNED = "Returned"
    # Both online and store
    REFUNDED = "Refunded"
    PARTIAL_REFUND = "Partial Refunded"
    
    RETURN_TYPE_CHOICES = [
        ("CLOSED", "Closed"),

        ("PROCESSING", "Processing"),
        ("SHIPPED", "Shipped"),
        ("DELIVERED", "Delivered"),
        ("RETURNED", "Returned"),
        ("COMPLETED", "Completed"),

        ("REFUNDED", "Refunded"),
        ("PARTIAL_REFUND", "Partial Refunded"),
    ]
    order_id = models.ForeignKey(SalesOrder, on_delete=models.CASCADE)
    varient_id = models.ForeignKey(Varient, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    status = models.CharField(max_length=25, choices=RETURN_TYPE_CHOICES, default=PROCESSING, null=True, blank=True)
    status_date = models.DateTimeField(auto_now_add=True)

    @property
    def cal_purchase_price(self):
        total_price = self.quantity * self.unit_price
        return '${}'.format(total_price)
    
    def __str___(self):
        return f'Order Item - {str(self.id)}'

class ReturnOrders(models.Model):
    ONE = "Wrong Size"
    TWO = "Product Damage"
    THREE = "Bank Tranfer"
    FOUR = "Other"
    FIVE = "Received Wrong Product"
    SIX = "No Longer Need"
    SEVEN = "Arrived Too Late"
    RETURN_TYPE_CHOICES = [
        ("ONE", "Wrong Size"),
        ("TWO", "Product Damage"),
        ("THREE", "Bank Tranfer"),
        ("FOUR", "Other"),
        ("FIVE", "Received Wrong Product"),
        ("SIX", "No Longer Need"),
        ("SEVEN", "Arrived Too Late"),
    ]

    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    order_id = models.ForeignKey(SalesOrder, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    return_reason = models.CharField(max_length=25, choices=RETURN_TYPE_CHOICES, default=ONE)
    approval_status = models.CharField(max_length=50)
    approved_by = models.CharField(max_length=100)
    credit_note = models.CharField(max_length=150, null=True, blank=True)
    return_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.CharField(max_length=100)
    status = models.CharField(max_length=25)
    status_date = models.DateTimeField()

class ReturnLines(models.Model):
    EXELENT = "New Condition"
    GOOD = "Good Condition"
    USED = "Used"
    BAD = "Damaged"
    OTHER = "OTHER"
    CONDITION_TYPE_CHOICES = [
        ("EXELENT", "New Condition"),
        ("GOOD", "Good Condition"),
        ("USED", "Used"),
        ("BAD", "Damaged"),
        ("OTHER", "Other")
    ]

    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    return_order_id = models.ForeignKey(ReturnOrders, on_delete=models.CASCADE)
    varient_id = models.ForeignKey(Varient, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=30)
    sku = models.CharField(max_length=30)
    unit_price = models.DecimalField(max_digits=9, decimal_places=2)
    quantity = models.IntegerField()
    # total_price = models.DecimalField(max_digits=9, decimal_places=2)
    condition = models.CharField(max_length=15, choices=CONDITION_TYPE_CHOICES, default=USED)
    picture_one = models.ImageField(null=True, blank=True)
    status = models.CharField(max_length=25)
    status_date = models.DateTimeField()

    @property
    def Total_price(self):
        return self.unit_price * self.quantity

# TODO: Had diferent types 
# cash debit, credit, bacnk tranfer
# class paymentType (models.Model):
#     pass

# Rename this to another thing When Deploying
# TODO: RENAME TO OrderPayments
#TODO: ADD TRANSACTION ID OR ORDER ID Auto Generated
class TransactionReceipt(models.Model):
    CASH = "Cash"
    CREDIT = "Credit Card (Offline)"
    EFT = "Bank Transfer"

    PAYMENT_TYPE_CHOICES = [
        ("CASH", "Cash"),
        ("CREDIT", "Credit"),
        ("EFT", "Bank Transfer"),
    ]
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE)
    amount_received = models.DecimalField(max_digits=7, decimal_places=2, default=0.00) 
    amount = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)                          # The amount of the first trasaction
    order_total = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)                     # this is the amount after the the refund
    
    transaction_type = models.CharField(max_length=25, choices=PAYMENT_TYPE_CHOICES, default=CASH)
    refundable_amount = models.DecimalField(max_digits=7, decimal_places=2, default=order_total)           # This the amount of money a user can be refunded /After this hits 0 the order is closed
    isOnline  = models.BooleanField(default=False)
      
    # master_transaction_id = models.IntegerField()
    # master_transaction_payment_number = models.CharField(max_length=25)
    order_payment_refund_info = models.ManyToManyField(ReturnOrders, related_name="refund_orders", blank=True)
    name_on_card = models.CharField(max_length=25, null=True, blank=True)
    has_refund = models.BooleanField(default=False)
    CcLast4Digits = models.CharField(max_length=4, null=True, blank=True)

    Auth_code = models.CharField(max_length=255, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)


# # functions as a request for payment 
# class Invoice(models.Model):
#     CASH = "Cash"
#     CREDIT = "Credit"
#     DEBIT = "Debit"
#     TRANSFER = "Bank Transfer"
#     CHECK = "cheque"
#     PAYPAL = "Paypal"

#     PAYMENT_TYPE_CHOICES = [
#         ("CASH", "Cash"),
#         ("CREDIT", "Credit"),
#         ("DEBIT", "Debit"),
#         ("TRANSFER", "Bank Transfer"),
#         ("CHECK", "cheque"),
#         ("PAYPAL", "Paypal")
#     ]
#     location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
#     subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)                                          
#     total_tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
#     grand_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
#     amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
#     payment_type = models.CharField(max_length=15, choices=PAYMENT_TYPE_CHOICES, default=CASH)
#     sales_order_id = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, null=True, blank=True)
#     discount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, null=True, blank=True)
#     # balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)                                          #
#     change = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)                                           #this is the change that should be give to the customer
#     cc_authcode= models.CharField(max_length=100, null=True, blank=True)                                                  #this is a authorizarion coe for credit card payment
#     created_on = models.DateTimeField(auto_now_add=True)
#     created_by = models.CharField(max_length=100)
#     status = models.CharField(max_length=25)
#     status_date = models.DateTimeField()

#     @property
#     def Gross_total(self):
#         return self.subtotal + self.total_tax
#     @property
#     def Discount(self):
#         return self.gross_total * self.discount_percentage
    
#     @property
#     def amount_payable(self):
#         return self.gross_total - self.Discount
    
#     @property
#     def balance(self):
#         return self.amount_payable - self.amount_paid

# class CreditNote(models.Model):
#     location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
#     created_on = models.DateTimeField()
#     return_order_id = models.ForeignKey(ReturnOrders, on_delete=models.CASCADE)    
#     profit_center_id = models.CharField(max_length=30)
#     return_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
#     status = models.CharField(max_length=25)
#     status_date = models.DateTimeField()













##########################
##########################
####### ACCOUNTING #####
########   AND  ########
#####    FINCACE #######
#######################
class PurchaseOrderLines(models.Model):
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    purchase_order_id = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    catalog_id = models.ForeignKey(Catalog, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    varient_id = models.ForeignKey(Varient, on_delete=models.CASCADE)
    supplier_id = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=150)
    sku = models.CharField(max_length=20)
    uom = models.CharField(max_length=15)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    order_quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    rec_quanity = models.IntegerField()
    status = models.CharField(max_length=25)
    status_date = models.DateTimeField(auto_now_add=True)


class ExpenseTypes(models.Model):
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    expense_type = models.CharField(max_length=100)
    status = models.CharField(max_length=25)
    status_date = models.DateTimeField()

def current_year():
    return datetime.date.today().year

def max_value_current_year(value):
    return MaxValueValidator(current_year())(value) 

def year_choices():
    return [(r,r) for r in range(1984, datetime.date.today().year+1)]

class MyForm(forms.ModelForm):
    year = forms.TypedChoiceField(coerce=int, choices=year_choices, initial=current_year)

class Expense(models.Model):
    MONTH_CHOICES = [(str(i), calendar.month_name[i]) for i in range(1,13)]
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    expense_type_id = models.ForeignKey(ExpenseTypes, on_delete=models.CASCADE)
    cost_center = models.CharField(max_length=30)
    expense_year = models.IntegerField(validators=[MinValueValidator(1984), max_value_current_year])
    expense_month = models.IntegerField(choices=MONTH_CHOICES, default='1')
    description = models.CharField(max_length=150)
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    created_by = models.CharField(max_length=30)
    approved_by = models.CharField(max_length=30)
    approved_on = models.DateTimeField()
    status = models.CharField(max_length=25)
    status_date = models.DateTimeField()

class AccountsPayable(models.Model):
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    cost_center = models.CharField(max_length=30)
    payable_type = models.CharField(max_length=50)
    document_type = models.CharField(max_length=50)
    document_number = models.CharField(max_length=50)
    reference_num = models.CharField(max_length=30)
    total_payable = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    due_date = models.DateTimeField()
    paid_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    # balance = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    paid_on = models.DateTimeField()
    update_by = models.CharField(max_length=30)
    status = models.CharField(max_length=25)
    status_date = models.DateTimeField()

    @property
    def Balanc(self):
        return self.total_payable - self.paid_amount
# This is payment made for a supplier
class PaymentVoucher(models.Model):
    CASH = "Cash"
    CREDIT = "Credit"
    DEBIT = "Debit"
    TRANSFER = "Bank Tranfer"
    CHECK = "Check"
    PAYPAL = "Paypal"
    PORTAL = "Online Portal"
    PAYMENT_TYPE_CHOICES = [
        ("CASH", "Cash"),
        ("CREDIT", "Credit"),
        ("DEBIT", "Debit"),
        ("TRANSFER", "Bank Tranfer"),
        ("CHECK", "Check"),
        ("PAYPAL", "Paypal"),
        ("PORTAL", "Online Portal")
    ]
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    account_payable_id =  models.ForeignKey(AccountsPayable, on_delete=models.CASCADE)
    total_due = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    total_paid = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    paid_on = models.DateTimeField()
    payment_channel = models.CharField(max_length=15, choices=PAYMENT_TYPE_CHOICES, default=CASH)
    payment_document = models.CharField(max_length=100, null=True, blank=True)
    payment_doc_validity = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=25)
    status_date = models.DateTimeField()

class AccountReceivables(models.Model):
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    profit_center = models.CharField(max_length=25)
    revenue_type = models.CharField(max_length=100)
    document_type = models.CharField(max_length=25)
    document_number = models.CharField(max_length=50)
    total_receivable_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    received_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    # balance = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    received_on = models.DateTimeField()
    updated_by = models.CharField(max_length=100)
    status = models.CharField(max_length=25)
    status_date = models.DateTimeField()

    @property
    def Balance(self):
        return self.total_receivable_amount - self.received_amount
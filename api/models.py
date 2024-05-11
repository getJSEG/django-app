from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, PermissionsMixin, AbstractBaseUser, BaseUserManager
from django import forms 
from django.core.validators import MaxValueValidator, MinValueValidator
from .helper import store_number_generator
from django_resized import ResizedImageField
from sorl.thumbnail import ImageField, get_thumbnail
import os
import uuid
import datetime
import calendar

def get_upload_path(instance, filename):
    old_filename = filename
    filename = "%s%s" % ('product', old_filename)
    return os.path.join('varients/', filename)

#FAT MODELS THIN VIEWS
class Locations(models.Model):
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
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150,  null=True, blank=True)
    password = models.CharField(max_length=255, null=False, blank=False)
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    create_on = models.DateTimeField(auto_now_add=True)
    date_joined  = models.DateTimeField(auto_now_add=True)
    status_date = models.DateTimeField(auto_now_add=True)
    location = models.ForeignKey(Locations, on_delete=models.CASCADE, null=True, blank=True)
    avatar = ResizedImageField(size=[350, 350], upload_to='user', blank=True, null=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name']

    def __str__(self):
        return self.username

# user activity Here
class UserActivity(models.Model):
    location_id = models.ForeignKey(Locations, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=60)
    ref_doc_number = models.CharField(max_length=12)
    description = models.CharField(max_length=255)
    action_type = models.CharField(max_length=30)
    action_on = models.DateTimeField(max_length=60)
    actioned_by = models.CharField(max_length=60)

class Customer(models.Model):
    location_id = models.ForeignKey(Locations, on_delete=models.CASCADE)
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
    location_id = models.ForeignKey(Locations, on_delete=models.CASCADE)
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
    location_id = models.ForeignKey(Locations, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    cost_center = models.CharField(max_length=25, blank=True)
    created_by = models.CharField(max_length=100)
    approved_by = models.CharField(max_length=100)
    status = models.CharField(max_length=25)
    status_date = models.DateTimeField(auto_now_add=True)

# PRODUCTS
# RENAME PRODICT TO CATEGORIES
class Products(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    location_id = models.ForeignKey(Locations, on_delete=models.CASCADE)
    categorie = models.CharField(max_length=60)
    brand = models.CharField(max_length=60)
    create_on = models.DateTimeField(auto_now_add=True)
    product_acronym = models.CharField(max_length=10, null=True, blank=True) 
    status = models.ImageField(max_length=25, null=True, blank=True)
    status_date = models.DateTimeField(auto_now_add=True)
 
class ImageAlbum(models.Model):
    def default(self):
        return self.images.filter(default=True).first()
    def thumnail(self):
        return self.images.filter(width__lt=100, length_lt=100)

# Product varient colors
class VarientColors(models.Model):
    color = ResizedImageField(size=[100, 100], upload_to="colors", blank=True, null=True)
    description = models.CharField(max_length=100)
    album = models.ForeignKey(ImageAlbum, related_name='varient_colors', on_delete=models.CASCADE)

# Product varient images for males and female models
class VarientImages(models.Model):
    image = ResizedImageField(size=[1000, 1500], upload_to=get_upload_path, blank=True, null=True)
    album = models.ForeignKey(ImageAlbum, related_name='images', on_delete=models.CASCADE)

# product Varients
class Varients(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    location_id = models.ForeignKey(Locations, on_delete=models.CASCADE, null=True, blank=True)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=60, null=True, blank=True)
    vendor_sku = models.CharField(max_length=100)
    size = models.CharField(max_length=10)
    sku = models.CharField(max_length=100, unique=True)
    album = models.OneToOneField(ImageAlbum, related_name='model', on_delete=models.CASCADE, null=True)
    units = models.IntegerField()
    purchase_price = models.DecimalField(max_digits=8, decimal_places=2)
    listed_price = models.DecimalField(max_digits=8, decimal_places=2)
    storage_location = models.CharField(max_length=100, null=True, blank=True)
    create_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=25)
    status_date = models.DateTimeField(auto_now_add=True)

    @property
    def cal_purchase_price(self):
        price = self.units * self.listed_price
        return '${}'.format(price)

class TopSellingItems(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    location_id = models.ForeignKey(Locations, on_delete=models.CASCADE, null=True, blank=True)
    varient_Id = models.ForeignKey(Varients, on_delete=models.CASCADE, null=True, blank=True )
    quatitySold =  models.IntegerField()

class Tags(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    location_id = models.ForeignKey(Locations, on_delete=models.CASCADE, null=True, blank=True)
    tag = models.CharField(max_length=100, unique=True) 


class Discount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    location = models.ForeignKey(Locations, on_delete=models.CASCADE, null=True, blank=True)
    discount_code = models.CharField(max_length=56, unique=True)
    discount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, null=True, blank=True)
    expiration = models.DateTimeField()
    description = models.CharField(max_length=100)
    status_date = models.DateTimeField(auto_now_add=True)

class Catalogs(models.Model):
    location_id = models.ForeignKey(Locations, on_delete=models.CASCADE)
    catalog_name = models.CharField(max_length=100)
    varient_id = models.ForeignKey(Varients, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

class PurchaseOrderLines(models.Model):
    location_id = models.ForeignKey(Locations, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    purchase_order_id = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    catalog_id = models.ForeignKey(Catalogs, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    varient_id = models.ForeignKey(Varients, on_delete=models.CASCADE)
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

class StockTranfer(models.Model):
    location_id = models.ForeignKey(Locations, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    varient_id = models.ForeignKey(Varients, on_delete=models.CASCADE)
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

#############
#############
# SALES MANAGEMENT ######
#######
##########
 
class SalesOrder(models.Model):
    PHYSICAL = "physical_retail"
    ONLINE = "Online"
    ORDER_TYPES_CHOICES = [
        ("PHYSICAL_STORE", "physical_retail"),
        ("ONLINE", "Online"),
    ]
    location_id = models.ForeignKey(Locations, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    profit_center = models.CharField(max_length=25)
    order_type = models.CharField(max_length=15, choices=ORDER_TYPES_CHOICES, default=PHYSICAL)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    invoice_status = models.CharField(max_length=30)
    created_by = models.CharField(max_length=100)
    status = models.CharField(max_length=25)
    status_date = models.DateTimeField()

class SalesOrderLines(models.Model):
    location_id = models.ForeignKey(Locations, on_delete=models.CASCADE)
    order_id = models.ForeignKey(SalesOrder, on_delete=models.CASCADE)
    varient_id = models.ForeignKey(Varients, on_delete=models.CASCADE)
    sku = models.CharField(max_length=20)
    item_name = models.CharField(max_length=100)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_on = models.DateTimeField(auto_now_add=True)
    status_date = models.DateTimeField()

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

    location_id = models.ForeignKey(Locations, on_delete=models.CASCADE)
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

    location_id = models.ForeignKey(Locations, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    return_order_id = models.ForeignKey(ReturnOrders, on_delete=models.CASCADE)
    varient_id = models.ForeignKey(Varients, on_delete=models.CASCADE)
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

class Invoice(models.Model):
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
    location_id = models.ForeignKey(Locations, on_delete=models.CASCADE)
    sales_order_id = models.ForeignKey(SalesOrder, on_delete=models.CASCADE)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)                                          
    total_tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, null=True, blank=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    # balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)                                          #
    change = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)                                           #this is the change that should be give to the customer
    cc_authcode= models.CharField(max_length=100, null=True, blank=True)                                                  #this is a authorizarion coe for credit card payment
    payment_type = models.CharField(max_length=15, choices=PAYMENT_TYPE_CHOICES, default=CASH)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    status = models.CharField(max_length=25)
    status_date = models.DateTimeField()

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

class CreditNote(models.Model):
    location_id = models.ForeignKey(Locations, on_delete=models.CASCADE)
    created_on = models.DateTimeField()
    return_order_id = models.ForeignKey(ReturnOrders, on_delete=models.CASCADE)    
    profit_center_id = models.CharField(max_length=30)
    return_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=25)
    status_date = models.DateTimeField()


##########################
##########################
####### ACCOUNTING #####
########   AND  ########
#####    FINCACE #######
#######################
class ExpenseTypes(models.Model):
    location_id = models.ForeignKey(Locations, on_delete=models.CASCADE)
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
    location_id = models.ForeignKey(Locations, on_delete=models.CASCADE)
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
    location_id = models.ForeignKey(Locations, on_delete=models.CASCADE)
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
    location_id = models.ForeignKey(Locations, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    account_payable_id =  models.ForeignKey(AccountsPayable, on_delete=models.CASCADE)
    total_due = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    total_paid = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    paid_on = models.DateTimeField()
    payment_channel = models.CharField(max_length=15, choices=PAYMENT_TYPE_CHOICES, default=CASH)
    payment_document = models.CharField(max_length=100, null=True, blank=True)
    payment_doc_validity = models.CharField(max_length=100)
    status = models.CharField(max_length=25)
    status_date = models.DateTimeField()

class AccountReceivables(models.Model):
    location_id = models.ForeignKey(Locations, on_delete=models.CASCADE)
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


class ReceiteVoucher(models.Model):
    location_id = models.ForeignKey(Locations, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    account_receivable_id = models.ForeignKey(AccountReceivables, on_delete=models.CASCADE)
    total_received = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    received_on = models.DateTimeField()
    status = models.CharField(max_length=25)
    status_date = models.DateTimeField()

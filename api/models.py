from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, PermissionsMixin, AbstractBaseUser, BaseUserManager
from django.db.models import Sum
from django.core.validators import MaxValueValidator, MinValueValidator
from django import forms 

import uuid
from decimal import Decimal


#FAT MODELS THIN VIEWS
# RENAME THIS TO  StoreLocation or StoreNumber
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
    locationType = models.CharField(max_length=50, choices=LOCATION_TYPE_CHOICES, default=RETAIL)
    storeNumber = models.CharField(max_length=60, unique=True)
    incharge = models.CharField(max_length=30)
    email = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=255)
    countryCode = models.CharField(max_length=255, null=True, blank=True)
    currency = models.CharField(max_length=255)
    department = models.CharField(max_length=60, null=True, blank=True)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=60)
    cost_center = models.CharField(max_length=60)
    status = models.CharField(max_length=25)
    tax = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)       #Change name to vat (value_added_tax)
    isPreTax = models.BooleanField(default=False)                                  #This make it that the items already have a tax added to them
    dateCreated = models.DateTimeField(auto_now_add=True)
    
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

class Avatar(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    cf_id = models.CharField(max_length=200, null=True, blank=True)
    link = models.CharField(max_length=200, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

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
    avatar = models.ForeignKey(Avatar, null=True, blank=True, on_delete=models.CASCADE)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name']

    objects = CustomAccountManager()

    def __str__(self):
        return self.username

# user activity Here
# class UserActivity(models.Model):
#     location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
#     transaction_type = models.CharField(max_length=60)
#     ref_doc_number = models.CharField(max_length=12)
#     description = models.CharField(max_length=255)
#     action_type = models.CharField(max_length=30)
#     action_on = models.DateTimeField(max_length=60)
#     actioned_by = models.CharField(max_length=60)
    
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

####################################################PRODUCT####################################################
###############################################################################################################
###############################################################################################################
class Images(models.Model):
    filename = models.CharField(max_length=200, null=True, blank=True)
    cf_id = models.CharField(max_length=200)
    link = models.CharField(max_length=200)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Categories(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    categorie = models.CharField(max_length=100, unique=True, null=True, blank=True) 

class Tags(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    tag = models.CharField(max_length=100, unique=True, null=True, blank=True) 

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=60)
    cost = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    productAcronym = models.CharField(max_length=10, null=True, blank=True)
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    created_by = models.CharField(max_length=250, null=True, blank=True)
    createdDate = models.DateTimeField(auto_now_add=True)

# product Varient
class Varient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE,)
    color = models.CharField(max_length=100)
    size = models.CharField(max_length=10)
    units = models.PositiveIntegerField()
    minUnits = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    categories = models.ManyToManyField(Categories, related_name="variantCategory", null=True, blank=True)
    vendorSku = models.CharField(max_length=100, null=True, blank=True)
    tags = models.ManyToManyField(Tags, related_name="variantTags", blank=True)
    varientImage = models.ForeignKey(Images, null=True, related_name="varientImage", blank=True, on_delete=models.CASCADE)
    storageLocation = models.CharField(max_length=100, null=True, blank=True)
    sku = models.CharField(max_length=100, unique=True)
    createdDate = models.DateTimeField(auto_now_add=True)

    @property
    def inventoryValue(self):
        price = self.units * self.listed_price
        return '${}'.format(price)
    
    @property
    def outOfStock(self):
        if self.units == 0:
            return True
        else:
            return False
    @property
    def lowStock(self):
        if self.units < self.minUnits:
            return True
        else:
            return False
        
class StockTransfer(models.Model):
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



class Discount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    code = models.CharField(max_length=56, unique=True)
    discount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, null=True, blank=True)
    expirationDate = models.DateTimeField()
    description = models.CharField(max_length=100)
    dateCreated = models.DateTimeField(auto_now_add=True)

# TODO: CHANGE Phone = > charfield to Phone number field
class Customer(models.Model):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, null=True, blank=True)
    countryCode = models.CharField(max_length=5, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=30, null=True, blank=True)
    zip_code = models.CharField(max_length=10, null=True, blank=True)

    address = models.CharField(max_length=100, null=True, blank=True)
    extraDetails = models.CharField(max_length=255, null=True, blank=True)
    department = models.CharField(max_length=255, null=True, blank=True)
    municipality = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=25, null=True, blank=True, default="El Salvador")
    dateCreated = models.DateTimeField(auto_now_add=True)

class PaymentMethod(models.Model):
    PAYMENT_TYPE_CHOICES = [
        ("cash", "Efectico"),
        ('credit_card', 'Tarjeta de Credito'),
        ('debit_card', 'Tarjeta de Devito'),
        ('bank_transfer', 'Transferencia'),
    ]
    transactionType = models.CharField(max_length=255, choices=PAYMENT_TYPE_CHOICES)

# Payment Types
class CashPayment(models.Model):
    paymentMethod = models.OneToOneField(PaymentMethod, related_name='cashPaymentMethod', on_delete=models.CASCADE, primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    changeDue = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

class TransferPayment(models.Model):
    paymentMethod = models.OneToOneField(PaymentMethod, related_name='transferPaymentMethod',  on_delete=models.CASCADE, primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    transactionID = models.CharField(max_length=255)

class CreditCardPayment(models.Model):
    paymentMethod = models.OneToOneField(PaymentMethod, related_name='creditcardPaymentMethod', on_delete=models.CASCADE, primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    lastDigits = models.CharField(max_length=255)
    transactionID = models.CharField(max_length=255)

# This is the Parent this is Sales Receipt/Invoice
class SalesReceipt(models.Model):
    OPEN = "Avierto"

    Sales_Choices = [
        ('OPEN', 'Avierto'),
        ("CLOSED", "Cerrado"),
        ("PAID", "Pagado"),
        ("PROCESSING", "procesando"),
        ("CANCELED", "Cancelado"),
        ("RETURN", "RETURNED")
    ]
    paymentExecution_Choices = [
        ('POS', 'POS'),
        ('SHIPPING', 'SHIPPING')
    ]
    status = models.CharField(max_length=25, choices=Sales_Choices, default=OPEN, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    paymentMethod = models.ForeignKey(PaymentMethod, related_name="paymentMethods",on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    discount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, null=True, blank=True)
    shipping = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    totalAmount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    paymentExecution = models.CharField(max_length=25, choices=paymentExecution_Choices, default="POS", null=True, blank=True)
    dateCreated = models.DateTimeField(auto_now_add=True)


class ReceiptLine(models.Model):
    salesReceipt = models.ForeignKey(SalesReceipt, related_name='receiptLines', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    size = models.CharField(max_length=255)
    sku = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)



# Below is all of the shipping models
# TODO: REMOVE null and blank whe in production
class Shipping(models.Model):

    ShippingType = [
        ("personalShipping", "Envio Personalizado"),
        ('parcel', 'Encomienda')
    ]

    shippingReceipts = models.ForeignKey(SalesReceipt, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)

    shippingType = models.CharField(max_length=25, choices=ShippingType)
    attempts = models.IntegerField(default=1, null=True, blank=True)
    companyName = models.CharField(max_length=255)
    details = models.CharField(max_length=255, null=True, blank=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2, default=1.00)

    class Meta:
        abstract = True

class CustomShipping(Shipping):
    PROCESSING = 'procesando'

    Sales_Choices = [
        ('PREPAIDED', 'Pagado'),
        ("PROCESSING", "Procesando"),
        ("SHIPPED", "Enviado"),
        ("DELIVERED", "Entregado"),
        ("RETURN", "DEVOLUCION"),
        ("CANCELED", "Cancelado")
    ]
    status = models.CharField(max_length=25, choices=Sales_Choices, default=PROCESSING)

    
class ParselShipping(Shipping):
    PROCESSING = 'procesando'

    Sales_Choices = [
        ('PREPAIDED', 'Pagado'),
        ("PROCESSING", "Procesando"),
        ("SHIPPED", "Enviado"),
        ("PICKEDUP", "Recojido"),
        ("NOSHOW", "No Retiro"),
        ("RETURN", "DEVOLUCION"),
        ("CANCELED", "Cancelado"),
    ]
    status = models.CharField(max_length=25, choices=Sales_Choices, default=PROCESSING, null=True, blank=True)









# Accounting
# All the current store  Expenses
class Expense(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    created_by = models.CharField(max_length=30)
    currency = models.CharField(max_length=5, default="USD")
    note = models.CharField(blank=True, null=True)
    totalAmount = models.DecimalField(max_digits=10, decimal_places=2)
    creationDate = models.DateTimeField(auto_now_add=True)

# TODO: REMOVE LOCATION_ID
class ExpenseTypes(models.Model):

    expense = models.ForeignKey(Expense, related_name='expenses', on_delete=models.CASCADE)
    description = models.CharField(max_length=150)
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    isReimbursable = models.BooleanField(default=False)
    isACHReimbursed = models.BooleanField(default=False)
    merchant = models.CharField(max_length=30, blank=True, null=True)
    expense_date = models.DateTimeField()
    expense_type = models.CharField(max_length=100)


# Alll purchase orders from current store
class PurchaseOrder(models.Model):
    PROCESSING = "Procesando"
    purchaseOrder_Choices = [
        ('ONHOLD', 'En Espera'),
        ("PROCESSING", "Procesando"),
        ("PAID", "Pagado"),
        ("SHIPPED", "Enviado"),
        ("DELIVERED", "Entregado"),
        ("CANCELED", "Cancelado")
    ]

    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    createdOn = models.DateTimeField(auto_now_add=True)
    supplierId = models.ForeignKey(Supplier, on_delete=models.CASCADE, blank=True, null=True)
    merchant = models.CharField(max_length=255)
    costCenter = models.CharField(max_length=25, blank=True, null=True)
    createdBy = models.CharField(max_length=100)
    totalAmount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=25, choices=purchaseOrder_Choices, default=PROCESSING)
    datePaid = models.DateTimeField(blank=True, null=True)
    statusDate = models.DateTimeField(auto_now_add=True)

class PurchaseOrderLines(models.Model):
    purchaseOrderId = models.ForeignKey(PurchaseOrder, related_name='POLines', on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    sku = models.CharField(max_length=20, blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField(default=1)
    createdOn = models.DateTimeField(auto_now_add=True)
    subtotal = models.DecimalField(max_digits=8, decimal_places=2)


##########################
##########################
####### ACCOUNTING #####
########   AND  ########
#####    FINCACE #######
#######################
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
# Generated by Django 4.2.7 on 2024-04-25 03:39

import api.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountReceivables',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('profit_center', models.CharField(max_length=25)),
                ('revenue_type', models.CharField(max_length=100)),
                ('document_type', models.CharField(max_length=25)),
                ('document_number', models.CharField(max_length=50)),
                ('total_receivable_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('received_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('received_on', models.DateTimeField()),
                ('updated_by', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=25)),
                ('status_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='AccountsPayable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('cost_center', models.CharField(max_length=30)),
                ('payable_type', models.CharField(max_length=50)),
                ('document_type', models.CharField(max_length=50)),
                ('document_number', models.CharField(max_length=50)),
                ('reference_num', models.CharField(max_length=30)),
                ('total_payable', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('due_date', models.DateTimeField()),
                ('paid_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('paid_on', models.DateTimeField()),
                ('update_by', models.CharField(max_length=30)),
                ('status', models.CharField(max_length=25)),
                ('status_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Catalogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('catalog_name', models.CharField(max_length=100)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_on', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=30)),
                ('lastname', models.CharField(max_length=30)),
                ('phone_number', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=75)),
                ('country', models.CharField(max_length=25)),
                ('city', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=30)),
                ('zip_code', models.CharField(blank=True, max_length=10)),
                ('department', models.CharField(blank=True, max_length=30, null=True)),
                ('municipality', models.CharField(blank=True, max_length=30, null=True)),
                ('status', models.ImageField(max_length=25, upload_to='')),
                ('day_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ImageAlbum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Locations',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('location_type', models.CharField(choices=[('WAREHOUSE', 'Warehouse'), ('RETAIL', 'Retail'), ('DISTRIBUTION_CENTER', 'Distribution Center')], default='Retail', max_length=50)),
                ('store_number', models.CharField(max_length=60, unique=True)),
                ('incharge', models.CharField(max_length=30)),
                ('email', models.CharField(blank=True, max_length=100, null=True)),
                ('phone', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.CharField(max_length=255)),
                ('department', models.CharField(blank=True, max_length=60, null=True)),
                ('city', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=60)),
                ('profit_center', models.CharField(max_length=60)),
                ('cost_center', models.CharField(max_length=60)),
                ('status', models.CharField(max_length=25)),
                ('local_tax', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('pre_tax_items', models.BooleanField(default=False)),
                ('status_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=60)),
                ('brand', models.CharField(max_length=60)),
                ('create_on', models.DateTimeField(auto_now_add=True)),
                ('product_acronym', models.CharField(blank=True, max_length=10, null=True)),
                ('status', models.ImageField(blank=True, max_length=25, null=True, upload_to='')),
                ('status_date', models.DateTimeField(auto_now_add=True)),
                ('location_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.locations')),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('cost_center', models.CharField(blank=True, max_length=25)),
                ('created_by', models.CharField(max_length=100)),
                ('approved_by', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=25)),
                ('status_date', models.DateTimeField(auto_now_add=True)),
                ('location_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.locations')),
            ],
        ),
        migrations.CreateModel(
            name='SalesOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('profit_center', models.CharField(max_length=25)),
                ('order_type', models.CharField(choices=[('PHYSICAL_STORE', 'physical_retail'), ('ONLINE', 'Online')], default='physical_retail', max_length=15)),
                ('invoice_status', models.CharField(max_length=30)),
                ('created_by', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=25)),
                ('status_date', models.DateTimeField()),
                ('customer_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.customer')),
                ('location_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.locations')),
            ],
        ),
        migrations.CreateModel(
            name='Varients',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('brand', models.CharField(blank=True, max_length=60, null=True)),
                ('vendor_sku', models.CharField(max_length=100)),
                ('size', models.CharField(max_length=10)),
                ('sku', models.CharField(max_length=100, unique=True)),
                ('units', models.IntegerField()),
                ('purchase_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('listed_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('storage_location', models.CharField(blank=True, max_length=100, null=True)),
                ('create_on', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(max_length=25)),
                ('status_date', models.DateTimeField(auto_now_add=True)),
                ('album', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='model', to='api.imagealbum')),
                ('location_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.locations')),
                ('product_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.products')),
            ],
        ),
        migrations.CreateModel(
            name='VarientImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='JPEG', keep_meta=True, null=True, quality=75, scale=0.5, size=[1000, 1500], upload_to=api.models.get_upload_path)),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='api.imagealbum')),
            ],
        ),
        migrations.CreateModel(
            name='VarientColors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='JPEG', keep_meta=True, null=True, quality=75, scale=0.5, size=[100, 100], upload_to='colors')),
                ('description', models.CharField(max_length=100)),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='varient_colors', to='api.imagealbum')),
            ],
        ),
        migrations.CreateModel(
            name='UserActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(max_length=60)),
                ('ref_doc_number', models.CharField(max_length=12)),
                ('description', models.CharField(max_length=255)),
                ('action_type', models.CharField(max_length=30)),
                ('action_on', models.DateTimeField(max_length=60)),
                ('actioned_by', models.CharField(max_length=60)),
                ('location_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.locations')),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_on', models.DateTimeField(auto_now_add=True)),
                ('supplier_name', models.CharField(max_length=100)),
                ('contact_person', models.CharField(max_length=100)),
                ('contact_title', models.CharField(blank=True, max_length=100, null=True)),
                ('contact_email', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=30)),
                ('city', models.CharField(max_length=35)),
                ('state', models.CharField(max_length=35)),
                ('country', models.CharField(max_length=35)),
                ('address', models.CharField(max_length=100)),
                ('LicenseNumber', models.CharField(max_length=30)),
                ('payment_method', models.CharField(choices=[('CASH', 'Cash'), ('CREDIT', 'Credit'), ('DEBIT', 'Debit'), ('TRANSFER', 'Bank Transfer'), ('CHECK', 'cheque'), ('PAYPAL', 'Paypal')], default='Cash', max_length=15)),
                ('payment_terms', models.IntegerField()),
                ('status', models.CharField(max_length=25)),
                ('status_date', models.DateTimeField(auto_now_add=True)),
                ('location_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.locations')),
            ],
        ),
        migrations.CreateModel(
            name='StockTranfer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('unit_purchase_price', models.DecimalField(decimal_places=2, max_digits=9)),
                ('tranfer_by_location', models.IntegerField()),
                ('tranfer_by_costcenter', models.CharField(max_length=25)),
                ('transfer_qty', models.IntegerField()),
                ('transferred_by', models.CharField(max_length=56)),
                ('tranfer_to_location', models.IntegerField()),
                ('tranfer_to_costcenter', models.CharField(max_length=25)),
                ('received_qty', models.IntegerField()),
                ('received_by', models.CharField(max_length=56)),
                ('status', models.CharField(max_length=25)),
                ('status_date', models.DateTimeField()),
                ('location_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.locations')),
                ('varient_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.varients')),
            ],
        ),
        migrations.CreateModel(
            name='SalesOrderLines',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.CharField(max_length=20)),
                ('item_name', models.CharField(max_length=100)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.IntegerField()),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('status_date', models.DateTimeField()),
                ('location_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.locations')),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.salesorder')),
                ('varient_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.varients')),
            ],
        ),
        migrations.CreateModel(
            name='ReturnOrders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('order_date', models.DateTimeField()),
                ('return_reason', models.CharField(choices=[('ONE', 'Wrong Size'), ('TWO', 'Product Damage'), ('THREE', 'Bank Tranfer'), ('FOUR', 'Other'), ('FIVE', 'Received Wrong Product'), ('SIX', 'No Longer Need'), ('SEVEN', 'Arrived Too Late')], default='Wrong Size', max_length=25)),
                ('approval_status', models.CharField(max_length=50)),
                ('approved_by', models.CharField(max_length=100)),
                ('credit_note', models.CharField(blank=True, max_length=150, null=True)),
                ('return_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_by', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=25)),
                ('status_date', models.DateTimeField()),
                ('location_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.locations')),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.salesorder')),
            ],
        ),
        migrations.CreateModel(
            name='ReturnLines',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('item_name', models.CharField(max_length=30)),
                ('sku', models.CharField(max_length=30)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=9)),
                ('quantity', models.IntegerField()),
                ('condition', models.CharField(choices=[('EXELENT', 'New Condition'), ('GOOD', 'Good Condition'), ('USED', 'Used'), ('BAD', 'Damaged'), ('OTHER', 'Other')], default='Used', max_length=15)),
                ('picture_one', models.ImageField(blank=True, null=True, upload_to='')),
                ('status', models.CharField(max_length=25)),
                ('status_date', models.DateTimeField()),
                ('location_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.locations')),
                ('return_order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.returnorders')),
                ('varient_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.varients')),
            ],
        ),
        migrations.CreateModel(
            name='ReceiteVoucher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('total_received', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('received_on', models.DateTimeField()),
                ('status', models.CharField(max_length=25)),
                ('status_date', models.DateTimeField()),
                ('account_receivable_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.accountreceivables')),
                ('location_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.locations')),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseOrderLines',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('item_name', models.CharField(max_length=150)),
                ('sku', models.CharField(max_length=20)),
                ('uom', models.CharField(max_length=15)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('order_quantity', models.IntegerField()),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('rec_quanity', models.IntegerField()),
                ('status', models.CharField(max_length=25)),
                ('status_date', models.DateTimeField(auto_now_add=True)),
                ('catalog_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.catalogs')),
                ('location_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.locations')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.products')),
                ('purchase_order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.purchaseorder')),
                ('supplier_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.supplier')),
                ('varient_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.varients')),
            ],
        ),
        migrations.CreateModel(
            name='PaymentVoucher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('total_due', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('total_paid', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('paid_on', models.DateTimeField()),
                ('payment_channel', models.CharField(choices=[('CASH', 'Cash'), ('CREDIT', 'Credit'), ('DEBIT', 'Debit'), ('TRANSFER', 'Bank Tranfer'), ('CHECK', 'Check'), ('PAYPAL', 'Paypal'), ('PORTAL', 'Online Portal')], default='Cash', max_length=15)),
                ('payment_document', models.CharField(blank=True, max_length=100, null=True)),
                ('payment_doc_validity', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=25)),
                ('status_date', models.DateTimeField()),
                ('account_payable_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.accountspayable')),
                ('location_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.locations')),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('total_tax', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('grand_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('discount', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=8, null=True)),
                ('amount_paid', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('change', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('cc_authcode', models.CharField(blank=True, max_length=100, null=True)),
                ('payment_type', models.CharField(choices=[('CASH', 'Cash'), ('CREDIT', 'Credit'), ('DEBIT', 'Debit'), ('TRANSFER', 'Bank Transfer'), ('CHECK', 'cheque'), ('PAYPAL', 'Paypal')], default='Cash', max_length=15)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=25)),
                ('status_date', models.DateTimeField()),
                ('location_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.locations')),
                ('sales_order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.salesorder')),
            ],
        ),
        migrations.CreateModel(
            name='ExpenseTypes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('expense_type', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=25)),
                ('status_date', models.DateTimeField()),
                ('location_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.locations')),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('cost_center', models.CharField(max_length=30)),
                ('expense_year', models.IntegerField(validators=[django.core.validators.MinValueValidator(1984), api.models.max_value_current_year])),
                ('expense_month', models.IntegerField(choices=[('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'), ('5', 'May'), ('6', 'June'), ('7', 'July'), ('8', 'August'), ('9', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')], default='1')),
                ('description', models.CharField(max_length=150)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('created_by', models.CharField(max_length=30)),
                ('approved_by', models.CharField(max_length=30)),
                ('approved_on', models.DateTimeField()),
                ('status', models.CharField(max_length=25)),
                ('status_date', models.DateTimeField()),
                ('expense_type_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.expensetypes')),
                ('location_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.locations')),
            ],
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('discount_code', models.CharField(max_length=56, unique=True)),
                ('discount', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=8, null=True)),
                ('expiration', models.DateTimeField()),
                ('description', models.CharField(max_length=100)),
                ('status_date', models.DateTimeField(auto_now_add=True)),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.locations')),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='location_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.locations'),
        ),
        migrations.CreateModel(
            name='CreditNote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField()),
                ('profit_center_id', models.CharField(max_length=30)),
                ('return_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('status', models.CharField(max_length=25)),
                ('status_date', models.DateTimeField()),
                ('location_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.locations')),
                ('return_order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.returnorders')),
            ],
        ),
        migrations.AddField(
            model_name='catalogs',
            name='location_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.locations'),
        ),
        migrations.AddField(
            model_name='catalogs',
            name='product_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.products'),
        ),
        migrations.AddField(
            model_name='catalogs',
            name='varient_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.varients'),
        ),
        migrations.AddField(
            model_name='accountspayable',
            name='location_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.locations'),
        ),
        migrations.AddField(
            model_name='accountreceivables',
            name='location_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.locations'),
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('username', models.EmailField(max_length=254, unique=True)),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(blank=True, max_length=150, null=True)),
                ('password', models.CharField(max_length=50)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('create_on', models.DateTimeField(auto_now_add=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('status_date', models.DateTimeField(auto_now_add=True)),
                ('avatar', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='JPEG', keep_meta=True, null=True, quality=75, scale=0.5, size=[350, 350], upload_to='user')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.locations')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

from datetime import datetime
from django.utils import timezone
from rest_framework import serializers
from django.contrib.auth import authenticate
from drf_extra_fields.fields import Base64ImageField

from ..models import Locations
from ..models import Varients, VarientImages, VarientColors, ImageAlbum 
from ..models import SalesOrderLines, SalesOrder, Invoice, PaymentVoucher

###GETTTING POS System######

class ColorSerealizer(serializers.ModelSerializer):
    description = serializers.CharField()

    class Meta:
        model= VarientColors
        fields = ['description']


class ColorAlbumSerializer(serializers.ModelSerializer):
    varient_colors = ColorSerealizer(many=True)

    class Meta:
        model = ImageAlbum
        fields = ['varient_colors'] 

class GetVarient(serializers.ModelSerializer):
    album = ColorAlbumSerializer()

    class Meta:
        model = Varients
        fields = ['sku', 'name', 'size', 'listed_price', 'album']
        read_only_fields = ['sku', 'name', 'size', 'listed_price', 'album']




# # INVOICES
# class InvoiceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Invoice
#         fields = '__all__'


# payment Voucher
class PaymentVoucherSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentVoucher
        fields = '__all__'


#creating Invoice
class CreateInvoiceSerializer(serializers.ModelSerializer):

    class Meta:
            model = Invoice
            fields = ['location_id', 'sales_order_id', 'subtotal', 'total_tax', 'grand_total',
                      'discount', 'amount_paid', 'change', 'cc_authcode', 'payment_type',
                      'created_by', 'status']
            
    def create(self, validated_data):
        invoice = Invoice.objects.create(**validated_data, status_date = datetime.now(tz=timezone.utc) )
        return invoice
    

class SalesOrderLinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesOrderLines
        fields = ['location_id', 'created_on', 'profit_center', 'order_type', 'invoice_status',
                  'created_by', 'status', 'status_date']

    def create(self, validated_data):
        salesOrder = SalesOrderLines.objects.create(**validated_data, status_date = datetime.now(tz=timezone.utc) )
        return salesOrder
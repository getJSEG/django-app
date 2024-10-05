from datetime import datetime
from django.utils import timezone
from rest_framework import serializers

from ..models import Location
from ..models import Varient, ProductImages, VarientColor, ImageAlbum
from ..models import SalesOrder, SalesOrderLine, TransactionReceipt

###GETTTING POS System######

class ColorSerealizer(serializers.ModelSerializer):
    description = serializers.CharField()

    class Meta:
        model= VarientColor
        fields = ['description']


class ColorAlbumSerializer(serializers.ModelSerializer):
    varient_colors = ColorSerealizer(many=True)

    class Meta:
        model = ImageAlbum
        fields = ['varient_colors'] 

class GetVarient(serializers.ModelSerializer):
    album = ColorAlbumSerializer()

    class Meta:
        model = Varient
        fields = ['sku', 'name', 'size', 'listed_price', 'album']
        read_only_fields = ['sku', 'name', 'size', 'listed_price', 'album']

class TransactionReceiptSerializer(serializers.ModelSerializer):

    class Meta:
        model = TransactionReceipt
        fields = ['id','location_id', 'order', 'amount_received', 'amount', 'order_total', 'transaction_type', 'Auth_code','date_created',
                  'refundable_amount', 'isOnline', 'order_payment_refund_info', 'name_on_card', 'has_refund', 'CcLast4Digits']
    
class SalesOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model= SalesOrder
        fields = ['id', 'location_id', 'order_total_paid', 'subtotal', 'taxes', 'order_total_price', 'created_by', 'status']
        extra_kwargs = {
            'id': {'required': False},
        }

class SalesOrderLineSerializer(serializers.ModelSerializer):

    class Meta:
        model = SalesOrderLine
        fields = ['order_id', 'varient_id', 'price', 'quantity', 'status']

    def create(self, validated_data):
        salesOrder = SalesOrderLine.objects.create(**validated_data)
        return salesOrder
    

# Getting
class GetSalesOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = SalesOrder
        fields = ['id', 'location_id', 'order_total_price', 'status', 'created_by', 'date_created']

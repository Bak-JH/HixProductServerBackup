from rest_framework import serializers
from .models import Product
from order.models import PricingPolicy, BillingInfo

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'description')

class PolicySerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name')
    description = serializers.JSONField(source='product.description')

    class Meta:
        model = PricingPolicy
        fields = ('pricing_id', 'method', 'price', 'product_name', 'description')

class BillingInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingInfo
        fields = ('billing_key', 'card_name', 'card_number')
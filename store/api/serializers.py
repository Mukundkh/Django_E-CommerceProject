from rest_framework import serializers
from store.models import Customer, Product, Order, OrderItem, ShippingAddress

class ProductItemSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

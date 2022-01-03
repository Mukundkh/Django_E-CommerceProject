from rest_framework import serializers
from .models import Product

class ProductItemSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

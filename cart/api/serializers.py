from rest_framework import serializers
from cart.models import Cart, CartItem
from store.models import Product

class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "name",
            "quantity",
            "price",
            "image",
        )

class CartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = ["cart", "product", "quantity"]

class CartItemMiniSerializer(serializers.ModelSerializer):
    product = CartProductSerializer(required=False)

    class Meta:
        model = CartItem
        fields = ["product", "quantity"]

class CartItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["product", "quantity"]


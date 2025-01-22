from rest_framework import serializers
from store.models import Product, Cart, Order, CartProduct

# Product Serializer
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'image', 'category', 'stock_quantity']


# CartProduct Serializer (used to serialize Cart-Product relationships)
class CartProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartProduct
        fields = ['id', 'product', 'quantity']


# Cart Serializer
class CartSerializer(serializers.ModelSerializer):
    products = CartProductSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'products']


# Order Serializer
class OrderSerializer(serializers.ModelSerializer):
    order_details = serializers.JSONField()
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'order_details', 'status', 'total_price', 'created_at']



from rest_framework import serializers
from orders.models import OrderItem


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class CartAddSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    unit_price = serializers.IntegerField()
    quantity = serializers.IntegerField()
    total = serializers.IntegerField()

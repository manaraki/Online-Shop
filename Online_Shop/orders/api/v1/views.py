from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from products.models import Product
from .serializers import OrderDetailSerializer, CartAddSerializer
from orders.models import OrderItem
from ...cart import Cart


class OrderDetail(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, order_id):
        order_items = get_list_or_404(OrderItem, order_id=order_id)
        ser_data = OrderDetailSerializer(instance=order_items, many=True)
        return Response(data=ser_data.data)


class CartAddView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        return Response(data=request.session['cart'])

    def post(self, request):
        cart = Cart(request)
        ser_data = CartAddSerializer(data=request.POST)
        if ser_data.is_valid():
            vd = ser_data.validated_data
            product = get_object_or_404(Product, id=vd['product_id'])
            if str(vd['product_id']) in cart.session['cart'].keys():
                balance = product.quantity - cart.session['cart'][str(vd['product_id'])][vd['quantity']]
            else:
                balance = product.quantity
            if balance >= vd['quantity']:
                cart.add(product, vd['quantity'])
            else:
                return Response(f'Sorry! available quantity is: {balance}')
            return Response(data=ser_data.data)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

from django.urls import path
from . import views

urlpatterns = [
    path('order/<int:order_id>/', views.OrderDetail.as_view(), name='user_order_api'),
    path('order/cart/add/',views.CartAddView.as_view(),name='user_cart_add_api'),
]

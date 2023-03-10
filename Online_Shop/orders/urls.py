from django.urls import path,include
from . import views

app_name = 'orders'
urlpatterns = [
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/add/<int:product_id>/', views.CartAddView.as_view(), name='cart_add'),
    path('cart/add/<int:product_id>/plus/',views.CartPlusView.as_view(),name='cart_plus'),
    path('cart/add/<int:product_id>/minus/',views.CartMinusView.as_view(),name='cart_minus'),
    path('cart/remove/<int:product_id>/',views.CartRemoveView.as_view(),name='cart_remove'),
    path('create/',views.OrderCreateView.as_view(),name='order_create'),
    path('detail/<int:order_id>/',views.OrderDetailView.as_view(),name='order_detail'),
    path('coupon/<int:order_id>/',views.CouponApplyView.as_view(),name='apply_coupon'),
    path('<int:order_id>/address/',views.OrderAddressView.as_view(),name='order_address'),
    path('<int:order_id>/address/add/',views.OrderAddAddressView.as_view(),name='order_add_address'),
    path('api/v1/',include('orders.api.v1.urls')),
]

from django.urls import path,include
from . import views

app_name = 'accounts'
urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('verify/', views.UserRegisterVerifyCodeView.as_view(), name='verify_code'),
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('logout/', views.UserLogoutView.as_view(), name='user_logout'),
    path('profile/<int:user_id>/', views.UserProfileView.as_view(), name='user_profile'),
    path('profile/<int:pk>/personal-info/',views.PersonalInfoUpdateView.as_view(),name='user_pesonal_info'),
    path('profile/<int:user_id>/addresses/',views.AddressListView.as_view(),name='user_addresses'),
    path('profile/<int:user_id>/addresses/<int:pk>/',views.AddressUpdateView.as_view(),name='user_address_update'),
    path('profile/<int:user_id>/addresses/add/',views.AddressCreateView.as_view(),name='user_address_add'),
    path('profile/<int:user_id>/orders/',views.OrderView.as_view(),name='user_orders'),
    path('profile/<int:user_id>/orders/current/',views.CurrentOrderView.as_view(),name='user_order_current'),
    path('profile/<int:user_id>/orders/posted/',views.PostedOrderView.as_view(),name='user_order_posted'),
    path('profile/<int:user_id>/orders/delivered/',views.DeliveredOrderView.as_view(),name='user_order_delivered'),
    path('profile/<int:user_id>/orders/detail/<int:order_id>/',views.OrderDetailView.as_view(),name='user_order_detail'),
    path('api/v1/',include('accounts.api.v1.urls')),
]

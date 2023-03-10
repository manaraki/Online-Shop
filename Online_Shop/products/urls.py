from django.urls import path
from . import views

app_name = 'products'
urlpatterns = [
    path('', views.ShopView.as_view(), name='home'),
    path('category/<int:pk>/sub_categories/', views.SubCategoryView.as_view(), name='sub_category'),
    path('category/<int:pk>/sub_categories/products/', views.ProductView.as_view(), name='products'),
    path('products/product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
]

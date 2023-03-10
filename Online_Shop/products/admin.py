from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from accounts.admin import product_manager_group, supervisor_group
from .models import Product, Category, Discount


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['type', 'value']


# add permissions to defined groups
ct_product = ContentType.objects.get_for_model(Product)
product_permissions = Permission.objects.filter(content_type=ct_product)
for perm in product_permissions:
    product_manager_group.permissions.add(perm)
    if perm.codename == "view_product":
        supervisor_group.permissions.add(perm)

ct_category = ContentType.objects.get_for_model(Category)
category_permissions = Permission.objects.filter(content_type=ct_category)
for perm in category_permissions:
    product_manager_group.permissions.add(perm)
    if perm.codename == "view_category":
        supervisor_group.permissions.add(perm)

ct_discount = ContentType.objects.get_for_model(Discount)
discount_permissions = Permission.objects.filter(content_type=ct_discount)
for perm in discount_permissions:
    product_manager_group.permissions.add(perm)
    if perm.codename == "view_discount":
        supervisor_group.permissions.add(perm)

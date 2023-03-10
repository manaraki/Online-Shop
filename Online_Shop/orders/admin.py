from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .models import Order, OrderItem, Coupon
from accounts.admin import operator_group, supervisor_group


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product', ]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'updated', 'paid']
    list_filter = ['paid', 'updated']
    inlines = [OrderItemInline, ]


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount', 'valid_from', 'valid_to', 'is_active']


# add permissions to defined groups
ct_order = ContentType.objects.get_for_model(Order)
order_permissions = Permission.objects.filter(content_type=ct_order)
for perm in order_permissions:
    operator_group.permissions.add(perm)
    if perm.codename == "view_order":
        supervisor_group.permissions.add(perm)

ct_coupon = ContentType.objects.get_for_model(Coupon)
coupon_permissions = Permission.objects.filter(content_type=ct_coupon)
for perm in coupon_permissions:
    operator_group.permissions.add(perm)
    if perm.codename == "view_coupon":
        supervisor_group.permissions.add(perm)

from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext as _
from django.db import models
from accounts.models import User, Address
from products.models import Product


class Order(models.Model):
    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
        ordering = ('paid',)

    order_status = [
        ('PRE', 'preparation'),
        ('POS', 'posted'),
        ('DEL', 'delivered')]
    user = models.ForeignKey(User, verbose_name=_('user'), on_delete=models.CASCADE, related_name='orders')
    address = models.CharField(verbose_name=_('address'), max_length=1000, null=True, blank=True)
    paid = models.BooleanField(verbose_name=_('paid'), default=False)
    status = models.CharField(verbose_name=_('status'), max_length=3, choices=order_status, default='PRE')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    discount = models.IntegerField(verbose_name=_('discount'), blank=True, null=True, default=0)

    def __str__(self):
        return f'{self.user}-{self.id}'

    def get_total_price(self):
        total = sum(item.get_cost() for item in self.items.all())
        return int(total * (100 - self.discount) / 100)


class OrderItem(models.Model):
    class Meta:
        verbose_name = _('Order Item')
        verbose_name_plural = _('Order Items')

    order = models.ForeignKey(Order, verbose_name=_('Order'), on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, verbose_name=_('Product'), on_delete=models.CASCADE)
    unit_price = models.IntegerField(verbose_name=_('Unit Price'))
    quantity = models.IntegerField(verbose_name=_('Quantity'), default=1)

    def __str__(self):
        return f'{self.id}'

    def get_cost(self):
        return self.unit_price * self.quantity


class Coupon(models.Model):
    class Meta:
        verbose_name = _('Coupon')
        verbose_name_plural = _('Coupons')

    code = models.CharField(verbose_name=_('Code'), max_length=10, unique=True)
    discount = models.IntegerField(verbose_name=_('Discount'), validators=[MinValueValidator(0), MaxValueValidator(90)])
    valid_from = models.DateTimeField(verbose_name=_('valid from'))
    valid_to = models.DateTimeField(verbose_name=_('valid to'))
    is_active = models.BooleanField(verbose_name=_('active'), default=False)

    def __str__(self):
        return self.code

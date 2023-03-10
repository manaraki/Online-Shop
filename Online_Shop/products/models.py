from django.db import models
from django.utils.translation import gettext as _
from datetime import datetime
import pytz


class Category(models.Model):
    class Meta:
        ordering = ('name',)
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    sub_category = models.ForeignKey('self', verbose_name=_('sub category of'), on_delete=models.CASCADE,
                                     related_name='scategory', null=True, blank=True)
    is_sub = models.BooleanField(verbose_name=_('is sub category'), default=False)
    name = models.CharField(verbose_name=_('name'), max_length=50)
    image = models.ImageField(verbose_name=_('image'), upload_to='products/categories/img/%Y/%m', blank=True, null=True)

    @property
    def sub_categories(self):
        return self.sub_category

    def __str__(self):
        return self.name


class Discount(models.Model):
    class Meta:
        verbose_name = _('Discount')
        verbose_name_plural = _('Discounts')

    type = models.CharField(verbose_name=_('type'), max_length=3, choices=[('val', 'value'), ('per', 'percent')])
    value = models.IntegerField(verbose_name=_('value'))
    start_date = models.DateTimeField(verbose_name=_('start'))
    end_date = models.DateTimeField(verbose_name=_('end'))

    @property
    def is_active(self):
        now = datetime.now(tz=pytz.timezone('Asia/Tehran'))
        if self.start_date <= now and self.end_date >= now:
            return True
        return False

    def __str__(self):
        return f'{self.type}-{self.value}'


class Product(models.Model):
    class Meta:
        ordering = ('name',)
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    category = models.ManyToManyField(Category, verbose_name=_('category'), related_name='products')
    name = models.CharField(verbose_name=_('name'), max_length=100)
    image = models.ImageField(verbose_name=_('image'), upload_to='products/products/img/%Y/%m')
    description = models.TextField(verbose_name=_('description'))
    initial_price = models.IntegerField(verbose_name=_('initial price'))
    quantity = models.IntegerField(verbose_name=_('quantity'))
    discount_obj = models.ForeignKey(Discount, verbose_name=_('discount'), on_delete=models.CASCADE, blank=True,
                                     null=True)
    created = models.DateTimeField(verbose_name=_('created'), auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('updated'), auto_now=True)

    @property
    def price(self):
        return self.initial_price - self.discount

    @property
    def discount(self):
        if self.discount_obj and self.discount_obj.type == 'val' and self.discount_obj.is_active:
            return self.discount_obj.value
        elif self.discount_obj and self.discount_obj.type == 'per' and self.discount_obj.is_active:
            return int(self.initial_price * self.discount_obj.value / 100)
        else:
            return 0

    def update_quantity(self, quantity):
        self.quantity -= quantity
        self.save()

    def __str__(self):
        return self.name

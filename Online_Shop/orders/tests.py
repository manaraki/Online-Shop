from django.test import TestCase
from .models import Order, OrderItem
from accounts.models import User
from products.models import Product


class OrderTestCase(TestCase):
    def setUp(self) -> None:
        user = User.objects.create(first_name='fname4', last_name='lname4', email='email4@email.com',
                                   phone_number='09124444444')

        Order.objects.create(user_id=user.id, paid=False, created='2023-02-12 19:54:20.339126+03:30',
                             updated='2023-02-12 19:54:20.339126+03:30')


    def test_order(self):
        order = Order.objects.get(id=2)
        self.assertEqual(order.__str__(), 'fname4' + ' ' + 'lname4' + '-' + '2')


class OrderItemTestCase(TestCase):
    def setUp(self) -> None:
        user = User.objects.create(first_name='fname5', last_name='lname5', email='email5@email.com',
                                   phone_number='09125555555')
        order = Order.objects.create(user_id=user.id, paid=False, created='2023-02-02 19:54:20.339126+03:30',
                                     updated='2023-02-02 19:54:20.339126+03:30')
        product = Product.objects.create(name='prod2', description='product2', image='products/2023/download.jfif',
                                         created='2023-03-02 19:54:20.339126+03:30',
                                         updated='2023-03-02 19:54:20.339126+03:30',
                                         initial_price=1000, quantity=10, discount_obj=None)

        OrderItem.objects.create(order=order, product=product, unit_price=1000, quantity=1)

    def test_order_item(self):
        item = OrderItem.objects.get(id=1)
        self.assertEqual(item.__str__(), str(1))

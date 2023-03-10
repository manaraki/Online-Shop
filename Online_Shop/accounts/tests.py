from django.test import TestCase
from .models import Address, User


class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(first_name='fname1', last_name='lname1', email='email1@email.com',
                            phone_number='09127654321')
        User.objects.create(first_name='fname2', last_name='lname2', email='email2@email.com',
                            phone_number='09127654322')

    def test_user(self):
        user1 = User.objects.get(first_name='fname1')
        user2 = User.objects.get(first_name='fname2')
        self.assertEqual(user1.__str__(), 'fname1' + ' ' + 'lname1')
        self.assertEqual(user2.__str__(), 'fname2' + ' ' + 'lname2')


class AddressTestCase(TestCase):
    def setUp(self):
        User.objects.create(first_name='fname', last_name='lname', email='email@email.com',
                            phone_number='09121111111')
        Address.objects.create(user_id=1, city="city1", street="street1", alley='alley1', number='num1', floor=1)

    def test_address(self):
        address1 = Address.objects.get(city="city1")
        self.assertEqual(address1.__str__(), str(address1.id))




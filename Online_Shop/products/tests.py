# test with TestCase
from django.test import TestCase
from .models import Category, Product


class CategoryTestCase(TestCase):
    def setUp(self) -> None:
        Category.objects.create(is_sub=False, name='cat1')
        Category.objects.create(is_sub=True, name='cat2')

    def test_category(self):
        category1 = Category.objects.get(name='cat1')
        category2 = Category.objects.get(name='cat2')
        self.assertEqual(category1.__str__(), category1.name)
        self.assertEqual(category2.__str__(), category2.name)


class ProductTestCase(TestCase):
    def setUp(self) -> None:
        Product.objects.create(name='prod1', description='product1', image='products/2023/download.jfif',
                               created='2023-02-02 19:54:20.339126+03:30', updated='2023-02-02 19:54:20.339126+03:30',
                               initial_price=1000, quantity=10, discount_obj=None)

    def test_product(self):
        product = Product.objects.get(name='prod1')
        self.assertEqual(product.__str__(), 'prod1')


# test with selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from django.test import LiveServerTestCase


class HomeTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_home(self):
        self.browser.get(self.live_server_url + '/')
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('Categories', body.text)

from django.shortcuts import render, HttpResponse, get_object_or_404, get_list_or_404
from django.views import View
from .models import Category, Product
from orders.forms import CartAddForm


class ShopView(View):
    template_name = 'products/categories.html'

    def get(self, request):
        categories = Category.objects.filter(is_sub=False)
        return render(request, self.template_name, {'categories': categories})


class SubCategoryView(View):
    template_name = 'products/scategories.html'

    def get(self, request, pk):
        scategories = Category.objects.filter(sub_category_id=pk)
        return render(request, self.template_name, {'scategories': scategories})


class ProductView(View):
    template_name = 'products/products.html'

    def get(self, request, pk):
        category = Category.objects.get(pk=pk)
        # products=get_list_or_404(Product,category=category)
        products = Product.objects.filter(category=category)
        return render(request, self.template_name, {'products': products})


class ProductDetailView(View):
    template_name = 'products/product_detail.html'

    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        form = CartAddForm()
        return render(request, self.template_name, {'product': product, 'form': form})

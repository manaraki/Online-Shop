from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from .cart import Cart
from products.models import Product
from .forms import CartAddForm, CouponApplyForm
from .models import Order, OrderItem, Coupon
from accounts.models import Address, User
from datetime import datetime
import pytz


class CartView(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, 'orders/cart.html', {'cart': cart})


class CartAddView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        if str(product_id) in cart.session['cart'].keys():
            balance = product.quantity - cart.session['cart'][str(product_id)]['quantity']
        else:
            balance = product.quantity
        form = CartAddForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if balance >= cd['quantity']:
                cart.add(product, cd['quantity'])
            else:
                messages.info(request, f'Sorry! available quantity is: {balance}')
        return redirect('products:home')


class CartPlusView(View):
    def get(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.add(product, quantity=1)
        return redirect('orders:cart')


class CartMinusView(View):
    def get(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.add(product, quantity=-1)
        return redirect('orders:cart')


class CartRemoveView(View):
    def get(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return redirect('orders:cart')


class OrderCreateView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user)
        for item in cart:
            OrderItem.objects.create(order=order, product=item['product'], unit_price=item['price'],
                                     quantity=item['quantity'])
            product = item['product']
            product.update_quantity(item['quantity'])
        cart.clear()
        return redirect('orders:order_detail', order.id)


class OrderDetailView(LoginRequiredMixin, View):
    form_class = CouponApplyForm

    def setup(self, request, *args, **kwargs):
        self.order = get_object_or_404(Order, id=kwargs['order_id'])
        self.user = self.order.user
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        # check if user logged in before
        if not request.user.is_authenticated:
            messages.error(request, 'you must log in first')
            return redirect('accounts:user_login')
        elif self.user.id != request.user.id:
            messages.success(request, 'you are not allowed')
            return redirect('products:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        return render(request, 'orders/order.html', {'order': order, 'form': self.form_class})


class CouponApplyView(LoginRequiredMixin, View):
    form_class = CouponApplyForm

    def post(self, request, order_id):
        now = datetime.now(tz=pytz.timezone('Asia/Tehran'))
        form = self.form_class(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                coupon = Coupon.objects.get(code__exact=code, valid_from__lte=now, valid_to__gte=now, is_active=True)
            except Coupon.DoesNotExist:
                messages.error(request, 'code is not valid!', 'danger')
                return redirect('orders:order_detail', order_id)
            order = Order.objects.get(id=order_id)
            order.discount = coupon.discount
            order.save()
        return redirect('orders:order_detail', order_id)


class OrderAddressView(LoginRequiredMixin, View):
    def setup(self, request, *args, **kwargs):
        self.user_addresses = Address.objects.filter(user=request.user)
        return super().setup(request, *args, **kwargs)

    def get(self, request, order_id):
        return render(request, 'orders/order_address.html', {'addresses': self.user_addresses, 'order_id': order_id})

    def post(self, request, order_id):
        address = request.POST['address']
        if address:
            order = get_object_or_404(Order, id=order_id)
            order.address = address
            order.save()
            messages.success(request, 'your address successfully registered.')
            return render(request, 'orders/order_to_pay.html')
        messages.warning(request, 'select your address')
        return render(request, 'orders/order_address.html', {'addresses': self.user_addresses, 'order_id': order_id})


class OrderAddAddressView(LoginRequiredMixin, CreateView):
    model = Address
    fields = ['city', 'street', 'alley', 'number', 'floor']
    template_name = 'accounts/address_add.html'

    def setup(self, request, *args, **kwargs):
        self.user = User.objects.get(pk=request.user.id)
        self.order_id = kwargs['order_id']
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        # verify if user is authenticated
        if not request.user.is_authenticated:
            messages.success(request, 'you must log in first')
            return redirect('products:home')
        # verify if user is profile's owner
        elif self.user.id != request.user.id:
            messages.success(request, 'you are not allowed')
            return redirect('products:home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        address = form.save(commit=False)
        address.user_id = self.request.user.id
        return super(OrderAddAddressView, self).form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy('orders:order_address', kwargs={'order_id': self.order_id})

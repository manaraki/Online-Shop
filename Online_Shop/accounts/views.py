from django.contrib import messages
from django.shortcuts import render, redirect, get_list_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import UpdateView, CreateView
from django.urls import reverse_lazy
from .forms import UserCreationForm, UserLoginForm, VerifyCodeForm
from .models import User, OneTimePassword, Address
import random
from utils import send_otp_code
from orders.models import Order, OrderItem


class UserRegisterView(View):
    form_class = UserCreationForm
    template_name = 'accounts/register.html'

    def dispatch(self, request, *args, **kwargs):
        # verify if user is authenticated
        if request.user.is_authenticated:
            return redirect('products:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            random_code = random.randint(1000, 9999)

            # send SMS to verify user
            send_otp_code(cd['phone_number'], random_code)

            OneTimePassword.objects.create(phone_number=cd['phone_number'], code=random_code)
            request.session['user_registration_info'] = {
                'phone_number': cd['phone_number'],
                'email': cd['email'],
                'password': cd['password2']
            }

            return redirect('accounts:verify_code')
        # show validation errors
        return render(request, self.template_name, {'form': form})


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        # verify if user is authenticated
        if request.user.is_authenticated:
            return redirect('products:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['phone_number'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'you are successfully logged in', 'success')
                if self.next:
                    return redirect(self.next)
                return redirect('products:home')
            else:
                messages.error(request, 'phone number or password is wrong', 'warning')
        return render(request, self.template_name, {'form': form})


class UserRegisterVerifyCodeView(View):
    form_class = VerifyCodeForm
    template_name = 'accounts/verify.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        user_session = request.session['user_registration_info']
        code_instance = OneTimePassword.objects.get(phone_number=user_session['phone_number'])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_instance.code:
                User.objects.create_user(user_session['phone_number'], user_session['email'], user_session['password'])
                code_instance.delete()
                messages.success(request, 'you are successfully registered', 'success')
                return redirect('products:home')
            else:
                return render(request, self.template_name)


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('products:home')


class UserProfileView(LoginRequiredMixin, View):
    template_name = 'accounts/profile.html'

    def setup(self, request, *args, **kwargs):
        self.user = User.objects.get(pk=kwargs['user_id'])
        self.address_list = Address.objects.filter(user_id=kwargs['user_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        # verify if user is authenticated
        if not request.user.is_authenticated:
            messages.success(request, 'you must log in first')
            return redirect('products:home')
        # verify if user is profile's owner
        elif self.user.id != request.user.id:
            messages.success(request,'you are not allowed')
            return redirect('products:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'user': request.user})


class PersonalInfoUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'phone_number', 'email']
    template_name = 'accounts/profile.html'

    def setup(self, request, *args, **kwargs):
        self.user = User.objects.get(pk=kwargs['pk'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        # verify if user is authenticated
        if not request.user.is_authenticated:
            messages.success(request, 'you must log in first')
            return redirect('products:home')
        # verify if user is profile's owner
        elif self.user.id != request.user.id:
            messages.success(request,'you are not allowed')
            return redirect('products:home')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('accounts:user_profile', kwargs={'user_id': self.user.id})


class AddressListView(LoginRequiredMixin, View):
    template_name = 'accounts/profile.html'

    def setup(self, request, *args, **kwargs):
        self.user = User.objects.get(pk=kwargs['user_id'])
        self.address_list = Address.objects.filter(user_id=kwargs['user_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        # verify if user is authenticated
        if not request.user.is_authenticated:
            messages.success(request, 'you must log in first')
            return redirect('products:home')
        # verify if user is profile's owner
        elif self.user.id != request.user.id:
            messages.success(request,'you are not allowed')
            return redirect('products:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name,
                      {'address_list': self.address_list, 'new_address': 'Add new Address'})


class AddressUpdateView(LoginRequiredMixin, UpdateView):
    model = Address
    fields = ['city', 'street', 'alley', 'number', 'floor']
    template_name = 'accounts/address_update.html'

    def setup(self, request, *args, **kwargs):
        self.user = User.objects.get(pk=kwargs['user_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        # verify if user is authenticated
        if not request.user.is_authenticated:
            messages.success(request, 'you must log in first')
            return redirect('products:home')
        # verify if user is profile's owner
        elif self.user.id != request.user.id:
            messages.success(request,'you are not allowed')
            return redirect('products:home')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('accounts:user_addresses', kwargs={'user_id': self.user.id})


class AddressCreateView(LoginRequiredMixin, CreateView):
    model = Address
    fields = ['city', 'street', 'alley', 'number', 'floor']
    template_name = 'accounts/address_add.html'

    def setup(self, request, *args, **kwargs):
        self.user = User.objects.get(pk=kwargs['user_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        # verify if user is authenticated
        if not request.user.is_authenticated:
            messages.success(request, 'you must log in first')
            return redirect('products:home')
        # verify if user is profile's owner
        elif self.user.id != request.user.id:
            messages.success(request,'you are not allowed')
            return redirect('products:home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        address = form.save(commit=False)
        address.user_id = self.request.user.id
        return super(AddressCreateView, self).form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy('accounts:user_addresses', kwargs={'user_id': self.user.id})


class OrderView(LoginRequiredMixin, View):
    template_name = 'accounts/profile.html'

    def setup(self, request, *args, **kwargs):
        self.user = User.objects.get(pk=kwargs['user_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        # verify if user is authenticated
        if not request.user.is_authenticated:
            messages.success(request, 'you must log in first')
            return redirect('products:home')
        # verify if user is profile's owner
        elif self.user.id != request.user.id:
            messages.success(request,'you are not allowed')
            return redirect('products:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'orders': 'Orders'})


class CurrentOrderView(LoginRequiredMixin, View):
    template_name = 'accounts/profile.html'

    def setup(self, request, *args, **kwargs):
        self.user = User.objects.get(pk=kwargs['user_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        # verify if user is authenticated
        if not request.user.is_authenticated:
            messages.success(request, 'you must log in first')
            return redirect('products:home')
        # verify if user is profile's owner
        elif self.user.id != request.user.id:
            messages.success(request,'you are not allowed')
            return redirect('products:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, user_id):
        orders = Order.objects.filter(user_id=user_id, status='PRE')
        return render(request, self.template_name, {'orders': 'Orders', 'current_orders': orders})


class PostedOrderView(LoginRequiredMixin, View):
    template_name = 'accounts/profile.html'

    def setup(self, request, *args, **kwargs):
        self.user = User.objects.get(pk=kwargs['user_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        # verify if user is authenticated
        if not request.user.is_authenticated:
            messages.success(request, 'you must log in first')
            return redirect('products:home')
        # verify if user is profile's owner
        elif self.user.id != request.user.id:
            messages.success(request,'you are not allowed')
            return redirect('products:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, user_id):
        orders = Order.objects.filter(user_id=user_id, status='POS')
        return render(request, self.template_name, {'orders': 'Orders', 'posted_orders': orders})


class DeliveredOrderView(LoginRequiredMixin, View):
    template_name = 'accounts/profile.html'

    def setup(self, request, *args, **kwargs):
        self.user = User.objects.get(pk=kwargs['user_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        # verify if user is authenticated
        if not request.user.is_authenticated:
            messages.success(request, 'you must log in first')
            return redirect('products:home')
        # verify if user is profile's owner
        elif self.user.id != request.user.id:
            messages.success(request,'you are not allowed')
            return redirect('products:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, user_id):
        orders = Order.objects.filter(user_id=user_id, status='DEL')
        return render(request, self.template_name, {'orders': 'Orders', 'delivered_orders': orders})


class OrderDetailView(LoginRequiredMixin, View):
    template_name = 'accounts/profile.html'

    def setup(self, request, *args, **kwargs):
        self.user = User.objects.get(pk=kwargs['user_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        # verify if user is authenticated
        if not request.user.is_authenticated:
            messages.success(request, 'you must log in first')
            return redirect('products:home')
        # verify if user is profile's owner
        elif self.user.id != request.user.id:
            messages.success(request,'you are not allowed')
            return redirect('products:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, order_id, *args, **kwargs):
        order_items = get_list_or_404(OrderItem, order_id=order_id)
        return render(request, self.template_name, {'order_items': order_items})

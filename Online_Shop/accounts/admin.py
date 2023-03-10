from django.contrib import admin
from .models import User, Address, OneTimePassword
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['city', 'street']


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ['phone_number', 'email', 'is_admin']
    list_filter = ['is_admin', ]
    readonly_fields = ['last_login', ]
    fieldsets = (
        ('Information', {'fields': ('email', 'phone_number', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_admin', 'groups')}),
    )
    add_fieldsets = (
        ('Information', {'fields': ('email', 'phone_number', 'password1', 'password2')}),
    )
    search_fields = ('email',)
    ordering = ('email',)


@admin.register(OneTimePassword)
class OneTimePasswordAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'code', 'created']


# unregister auth.models.Group
admin.site.unregister(Group)

# define new groups
product_manager_group, created = Group.objects.get_or_create(name="product_manager")
operator_group, created = Group.objects.get_or_create(name="operator")
supervisor_group, created = Group.objects.get_or_create(name="supervisor")

# add permissions to defined groups
ct_user = ContentType.objects.get_for_model(User)
user_permissions = Permission.objects.filter(content_type=ct_user)
for perm in user_permissions:
    operator_group.permissions.add(perm)
    if perm.codename == "view_user":
        supervisor_group.permissions.add(perm)

ct_address = ContentType.objects.get_for_model(Address)
address_permissions = Permission.objects.filter(content_type=ct_address)
for perm in address_permissions:
    operator_group.permissions.add(perm)
    if perm.codename == "view_address":
        supervisor_group.permissions.add(perm)

ct_onetimepassword = ContentType.objects.get_for_model(OneTimePassword)
onetimepassword_permissions = Permission.objects.filter(content_type=ct_onetimepassword)
for perm in onetimepassword_permissions:
    if perm.codename == "view_onetimepassword":
        supervisor_group.permissions.add(perm)
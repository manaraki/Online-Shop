from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext as _
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    first_name = models.CharField(verbose_name=_('first name'), max_length=200, blank=True, null=True)
    last_name = models.CharField(verbose_name=_('last name'), max_length=200, blank=True, null=True)
    email = models.EmailField(verbose_name=_('email'), max_length=255, unique=True)
    phone_number = models.CharField(verbose_name=_('phone number'), max_length=11, validators=[MinLengthValidator(11)],
                                    unique=True)
    is_active = models.BooleanField(verbose_name=_('active'), default=True)
    is_admin = models.BooleanField(verbose_name=_('admin'), default=False)

    # custome user manager
    objects = UserManager()

    # field for user authentication
    USERNAME_FIELD = 'phone_number'

    # fields for createsuperuser
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def has_module_perms(self, app_lable):
        return True

    @property
    def is_staff(self):
        # user who is allowed to enter admin panel
        return self.is_admin or self.is_supervisor or self.is_operator or self.is_product_manager


class Address(models.Model):
    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')

    user = models.ForeignKey(User, verbose_name=_('user'), on_delete=models.CASCADE, related_name='addresses')
    city = models.CharField(verbose_name=_('city'), max_length=50)
    street = models.CharField(verbose_name=_('street'), max_length=50)
    alley = models.CharField(verbose_name=_('alley'), max_length=50)
    number = models.CharField(verbose_name=_('number'), max_length=5)
    floor = models.IntegerField(verbose_name=_('floor'))

    def __str__(self):
        return f'{self.id}'


class OneTimePassword(models.Model):
    class Meta:
        verbose_name = _('One Time Password')
        verbose_name_plural = _('One Time Passwords')

    phone_number = models.CharField(verbose_name=_('phone number'), max_length=11, validators=[MinLengthValidator(11)],
                                    unique=True)
    code = models.PositiveSmallIntegerField(verbose_name=_('code'))
    created = models.DateTimeField(verbose_name=_('created'), auto_now=True)

    def __str__(self):
        return f'{self.phone_number}-{self.code}-{self.created}'

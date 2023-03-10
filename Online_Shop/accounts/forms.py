from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User, OneTimePassword


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'phone_number']

    def clean_email(self):
        # verify if email is unique
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('This email exists already')
        return email

    def clean_phone_number(self):
        # verify if phone number is unique
        phone_number = self.cleaned_data['phone_number']
        user = User.objects.filter(phone_number=phone_number).exists()
        if user:
            raise ValidationError('This phone number exists already')
        # verify if code does not exist already
        OneTimePassword.objects.filter(phone_number=phone_number).delete()
        return phone_number

    def clean_password2(self):
        # check if two passwords match
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError('passwords dont match')
        return cd['password2']

    def save(self, commit=True):
        # save the provided password in hashed password
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    # a form for updating users.
    password = ReadOnlyPasswordHashField(
        help_text='you can change password using <a href=\"../password/\">this form</a>.')

    class Meta:
        model = User
        fields = ['phone_number', 'email', 'password', 'last_login', 'is_admin', 'is_active']


class UserLoginForm(forms.Form):
    phone_number = forms.CharField(max_length=11, min_length=11)
    password = forms.CharField(widget=forms.PasswordInput)


class VerifyCodeForm(forms.Form):
    code = forms.IntegerField()

from django import forms


class CartAddForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=5)


class CouponApplyForm(forms.Form):
    code = forms.CharField(max_length=10, label='Discount Code')

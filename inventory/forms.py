from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from .models import Item, Order


class CreateOrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = [
            'items'
        ]


class BillingForm(forms.Form):
    firstname = forms.CharField(required=True)
    lastname = forms.CharField(required=True)
    phone_number = forms.IntegerField(required=True)
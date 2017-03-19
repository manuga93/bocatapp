from django import forms
from ..models import CreditCard


class CreditCardForm(forms.ModelForm):
    class Meta:
        model = CreditCard
        fields = ('holderName', 'expireMonth', 'expireYear', 'cvv', 'number')

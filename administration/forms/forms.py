from django import forms
from ..models import CreditCard, Allergen


class CreditCardForm(forms.ModelForm):
    class Meta:
        model = CreditCard
        fields = ('holderName', 'expireMonth', 'expireYear', 'cvv', 'number', 'user')

class AllergenForm(forms.ModelForm):
    class Meta:
        model = Allergen
        fields = ('name', 'icon', 'description')

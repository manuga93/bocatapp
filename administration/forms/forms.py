from django import forms
from ..models import CreditCard, Allergen


class CreditCardForm(forms.ModelForm):
    cardExpiry = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(CreditCardForm, self).__init__(*args, **kwargs)
        self.fields['holderName'].label = "Nombre"
        self.fields['expireMonth'].label = "Mes de caducidad"
        self.fields['expireYear'].label = "Ano de caducidad"
        self.fields['cvv'].label = "CVV"
        self.fields['number'].label = "Numero"
        self.fields['user'].label = "Usuario"

    class Meta:
        model = CreditCard
        fields = ('holderName', 'expireMonth', 'expireYear', 'cvv', 'number', 'user')

class AllergenForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AllergenForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Nombre"
        self.fields['icon'].label = "Icono"
        self.fields['description'].label = "Descripcion"

    class Meta:
        model = Allergen
        fields = ('name', 'icon', 'description')

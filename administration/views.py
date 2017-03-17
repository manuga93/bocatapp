from django.shortcuts import render
from forms.forms import CreditCardForm

def creditcard_new(request):
    form = CreditCardForm()
    return render(request, 'creditcard_edit.html', {'form': form})
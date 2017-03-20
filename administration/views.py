from administration.models import CreditCard
from forms.forms import CreditCardForm
from services.CreditCardService import get_cc_type
from django.shortcuts import get_list_or_404, render_to_response, render, redirect, get_object_or_404


def creditcard_new(request):
    form = CreditCardForm(request.POST)
    if request.method == "POST":
        form = CreditCardForm(request.POST)
        if form.is_valid():
            creditCard = form.save(commit=False)
            creditCard.user = request.user
            creditCard.brandName =  get_cc_type(creditCard.number)
            creditCard.save()
            return redirect('creditCard_list')
    else:
        form = CreditCardForm()

    return render(request, 'creditcard_edit.html', {'form': form})

# Vista para el listado de creditCards
def creditCard_list(request):
        creditCards = CreditCard.objects.all()
        return render(request, 'creditCard_list.html', {'creditCards':creditCards})
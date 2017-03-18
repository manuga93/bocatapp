
from forms.forms import CreditCardForm
from django.shortcuts import get_list_or_404, render_to_response, render, redirect, get_object_or_404

def creditcard_new(request):
    form = CreditCardForm(request.POST)




    if request.method == "POST":
        form = CreditCardForm(request.POST)
        if form.is_valid():
            creditCard = form.save(commit=False)
            creditCard.user = request.user
            creditCard.isDeleted = True
            creditCard.save()
            return redirect('administration.views.creditCard_list')
    else:
        form = CreditCardForm()

    return render(request, 'creditcard_edit.html', {'form': form})
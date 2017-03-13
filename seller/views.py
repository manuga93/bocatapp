from django.http import HttpResponse
from seller.models import Product
from django.shortcuts import get_list_or_404, render_to_response

# Create your views here.



def carta(request): #Recibira una id de local def carta(request, local_id)
    productos = Product.objects.all() #productos = get_list_or_404(Producto, fk=local_id)
    return render_to_response('carta.html', 
                                {'productos': productos})
from django.shortcuts import render
from customer.models import ShoppingCart
from django.http import JsonResponse
import datetime



def createShoppingCart(request):
    if request.user.is_authenticated():
        if request.user.has_perm('bocatapp.customer'):
            new_shoppingcart = ShoppingCart(
                customer=request.user,
                moment=datetime.time(),
                checkout=False)
            new_shoppingcart.save()
    else:
        new_shoppingcart = ShoppingCart(
            moment=datetime.time(),
            checkout=False)
        new_shoppingcart.save()
    
    if new_shoppingcart:
        data = {
            'ShoppingCart': new_shoppingcart.pk
        }
    else:
        data = {
            'ShoppingCart': 0
        }
    
    return JsonResponse(data)
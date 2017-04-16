from django.shortcuts import render
from customer.models import ShoppingCart, ShoppingCartLine
from django.http import JsonResponse
import datetime



def createShoppingCart(request):
    now = datetime.datetime.now()
    string_now = now.strftime("%Y-%m-%d %H:%M:%S")

    if request.user.is_authenticated():
        if request.user.has_perm('bocatapp.customer'):
            new_shoppingcart = ShoppingCart(
                customer=request.user,
                moment=now,
                checkout=False)
            new_shoppingcart.save()
    else:
        new_shoppingcart = ShoppingCart(
            moment=now,
            checkout=False)
        new_shoppingcart.save()
    
    if new_shoppingcart:
        data = {
            'ShoppingCart': new_shoppingcart.pk,
            'now': string_now
        }
    else:
        data = {
            'ShoppingCart': 0
        }
    
    return JsonResponse(data)


def updateBadge(request):
    idShoppingCart = request.GET.get('idCart',None)
    numItems = ShoppingCartLine.objects.filter(shoppingCart_id=idShoppingCart).count()
    data = {
        'count': numItems,
    }

    return JsonResponse(data)
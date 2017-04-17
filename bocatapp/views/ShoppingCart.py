from django.shortcuts import render, get_object_or_404, redirect
from customer.models import ShoppingCart, ShoppingCartLine
from django.http import JsonResponse
import datetime
from bocatapp.views import home



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


# Vista del carrito de compra actual del customer logueado
def listShoppingCart(request, pk):
    if request.user.is_authenticated():
        if request.user.has_perm('bocatapp.customer'):  
            shoppingcart = get_object_or_404(ShoppingCart, pk=pk)
            return render(request, 'shoppingcart.html', {'shoppingcart': shoppingcart})
    else:
        shoppingcart = get_object_or_404(ShoppingCart, pk=pk)
        return render(request, 'shoppingcart.html', {'shoppingcart': shoppingcart})
        
    return redirect(home.home)


def addProduct(request):
    idShoppingCart = request.GET.get('idCart',None)
    idProduct = request.GET.get('idProduct',None)
    newQuantity = request.GET.get('quantity',None)
    scLine = ShoppingCartLine.objects.filter(shoppingCart_id=idShoppingCart,product_id=idProduct)
    if scLine:
        scLine.update(quantity = F('quantity')+newQuantity)
    else:
        scLine = ShoppingCartLine(
            quantity=newQuantity,
            product_id=idProduct,
            shoppingCart_id=idShoppingCart)
        scLine.save()

    data = {
        'line': scLine.pk,
    }

    return JsonResponse(data)


def updateBadge(request):
    idShoppingCart = request.GET.get('idCart',None)
    numItems = ShoppingCartLine.objects.filter(shoppingCart_id=idShoppingCart).count()
    data = {
        'count': numItems,
    }

    return JsonResponse(data)
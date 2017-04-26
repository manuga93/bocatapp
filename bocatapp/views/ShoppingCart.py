from django.shortcuts import render, get_object_or_404, redirect
from customer.models import ShoppingCart, ShoppingCartLine
from bocatapp.models import User
from seller.models import Product
from django.http import JsonResponse
from django.db.models import F
import datetime
from bocatapp.views import home



def create_shopping_cart(request):
    if request.user.is_authenticated():
        if request.user.has_perm('bocatapp.customer'):
            new_shoppingcart = ShoppingCart(
                customer=request.user,
                checkout=False)
            new_shoppingcart.save()
    else:
        new_shoppingcart = ShoppingCart(
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

def update_cookie(request):
    idShoppingCart = request.GET.get('idCart',None)
    if request.user.is_authenticated():
        if request.user.has_perm('bocatapp.customer'):
            customer = User.objects.filter(pk=request.user.id)
            shoppingCart = ShoppingCart.objects.filter(customer_id=request.user.id, checkout=False)
            actualShoppingCart = ShoppingCart.objects.filter(pk=idShoppingCart)
            if not shoppingCart:
                actualShoppingCart.update(customer=customer[0])
            else:
                productsShoppingCart = ShoppingCartLine.objects.filter(shoppingCart_id=shoppingCart[0].id)
                productsActualShoppingCart = ShoppingCartLine.objects.filter(shoppingCart_id=idShoppingCart)

                if productsActualShoppingCart and productsActualShoppingCart.count() > 0:
                    if int(idShoppingCart) != int(shoppingCart[0].pk):
                        shoppingCart[0].delete()
                        actualShoppingCart[0].update(customer=customer[0])
                else:
                    if int(idShoppingCart) != int(shoppingCart[0].pk):
                        if actualShoppingCart:
                            actualShoppingCart[0].delete()
                        
                        idShoppingCart = shoppingCart[0].pk
        else:
            actualShoppingCart = ShoppingCart.objects.filter(pk=idShoppingCart)
            actualShoppingCart.delete()
            idShoppingCart = "None"


    data = {
        'cookie': idShoppingCart
    }

    return JsonResponse(data)
    

# Vista del carrito de compra actual del customer logueado
def list_shopping_cart(request, pk):
    if request.user.is_authenticated():
        if request.user.has_perm('bocatapp.customer'):
            shoppingcart = get_object_or_404(ShoppingCart, pk=pk)
            if shoppingcart.customer.pk == request.user.pk:
                return render(request, 'shoppingcart.html', {'shoppingcart': shoppingcart})
    else:
        shoppingcart = get_object_or_404(ShoppingCart, pk=pk)
        return render(request, 'shoppingcart.html', {'shoppingcart': shoppingcart})
        
    return redirect(home.home)


def add_product(request):
    idShoppingCart = request.GET.get('idCart',None)
    idProduct = request.GET.get('idProduct',None)
    newQuantity = request.GET.get('quantity',None)
    
    productsInSC = ShoppingCartLine.objects.filter(shoppingCart_id=idShoppingCart)
    newProduct = get_object_or_404(Product, pk=idProduct)
    sameLocal = 1
    res = False

    data = {
            'add': 'no',
    }

    if productsInSC.count() == 0:
        res = add_to_shoppingcart_line(idShoppingCart, idProduct, newQuantity)
    else:
        for items in productsInSC:
            item = get_object_or_404(Product, pk=items.product_id)
            if newProduct.local_id != item.local_id:
                sameLocal = 0    

        if sameLocal == 1:
            res = add_to_shoppingcart_line(idShoppingCart, idProduct, newQuantity)   

    if res:
        data = {
            'add': 'ok',
        }

    return JsonResponse(data)

def add_to_shoppingcart_line(idShoppingCart, idProduct, newQuantity):
    scLine = ShoppingCartLine.objects.filter(shoppingCart_id=idShoppingCart,product_id=idProduct)
    if scLine:
        scLine.update(quantity = F('quantity')+newQuantity)
    else:
        scLine = ShoppingCartLine(
            quantity=newQuantity,
            product_id=idProduct,
            shoppingCart_id=idShoppingCart)
        scLine.save()

    return scLine

def update_product(request):
    idShoppingCart = request.GET.get('idCart',None)
    idProduct = request.GET.get('idProduct',None)
    newQuantity = request.GET.get('quantity',None)
    
    scLine = ShoppingCartLine.objects.filter(shoppingCart_id=idShoppingCart,product_id=idProduct)
    scLine.update(quantity = newQuantity)   
    
    data = {
        'update': 'ok',
    }

    return JsonResponse(data)

def delete_product(request):
    idShoppingCart = request.GET.get('idCart',None)
    idProduct = request.GET.get('idProduct',None)

    scLine = ShoppingCartLine.objects.filter(shoppingCart_id=idShoppingCart,product_id=idProduct)

    scLine.delete()
    
    data = {
        'delete': 'ok',
    }

    return JsonResponse(data)

def update_total(request):
    idShoppingCart = request.GET.get('idCart',None)
    shoppingCart = get_object_or_404(ShoppingCart, pk=idShoppingCart)
    data = {
        'total': shoppingCart.total_price,
    }

    return JsonResponse(data)

def update_badge(request):
    idShoppingCart = request.GET.get('idCart',None)
    numItems = ShoppingCartLine.objects.filter(shoppingCart_id=idShoppingCart).count()
    data = {
        'count': numItems,
    }

    return JsonResponse(data)
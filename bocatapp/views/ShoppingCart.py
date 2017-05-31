# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from customer.models import ShoppingCart, ShoppingCartLine
from bocatapp.models import User
from seller.models import Product
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import F
import datetime
from bocatapp.views import home
from django.utils.translation import ugettext_lazy as _


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

            try:
                actualShoppingCart = ShoppingCart.objects.get(pk=idShoppingCart)
            except ShoppingCart.DoesNotExist:
                actualShoppingCart = None

            if not shoppingCart and not actualShoppingCart:
                if request.user.is_authenticated():
                    if request.user.has_perm('bocatapp.customer'):
                        new_shoppingcart = ShoppingCart(
                            customer=request.user,
                            checkout=False)
                else:
                    new_shoppingcart = ShoppingCart(
                        checkout=False)
                new_shoppingcart.save()
                idShoppingCart = new_shoppingcart.pk
            else:
                if not shoppingCart:
                    ShoppingCart.objects.filter(pk=idShoppingCart).update(customer=customer[0])
                else:
                    productsShoppingCart = ShoppingCartLine.objects.filter(shoppingCart_id=shoppingCart[0].id)
                    productsActualShoppingCart = ShoppingCartLine.objects.filter(shoppingCart_id=idShoppingCart)

                    if productsActualShoppingCart and productsActualShoppingCart.count() > 0:
                        if int(idShoppingCart) != int(shoppingCart[0].pk):
                            shoppingCart[0].delete()
                            ShoppingCart.objects.filter(pk=idShoppingCart).update(customer=customer[0])
                    else:
                        if int(idShoppingCart) != int(shoppingCart[0].pk):
                            if actualShoppingCart:
                                actualShoppingCart.delete()
                            
                            idShoppingCart = shoppingCart[0].pk
        else:
            actualShoppingCart = ShoppingCart.objects.filter(pk=idShoppingCart)
            actualShoppingCart.delete()
            idShoppingCart = "None"
    else:
        actualShoppingCart = ShoppingCart.objects.filter(pk=idShoppingCart)
        if not actualShoppingCart:
            new_shoppingcart = ShoppingCart(
                        checkout=False)
            new_shoppingcart.save()
            idShoppingCart = new_shoppingcart.pk
            


    data = {
        'cookie': idShoppingCart
    }

    return JsonResponse(data)
    

# Vista del carrito de compra actual del customer logueado
def list_shopping_cart(request, pk):
    if request.user.is_authenticated():
        if request.user.has_perm('bocatapp.customer'):
            shoppingcart = ShoppingCart.objects.get(pk=pk)
            if shoppingcart.customer.pk == request.user.pk:
                return render(request, 'shoppingcart.html', {'shoppingcart': shoppingcart})
    else:
        shoppingcart = ShoppingCart.objects.get(pk=pk)
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
            'message': unicode(_("Product has not been added to cart")),
    }

    
    if productsInSC.count() == 0:
        res = add_to_shoppingcart_line(idShoppingCart, idProduct, newQuantity)
    else:
        for items in productsInSC:
            item = get_object_or_404(Product, pk=items.product_id)
            if newProduct.local_id != item.local_id:
                data = {
                    'add': 'no',
                    'message': unicode(_("You can not add products from different locations.")),
                }
                sameLocal = 0    

        if sameLocal == 1:
            res = add_to_shoppingcart_line(idShoppingCart, idProduct, newQuantity)   

    if res:
        data = {
            'add': 'ok',
            'message': unicode(_("The product has been successfully added to cart.")),
        }

    return JsonResponse(data)

def add_to_shoppingcart_line(idShoppingCart, idProduct, newQuantity):
    scLine = ShoppingCartLine.objects.filter(shoppingCart_id=idShoppingCart,product_id=idProduct)

    if int(newQuantity) > 0:
        if scLine:
            scLine.update(quantity = F('quantity')+newQuantity)
        else:
            scLine = ShoppingCartLine(
                quantity=newQuantity,
                product_id=idProduct,
                shoppingCart_id=idShoppingCart)
            scLine.save()
    else:
        scLine = 0

    return scLine

def update_product(request):
    idShoppingCart = request.GET.get('idCart',None)
    idProduct = request.GET.get('idProduct',None)
    newQuantity = request.GET.get('quantity',None)
    
    scLine = ShoppingCartLine.objects.filter(shoppingCart_id=idShoppingCart,product_id=idProduct)
    if int(newQuantity) > 0:
        scLine.update(quantity = newQuantity)
        data = {
            'update': 'ok',
            'message': unicode(_("The product has been updated successfully.")),
        }
    else:
        data = {
            'update': 'no',
            'message': unicode(_("The product has not been updated successfully.")),
        } 
    
    

    return JsonResponse(data)

def delete_product(request):
    idShoppingCart = request.GET.get('idCart',None)
    idProduct = request.GET.get('idProduct',None)

    scLine = ShoppingCartLine.objects.filter(shoppingCart_id=idShoppingCart,product_id=idProduct)

    scLine.delete()
    
    data = {
        'delete': 'ok',
        'message': unicode(_("The product has been removed from the cart.")),
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
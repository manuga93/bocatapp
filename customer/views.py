from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from customer.services import OrderService
from django.template import RequestContext
from django.http.response import HttpResponseRedirect
from customer.models import Order, OrderLine, ShoppingCart, ShoppingCartLine
from seller.models import Product

# Create your views here.

# This method is for testing the funcionality


def all_orders(request):
    try:
        orders = OrderService.find_all_orders()
        return render_to_response('orders.html', {'orders': orders}, context_instance=RequestContext(request))
    except Order.DoesNotExist:
        return render_to_response('error.html', context_instance=RequestContext(request))


def order_line_by_order(request, order_id):
    try:
        orders_line = OrderService.find_order_line_by_order(order_id)
        return render_to_response('ordersLine.html', {'lines': orders_line}, context_instance=RequestContext(request))
    except OrderLine.DoesNotExist:
        return render_to_response('error.html', context_instance=RequestContext(request))


def do_order_line(request, id1):
    order_line = get_object_or_404(OrderLine, pk=id1)
    order_line.status = True
    order_line.save()
    OrderService.set_order_status(order_line.order_id)
    return HttpResponseRedirect("/customer/ordersLine/" + str(order_line.order_id))


# Vista del carrito de compra actual del customer logueado
def list_shoppingcart(request):
    current_user = request.user
    shoppingcart = ShoppingCart.objects.get(customer_id=current_user.id)
    shoppingcart_line = ShoppingCartLine.objects.filter(shoppingCart_id=shoppingcart.id)
    return render(request, 'shoppingcart.html', {'shoppingcart_line': shoppingcart_line})


# Metodo para agregar un producto al carrito de compra
def add_shoppingcart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    current_user = request.user
    shoppingcart = ShoppingCart.objects.get(customer_id=current_user.id)

    shoppingcart_line = ShoppingCartLine(quantity=1,
               product=product,
               shoppingCart=shoppingcart)
    shoppingcart_line.save()
    
    return redirect('customer.views.list_shoppingcart')